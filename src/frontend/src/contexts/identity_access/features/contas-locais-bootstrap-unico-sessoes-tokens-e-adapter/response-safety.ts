import type {
  BootstrapStatus, Session, PersonalAccessToken, PersonalAccessTokenWritable,
  ProjectMember, AuthorizationDecision, OidcCallbackResult, Problem,
  PostAuthBootstrapResponse, PostAuthSessionResponse, PostAuthTokensResponse,
  GetAuthOidcCallbackResponse, GetProjectsProjectidMembersResponse,
  PostProjectsProjectidMembersResponse, GetAuthorizationCheckResponse,
} from "../../../operator_experience/contracts/openapi/generated";

// UI labels, checked against the generated union; no second domain enum.
export const roleLabels = {
  owner: "Owner", editor: "Editor", reviewer: "Reviewer", viewer: "Viewer",
} satisfies Record<ProjectMember["role"], string>;

export function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}
const text = (value: unknown): value is string => typeof value === "string" && value.length > 0;
const uuid = (value: unknown): value is string =>
  typeof value === "string" && /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(value);
const date = (value: unknown): value is string =>
  typeof value === "string" && /^\d{4}-\d{2}-\d{2}T/.test(value) && Number.isFinite(Date.parse(value));
const only = (value: Record<string, unknown>, fields: readonly string[]) => Object.keys(value).every(key => fields.includes(key));

// Narrow only the published data used by the UI. These are not DTOs or schemas.
function bootstrap(value: unknown): value is BootstrapStatus {
  return isRecord(value) && only(value, ["administratorId", "sessionId", "createdAt"])
    && uuid(value.administratorId) && uuid(value.sessionId) && date(value.createdAt);
}
export function validSession(value: unknown): value is Session {
  return isRecord(value) && only(value, ["sessionId", "userId", "expiresAt", "csrfToken"]) && uuid(value.sessionId) && uuid(value.userId)
    && date(value.expiresAt) && Date.parse(value.expiresAt) > Date.now()
    && typeof value.csrfToken === "string" && value.csrfToken.length >= 32;
}
function token(value: unknown): value is PersonalAccessToken {
  return isRecord(value) && only(value, ["tokenId", "token", "prefix", "scopes", "expiresAt"]) && uuid(value.tokenId) && text(value.prefix)
    && Array.isArray(value.scopes) && value.scopes.length > 0 && value.scopes.every(text)
    && (value.expiresAt === undefined || value.expiresAt === null || date(value.expiresAt))
    && (value.token === undefined || text(value.token));
}
export function issuedSecret(value: PersonalAccessToken): string | null {
  if ("token" in value && text(value.token)) {
    return (value as PersonalAccessTokenWritable).token;
  }
  return null;
}
function member(value: unknown): value is ProjectMember {
  return isRecord(value) && only(value, ["projectId", "userId", "role", "revision"]) && uuid(value.projectId) && uuid(value.userId)
    && typeof value.role === "string" && Object.hasOwn(roleLabels, value.role)
    && Number.isInteger(value.revision) && Number(value.revision) >= 1;
}
function decision(value: unknown): value is AuthorizationDecision {
  return isRecord(value) && only(value, ["allowed", "policyVersion", "reasonCode"])
    && typeof value.allowed === "boolean" && text(value.policyVersion) && text(value.reasonCode);
}
function oidc(value: unknown): value is OidcCallbackResult {
  return isRecord(value) && only(value, ["session", "linked"]) && validSession(value.session) && typeof value.linked === "boolean";
}
export const bootstrapResponse = (value: unknown): value is PostAuthBootstrapResponse =>
  isRecord(value) && only(value, ["data"]) && bootstrap(value.data);
export const sessionResponse = (value: unknown): value is PostAuthSessionResponse =>
  isRecord(value) && only(value, ["data"]) && validSession(value.data);
export const tokenResponse = (value: unknown): value is PostAuthTokensResponse =>
  isRecord(value) && only(value, ["data"]) && token(value.data);
export const oidcResponse = (value: unknown): value is GetAuthOidcCallbackResponse =>
  isRecord(value) && only(value, ["data"]) && oidc(value.data);
export const memberResponse = (value: unknown): value is PostProjectsProjectidMembersResponse =>
  isRecord(value) && only(value, ["data"]) && member(value.data);
export const authorizationResponse = (value: unknown): value is GetAuthorizationCheckResponse =>
  isRecord(value) && only(value, ["data"]) && decision(value.data);
export function membersResponse(value: unknown): value is GetProjectsProjectidMembersResponse {
  return isRecord(value) && only(value, ["items", "page"]) && Array.isArray(value.items) && value.items.every(member)
    && isRecord(value.page) && only(value.page, ["limit", "nextCursor"]) && Number.isInteger(value.page.limit)
    && Number(value.page.limit) >= 1 && Number(value.page.limit) <= 200
    && (value.page.nextCursor === undefined || value.page.nextCursor === null || typeof value.page.nextCursor === "string");
}
export const logoutResponse = (value: unknown): value is void =>
  value === undefined || (isRecord(value) && Object.keys(value).length === 0);

export function redact(value: string, secrets: readonly string[]): string {
  let safe = value;
  for (const secret of secrets.filter(Boolean).sort((a, b) => b.length - a.length)) {
    for (const encoding of new Set([secret, encodeURIComponent(secret)])) {
      safe = safe.split(encoding).join("[redigido]");
    }
  }
  return /Traceback \(most recent call last\)|\n\s*at\s+\S+/.test(safe)
    ? "[Informação interna omitida]" : safe;
}
export function safeProblem(value: unknown, status: number, secrets: readonly string[]): Problem | null {
  if (!isRecord(value) || !text(value.type) || !text(value.title) || !text(value.code)
    || !Number.isInteger(value.status) || value.status !== status || status < 400 || status > 599
    || (value.detail !== undefined && typeof value.detail !== "string")
    || (value.instance !== undefined && typeof value.instance !== "string")) return null;
  return {
    type: redact(value.type, secrets), title: redact(value.title, secrets), status,
    code: redact(value.code, secrets),
    ...(typeof value.detail === "string" ? { detail: redact(value.detail, secrets) } : {}),
    ...(typeof value.instance === "string" ? { instance: redact(value.instance, secrets) } : {}),
  };
}
