import { useEffect, useRef, useState } from "react";
import { api, client } from "../../../operator_experience/contracts/frontend-shell";
import type {
  Session, Problem, PostAuthBootstrapRequest, PostAuthSessionRequest, PostAuthTokensRequest,
  PostProjectsProjectidMembersRequest, GetAuthorizationCheckData, GetAuthOidcCallbackData,
  PostAuthBootstrapResponse, PostAuthSessionResponse, PostAuthTokensResponse,
  GetAuthOidcCallbackResponse, GetProjectsProjectidMembersResponse,
  PostProjectsProjectidMembersResponse, GetAuthorizationCheckResponse,
} from "../../../operator_experience/contracts/openapi/generated";
import * as safety from "./response-safety";

type Responses = {
  bootstrap: PostAuthBootstrapResponse; login: PostAuthSessionResponse; logout: void;
  tokens: PostAuthTokensResponse; oidc: GetAuthOidcCallbackResponse;
  members: GetProjectsProjectidMembersResponse; member: PostProjectsProjectidMembersResponse;
  authorization: GetAuthorizationCheckResponse;
};
export type Outcome<T> = { phase: "pending" } | { phase: "success"; data: T }
  | { phase: "failure"; problem: Problem | null; message: string };
type Results = { [K in keyof Responses]?: Outcome<Responses[K]> };
type ApiResult = { data?: unknown; error?: unknown; response: Response };

