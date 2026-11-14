import { useId, useRef, type ComponentProps, type ReactNode } from "react";
import type { ProjectMember } from "../../../operator_experience/contracts/openapi/generated";
import { roleLabels } from "../contas-locais-bootstrap-unico-sessoes-tokens-e-adapter/response-safety";
import { useProjectAccess, type AccessResult } from "./use-project-access";
import "./surface.css";

const value = (form: FormData, name: string) => String(form.get(name) ?? "");
function Field({ label, ...props }: ComponentProps<"input"> & { label: string }) {
  const id = useId();
  return <label htmlFor={id}>{label}<input id={id} {...props} /></label>;
}
function AccessForm({ title, action, disabled, children, invalidate, submit }: {
  title: string; action: string; disabled: boolean; children: ReactNode;
  invalidate: () => void; submit: (form: FormData, key: string) => Promise<boolean>;
}) {
  const key = useRef(crypto.randomUUID());
  return <section aria-label={title}><h3>{title}</h3>
    <form aria-label={title} onInput={() => { key.current = crypto.randomUUID(); invalidate(); }} onSubmit={event => {
      event.preventDefault(); if (disabled) return;
      const form = event.currentTarget;
      // Same intention retries with the same key; edits and success start a new one.
      void submit(new FormData(form), key.current).then(success => {
        if (success) {
          key.current = crypto.randomUUID();
          const password = form.elements.namedItem("password");
          if (password instanceof HTMLInputElement) password.value = "";
        }
      });
    }}><fieldset disabled={disabled}>{children}<button>{action}</button></fieldset></form>
  </section>;
}
function Feedback({ result }: { result: AccessResult | null }) {
  if (!result) return <p role="status">Nenhuma consulta confirmada.</p>;
  const problem = result.problem;
  return <div role={result.phase === "failure" ? "alert" : "status"}>
    <p>{result.message}{result.status !== undefined && ` HTTP ${result.status}.`}</p>
    {problem && <dl>{(["type", "title", "status", "code", "detail", "instance"] as const).map(field =>
      problem[field] !== undefined && <div key={field}><dt>{field}</dt><dd>{problem[field]}</dd></div>)}</dl>}
    {result.decision && <>
      <p>{result.decision.allowed ? "Permissão confirmada nesta consulta." : "Permissão negada pela API."}</p>
      <p>Política: {result.decision.policyVersion}. Motivo: {result.decision.reasonCode}.</p>
      <p>Esta consulta não autoriza outra operação. O servidor verifica cada uso novamente.</p>
    </>}
    {result.members && <><p>{result.members.length ? "Membros retornados pela API:" : "Nenhum membro retornado pela API."}</p>
      <ul>{result.members.map(member => <li key={member.userId}>{member.userId} — {roleLabels[member.role]} — revisão {member.revision}</li>)}</ul>
      {result.more && <p>A API indica mais resultados; esta lista é parcial. Este contrato não publica parâmetro de paginação.</p>}
    </>}
    {result.member && <p>Vínculo confirmado: {result.member.userId} — {roleLabels[result.member.role]} — revisão {result.member.revision}.</p>}
  </div>;
}

export function ProjectAccessSurface() {
  const access = useProjectAccess();
  const disabled = access.busy || !access.session;
  return <div className="project-access">
    <h2>Autorização e membros do projeto</h2>
    <p>A API decide as permissões. Nenhum papel informado ou resultado anterior concede acesso nesta página.</p>
    <p aria-live="polite">{access.session ? "Sessão confirmada pela API." : "Autentique-se para consultar ou vincular membros."}</p>
    <AccessForm title="Sessão local" action="Iniciar sessão" disabled={access.busy} invalidate={access.invalidate}
      submit={(form, key) => access.login(value(form, "username"), value(form, "password"), key)}>
      <Field label="Usuário" name="username" required autoComplete="username" />
      <Field label="Senha" name="password" type="password" required autoComplete="current-password" />
    </AccessForm>
    <AccessForm title="Consultar autorização" action="Verificar autorização" disabled={disabled} invalidate={access.invalidate}
      submit={form => access.check({ action: value(form, "action"), resourceType: value(form, "resourceType"),
        ...(value(form, "resourceId") ? { resourceId: value(form, "resourceId") } : {}) })}>
      <p>Informe a ação e o tipo de recurso do contrato consumido. A API rejeita valores desconhecidos.</p>
      <p>Artefatos e caminhos não têm concessão publicada na política integrada. O contrato HTTP não publica campo de caminho físico ou comando para conceder esse acesso.</p>
      <Field label="Ação" name="action" required placeholder="project_member:list" />
      <Field label="Tipo de recurso" name="resourceType" required placeholder="project" />
      <Field label="ID do recurso (opcional)" name="resourceId" />
    </AccessForm>
    <AccessForm title="Membros do projeto" action="Consultar membros" disabled={disabled} invalidate={access.invalidate}
      submit={form => access.list(value(form, "projectId"))}>
      <Field label="ID do projeto" name="projectId" required />
    </AccessForm>
    <AccessForm title="Vincular conta existente" action="Vincular membro" disabled={disabled} invalidate={access.invalidate}
      submit={(form, key) => access.add(value(form, "projectId"), value(form, "userId"), value(form, "role") as ProjectMember["role"], key)}>
      <p>O servidor valida o projeto, a conta existente e a autorização. Falhas podem ser reenviadas sem editar para preservar a chave da tentativa.</p>
      <Field label="ID do projeto" name="projectId" required /><Field label="ID da conta" name="userId" required />
      <label>Papel<select name="role" required defaultValue=""><option disabled value="">Selecione</option>
        {Object.entries(roleLabels).map(([role, label]) => <option key={role} value={role}>{label}</option>)}</select></label>
    </AccessForm>
    <section aria-label="Resultado"><h3>Resultado</h3><Feedback result={access.result} /></section>
  </div>;
}
