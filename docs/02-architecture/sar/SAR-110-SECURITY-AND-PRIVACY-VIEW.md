# SAR-110 — Segurança e privacidade

- Contas locais baseline; OIDC opcional por issuer+subject.
- Sessões opacas server-side, CSRF ligado à sessão, same-origin e CORS allowlist.
- PAT opaco, hash persistido, scope, expiry e revogação.
- TLS obrigatório para exposição em rede.
- Autorização central por aplicação/projeto/recurso.
- Egress e providers allowlisted; SSRF e licenças falham fechados.
- Redaction allowlist; audit append-only protegido.
- ModelPacks assinados, pinados, opt-in e importáveis offline.

Threat model e controles são rastreados por requirements, ADR-028, ADR-034, ADR-047 e ADR-054.