export function useIdentityAccess() {
  const [results, setResults] = useState<Results>({});
  const [session, setSession] = useState<Session | null>(null);
  const [sessionEtag, setSessionEtag] = useState("");
  const [secret, setSecret] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);
  const [notice, setNotice] = useState("");
  const lock = useRef(false);
  const epoch = useRef(0);
  const pending = useRef<AbortController | null>(null);

  function clearIdentity() {
    epoch.current += 1;
    setSession(null); setSessionEtag(""); setSecret(null); setResults({});
  }
  useEffect(() => () => pending.current?.abort(), []);
  useEffect(() => {
    const discard = () => { if (document.hidden) setSecret(null); };
    document.addEventListener("visibilitychange", discard);
    return () => document.removeEventListener("visibilitychange", discard);
  }, []);
  useEffect(() => {
    if (!session) return;
    let timer: ReturnType<typeof setTimeout>;
    function checkExpiry() {
      const remaining = Date.parse(session!.expiresAt) - Date.now();
      if (remaining <= 0) {
        pending.current?.abort(); clearIdentity();
        setNotice("Sessão expirada; autentique novamente.");
      } else timer = setTimeout(checkExpiry, Math.min(remaining, 2_147_483_647));
    }
    checkExpiry();
    return () => clearTimeout(timer);
  }, [session]);

  async function run<K extends keyof Responses>(
    operation: K, request: (config: ReturnType<typeof options>) => Promise<ApiResult>,
    guard: (value: unknown) => value is Responses[K], status: number,
    settings: { protected?: boolean; authentication?: boolean; secrets?: string[];
      present?: (data: Responses[K], response: Response) => Responses[K] } = {},
  ): Promise<boolean> {
    if (lock.current) return false;
    if (settings.protected && !safety.validSession(session)) {
      clearIdentity();
      setResults({ [operation]: { phase: "failure", problem: null, message: "Inicie uma sessão válida antes desta operação." } });
      return false;
    }
    const secrets = [...(settings.secrets ?? []), session?.csrfToken ?? "", secret ?? ""];
    if (settings.authentication) { clearIdentity(); setNotice(""); }
    setSecret(null); lock.current = true; setBusy(true);
    const controller = new AbortController(); pending.current = controller;
    const currentEpoch = epoch.current;
    setResults(previous => ({ ...previous, [operation]: { phase: "pending" } }));
    try {
      const result = await request(options(controller.signal));
      if (controller.signal.aborted || currentEpoch !== epoch.current) return false;
      if (!result.response.ok) {
        const problem = result.response.headers.get("content-type")?.split(";")[0]?.trim() === "application/problem+json"
          ? safety.safeProblem(result.error, result.response.status, secrets) : null;
        if (!problem || [401, 403].includes(result.response.status)) clearIdentity();
        setResults(previous => ({ ...previous, [operation]: { phase: "failure", problem,
          message: problem ? "Pedido rejeitado pela API." : "Resposta inesperada da API; nenhuma permissão foi confirmada." } }));
        return false;
      }
      if (result.response.status !== status || (status !== 204
        && result.response.headers.get("content-type")?.split(";")[0]?.trim() !== "application/json") || !guard(result.data)) {
        throw new Error("Unexpected response");
      }
      const data = settings.present ? settings.present(result.data, result.response) : result.data;
      setResults(previous => ({ ...previous, [operation]: { phase: "success", data } }));
      return true;
    } catch {
      if (controller.signal.aborted || currentEpoch !== epoch.current) return false;
      clearIdentity();
      setResults({ [operation]: { phase: "failure", problem: null,
        message: "Falha de comunicação ou resposta inválida; nenhuma permissão foi confirmada." } });
      return false;
    } finally {
      if (pending.current === controller) pending.current = null;
      lock.current = false; setBusy(false);
    }
  }
  function options(signal: AbortSignal) {
    return { baseUrl: new URL(client.getConfig().baseUrl ?? "/api/v1", window.location.origin).href,
      credentials: "same-origin" as const, cache: "no-store" as const, redirect: "error" as const,
      responseStyle: "fields" as const, throwOnError: false as const, signal };
  }
  function acceptSession(value: Session, response: Response) {
    setSession(value); setSessionEtag(response.headers.get("etag") ?? "");
  }
  const headers = (key: string) => ({ "Idempotency-Key": key });
  return {
    results, session, sessionEtag, secret, busy, notice, discardSecret: () => setSecret(null),
    bootstrap: (body: PostAuthBootstrapRequest, key: string) => run("bootstrap",
      opts => api.postAuthBootstrap({ ...opts, body, headers: headers(key) }), safety.bootstrapResponse, 202,
      { authentication: true, secrets: [body.password] }),
    login: (body: PostAuthSessionRequest, key: string) => run("login",
      opts => api.postAuthSession({ ...opts, body, headers: headers(key) }), safety.sessionResponse, 202,
      { authentication: true, secrets: [body.password], present: (data, response) => { acceptSession(data.data, response); return data; } }),
    logout: (key: string, ifMatch: string) => run("logout",
      opts => api.deleteAuthSession({ ...opts, headers: { ...headers(key), "If-Match": ifMatch } }), safety.logoutResponse, 204,
      { protected: true, authentication: true }),
    issueToken: (body: PostAuthTokensRequest, key: string) => run("tokens",
      opts => api.postAuthTokens({ ...opts, body, headers: headers(key) }), safety.tokenResponse, 201,
      { protected: true, present: data => {
        const issued = safety.issuedSecret(data.data); setSecret(issued);
        // Retain only the generated nonsecret DTO; discarding removes the sole UI copy.
        const { tokenId, prefix, scopes, expiresAt } = data.data;
        return { data: { tokenId, prefix: safety.redact(prefix, [issued ?? ""]),
          scopes: scopes.map(scope => safety.redact(scope, [issued ?? ""])),
          ...(expiresAt !== undefined ? { expiresAt } : {}) } };
      } }),
    oidc: (query: GetAuthOidcCallbackData["query"]) => run("oidc",
      opts => api.getAuthOidcCallback({ ...opts, query }), safety.oidcResponse, 200,
      { authentication: true, secrets: [query.code, query.state], present: (data, response) => { acceptSession(data.data.session, response); return data; } }),
    listMembers: (projectId: string) => run("members",
      opts => api.getProjectsProjectidMembers({ ...opts, path: { projectId } }),
      (value): value is GetProjectsProjectidMembersResponse => safety.membersResponse(value)
        && value.items.every(item => item.projectId.toLowerCase() === projectId.toLowerCase()), 200, { protected: true }),
    addMember: (projectId: string, body: PostProjectsProjectidMembersRequest, key: string) => run("member",
      opts => api.postProjectsProjectidMembers({ ...opts, path: { projectId }, body, headers: headers(key) }),
      (value): value is PostProjectsProjectidMembersResponse => safety.memberResponse(value)
        && value.data.projectId.toLowerCase() === projectId.toLowerCase()
        && value.data.userId.toLowerCase() === body.userId.toLowerCase() && value.data.role === body.role,
      201, { protected: true }),
    checkAuthorization: (query: GetAuthorizationCheckData["query"]) => run("authorization",
      opts => api.getAuthorizationCheck({ ...opts, query }), safety.authorizationResponse, 200, { protected: true }),
  };
}
