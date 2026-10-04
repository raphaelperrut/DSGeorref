import { useEffect, useState } from "react";
import type { ProjectMember } from "../../../operator_experience/contracts/openapi/generated";
import { Field, OperationPanel } from "./operation-panel";
import { roleLabels } from "./response-safety";
import { useIdentityAccess } from "./use-identity-access";
import "./surface.css";

const value = (form: FormData, name: string) => String(form.get(name) ?? "");
export function IdentitySurface() {
  const identity = useIdentityAccess();
  const { results, busy, session, secret } = identity;
  const [revealed, setRevealed] = useState(false);
  useEffect(() => setRevealed(false), [secret]);
  const protectedDisabled = busy || !session;
  return <div className="identity-surface">
    <header><h2>Identidade e acesso</h2><p>Contas locais, bootstrap único, sessões, tokens e OIDC.</p>
      <p aria-live="polite" data-testid="session-state">{session
        ? `Sessão válida recebida da API. Usuário: ${session.userId}. Expira: ${session.expiresAt}.`
        : "Sessão não confirmada. Autentique-se para usar as operações protegidas."}</p>
      {identity.notice && <p role="alert">{identity.notice}</p>}
    </header>
    <div className="identity-grid">
      <OperationPanel title="Bootstrap único" action="Executar bootstrap" disabled={busy} outcome={results.bootstrap}
        submit={(form, key) => identity.bootstrap({ username: value(form, "username"), password: value(form, "password"), displayName: value(form, "displayName") }, key)}
        result={results.bootstrap?.phase === "success" && <p>Bootstrap confirmado pela API. Administrador: {results.bootstrap.data.data.administratorId}. Inicie uma sessão para continuar.</p>}>
        <p>A API decide se esta tentativa é permitida; nenhuma disponibilidade prévia é presumida.</p>
        <Field label="Usuário" name="username" required minLength={3} autoComplete="username" />
        <Field label="Senha" name="password" type="password" required minLength={12} autoComplete="new-password" />
        <Field label="Nome de exibição" name="displayName" required />
      </OperationPanel>
      <OperationPanel title="Sessão local" action="Iniciar sessão" disabled={busy} outcome={results.login}
        submit={(form, key) => identity.login({ username: value(form, "username"), password: value(form, "password") }, key)}
        result={<p>Sessão confirmada pela API.</p>}>
        <Field label="Usuário" name="username" required autoComplete="username" />
        <Field label="Senha" name="password" type="password" required autoComplete="current-password" />
      </OperationPanel>
      <OperationPanel title="Encerrar sessão" action="Encerrar sessão" disabled={protectedDisabled} outcome={results.logout}
        submit={(form, key) => identity.logout(key, value(form, "ifMatch"))} result={<p>Sessão encerrada pela API.</p>}>
        <p>Use a revisão/ETag retornada pela API. Uma falha não confirma revogação.</p>
        <Field key={identity.sessionEtag} label="If-Match da sessão" name="ifMatch" defaultValue={identity.sessionEtag} required />
      </OperationPanel>
      <OperationPanel title="Emitir token pessoal" action="Emitir token" disabled={protectedDisabled} outcome={results.tokens}
        submit={(form, key) => identity.issueToken({ name: value(form, "name"), scopes: value(form, "scopes").split(",").map(scope => scope.trim()),
          ...(value(form, "expiresAt") ? { expiresAt: value(form, "expiresAt") } : {}) }, key)}
        result={results.tokens?.phase === "success" && <>
          <p>Emissão confirmada pela API. Prefixo: {results.tokens.data.data.prefix}.</p>
          <p>Scopes: {results.tokens.data.data.scopes.join(", ")}</p>
          {secret && <div className="identity-secret">
            <p>Guarde o token agora. O valor permanece somente nesta página até ser descartado, ocultada a página ou iniciada outra operação.</p>
            <Field label="Token emitido" type={revealed ? "text" : "password"} value={secret} readOnly autoComplete="off" />
            <button type="button" onClick={() => setRevealed(previous => !previous)}>{revealed ? "Ocultar token" : "Mostrar token"}</button>
            <button type="button" onClick={identity.discardSecret}>Descartar valor exibido</button>
          </div>}
        </>}>
        <Field label="Nome do token" name="name" required maxLength={100} />
        <Field label="Scopes separados por vírgula" name="scopes" required />
        <Field label="Expiração ISO 8601 (opcional)" name="expiresAt" placeholder="AAAA-MM-DDThh:mm:ssZ" />
      </OperationPanel>
      <OperationPanel title="Membros locais do projeto" action="Consultar membros" disabled={protectedDisabled} outcome={results.members}
        submit={form => identity.listMembers(value(form, "projectId"))}
        result={results.members?.phase === "success" && <>
          <p>Consulta confirmada. {results.members.data.items.length} membro(s).</p>
          <ul>{results.members.data.items.map(member => <li key={member.userId}>{member.userId} — {roleLabels[member.role]} — revisão {member.revision}</li>)}</ul>
          {results.members.data.page.nextCursor && <p>A API informa que há mais resultados.</p>}
        </>}>
        <Field label="ID do projeto" name="projectId" required />
      </OperationPanel>
      <OperationPanel title="Vincular conta local existente" action="Vincular membro" disabled={protectedDisabled} outcome={results.member}
        submit={(form, key) => identity.addMember(value(form, "projectId"), { userId: value(form, "userId"), role: value(form, "role") as ProjectMember["role"] }, key)}
        result={results.member?.phase === "success" && <p>Vínculo confirmado: {results.member.data.data.userId} — {roleLabels[results.member.data.data.role]}.</p>}>
        <p>O servidor valida a conta existente e a permissão para o projeto.</p>
        <Field label="ID do projeto" name="projectId" required /><Field label="ID da conta local" name="userId" required />
        <label>Papel<select name="role" required defaultValue=""><option value="" disabled>Selecione um papel</option>{Object.entries(roleLabels).map(([role, label]) => <option key={role} value={role}>{label}</option>)}</select></label>
      </OperationPanel>
      <OperationPanel title="Callback OIDC" action="Validar callback" disabled={busy} outcome={results.oidc}
        submit={form => identity.oidc({ code: value(form, "code"), state: value(form, "state") })}
        result={results.oidc?.phase === "success" && <p>Callback validado pela API. Novo vínculo confirmado: {results.oidc.data.data.linked ? "sim" : "não"}.</p>}>
        <p>Informe os parâmetros do fluxo OIDC iniciado pelo servidor.</p>
        <Field label="Code OIDC" name="code" type="password" required autoComplete="off" />
        <Field label="State OIDC" name="state" type="password" required autoComplete="off" />
      </OperationPanel>
      <OperationPanel title="Consultar autorização" action="Verificar autorização" disabled={protectedDisabled} outcome={results.authorization}
        submit={form => identity.checkAuthorization({ action: value(form, "action"), resourceType: value(form, "resourceType"),
          ...(value(form, "resourceId") ? { resourceId: value(form, "resourceId") } : {}) })}
        result={results.authorization?.phase === "success" && <>
          <p>{results.authorization.data.data.allowed ? "Permissão confirmada nesta consulta." : "Permissão negada pela API."}</p>
          <p>Política: {results.authorization.data.data.policyVersion}. Motivo: {results.authorization.data.data.reasonCode}.</p>
          <p>A API verifica novamente a autorização ao executar cada ação.</p>
        </>}>
        <Field label="Ação" name="action" required /><Field label="Tipo de recurso" name="resourceType" required />
        <Field label="ID do recurso (opcional)" name="resourceId" />
      </OperationPanel>
    </div>
  </div>;
}
