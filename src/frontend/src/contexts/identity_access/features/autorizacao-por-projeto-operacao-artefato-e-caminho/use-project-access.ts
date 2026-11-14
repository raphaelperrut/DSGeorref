import { useEffect, useRef, useState } from "react";
import { api, client } from "../../../operator_experience/contracts/frontend-shell";
import type { GetAuthorizationCheckData, ProjectMember, Session } from "../../../operator_experience/contracts/openapi/generated";
import * as safety from "../contas-locais-bootstrap-unico-sessoes-tokens-e-adapter/response-safety";

export type AccessResult = {
  operation: string; phase: "pending" | "failure" | "success";
  message: string; status?: number; problem?: ReturnType<typeof safety.safeProblem>;
  decision?: { allowed: boolean; policyVersion: string; reasonCode: string };
  members?: ProjectMember[]; more?: boolean; member?: ProjectMember;
};
type Reply = { data?: unknown; error?: unknown; response?: Response };

// Ephemeral presentation state only: each action still reaches the server.
export function useProjectAccess() {
  const [session, setSession] = useState<Session | null>(null);
  const [result, setResult] = useState<AccessResult | null>(null);
  const [busy, setBusy] = useState(false);
  const pending = useRef<AbortController | null>(null);
  const epoch = useRef(0);
  const lock = useRef(false);
  const invalidate = () => { epoch.current++; setResult(null); };
  useEffect(() => () => { epoch.current++; pending.current?.abort(); }, []);
  useEffect(() => {
    if (!session) return;
    let timer: ReturnType<typeof setTimeout>;
    function checkExpiry() {
      const remaining = Date.parse(session!.expiresAt) - Date.now();
      if (remaining > 0) { timer = setTimeout(checkExpiry, Math.min(remaining, 2_147_483_647)); return; }
      epoch.current++; pending.current?.abort(); setSession(null);
      setResult({ operation: "session", phase: "failure", message: "Sessão expirada. Autentique-se novamente." });
    }
    checkExpiry();
    return () => clearTimeout(timer);
  }, [session]);

  async function run(operation: string, status: number, protectedRequest: boolean,
    request: (config: ReturnType<typeof options>) => Promise<Reply>,
    present: (data: unknown) => Partial<AccessResult> | null, secrets: string[] = []) {
    if (lock.current) return false;
    invalidate();
    if (protectedRequest && !safety.validSession(session)) {
      setSession(null);
      setResult({ operation, phase: "failure", message: "Inicie uma sessão válida." });
      return false;
    }
    lock.current = true; setBusy(true);
    const controller = new AbortController(); pending.current = controller;
    const version = epoch.current;
    let httpStatus: number | undefined;
    setResult({ operation, phase: "pending", message: "Aguardando a API…" });
    try {
      const reply = await request(options(controller.signal));
      if (version !== epoch.current || controller.signal.aborted) return false;
      if (!reply.response) throw new Error("Missing response");
      httpStatus = reply.response.status;
      const contentType = reply.response.headers.get("content-type")?.split(";")[0]?.trim();
      // Text mode retains HTTP status even when the server sends invalid JSON.
      const raw = reply.response.ok ? reply.data : reply.error;
      const data: unknown = typeof raw === "string" ? JSON.parse(raw) : raw;
      if (!reply.response.ok) {
        const problem = contentType === "application/problem+json"
          ? safety.safeProblem(data, httpStatus, [...secrets, session?.csrfToken ?? ""]) : null;
        if (httpStatus === 401 || httpStatus === 403) setSession(null);
        setResult({ operation, phase: "failure", status: httpStatus, problem,
          message: problem ? "Pedido rejeitado pela API." : "Erro HTTP com resposta inválida; nenhuma permissão confirmada." });
        return false;
      }
      const presentation = httpStatus === status && contentType === "application/json" ? present(data) : null;
      if (!presentation) throw new Error("Invalid response");
      setResult({ operation, phase: "success", status: httpStatus, message: "Resposta confirmada pela API.", ...presentation });
      return true;
    } catch {
      if (version !== epoch.current || controller.signal.aborted) return false;
      if (httpStatus === 401 || httpStatus === 403 || operation === "session") setSession(null);
      setResult({ operation, phase: "failure", ...(httpStatus !== undefined ? { status: httpStatus } : {}),
        message: "Falha de comunicação ou resposta inválida; nenhuma permissão confirmada." });
      return false;
    } finally {
      if (pending.current === controller) pending.current = null;
      lock.current = false; setBusy(false);
    }
  }
  function options(signal: AbortSignal) {
    return { baseUrl: new URL(client.getConfig().baseUrl ?? "/api/v1", window.location.origin).href,
      credentials: "same-origin" as const, cache: "no-store" as const, redirect: "error" as const,
      responseStyle: "fields" as const, throwOnError: false as const, parseAs: "text" as const, signal };
  }
  return { session, result, busy, invalidate,
    login: (username: string, password: string, key: string) => {
      setSession(null);
      return run("session", 202, false,
        opts => api.postAuthSession({ ...opts, body: { username, password }, headers: { "Idempotency-Key": key } }),
        data => {
          if (!safety.sessionResponse(data)) return null;
          setSession(data.data); return {};
        }, [password]);
    },
    check: (query: GetAuthorizationCheckData["query"]) => run("authorization", 200, true,
      opts => api.getAuthorizationCheck({ ...opts, query }),
      data => safety.authorizationResponse(data) ? { decision: data.data } : null),
    list: (projectId: string) => run("members", 200, true,
      opts => api.getProjectsProjectidMembers({ ...opts, path: { projectId } }),
      data => safety.membersResponse(data) && data.items.every(item => item.projectId.toLowerCase() === projectId.toLowerCase())
        ? { members: data.items, more: Boolean(data.page.nextCursor) } : null),
    add: (projectId: string, userId: string, role: ProjectMember["role"], key: string) => run("member", 201, true,
      opts => api.postProjectsProjectidMembers({ ...opts, path: { projectId }, body: { userId, role },
        headers: { "Idempotency-Key": key, "X-CSRF-Token": session?.csrfToken ?? "" } }),
      data => safety.memberResponse(data) && data.data.projectId.toLowerCase() === projectId.toLowerCase()
        && data.data.userId.toLowerCase() === userId.toLowerCase() && data.data.role === role ? { member: data.data } : null),
  };
}
