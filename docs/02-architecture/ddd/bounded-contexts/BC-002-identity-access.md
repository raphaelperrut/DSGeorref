# BC-002 — Identidade e Controle de Acesso

- **Classificação DDD:** `Generic`
- **Papel estratégico:** `Suporte`
- **Runtime:** `Participa do monólito modular por ports e adapters`
- **Épicos owners:** `EPIC-008, EPIC-009, EPIC-010, EPIC-011`

## Missão

Gerenciar identidades, sessões, tokens, memberships e decisões de autorização da instância.

## Linguagem ubíqua local

- `conta`
- `sessão`
- `token pessoal`
- `membership`
- `autorização`

## Aggregates e raízes

- `Account`
- `Session`
- `PersonalAccessToken`
- `ProjectMembership`
- `AuthorizationPolicy`

## Comandos

- `BootstrapAdmin`
- `CriarSessao`
- `RevogarSessao`
- `EmitirToken`
- `VincularMembro`

## Eventos de domínio

- `AdminBootstrapped`
- `SessionCreated`
- `SessionRevoked`
- `TokenIssued`
- `MembershipChanged`

## Relações

- **Upstream:** Nenhum contexto de produto.
- **Downstream:** BC-003, BC-004, BC-010, BC-011, BC-012, BC-013, BC-014, BC-016.
- As relações normativas e os padrões de integração estão em `../DDD-040-CONTEXT-MAP.md`.

## Autoridade

O contexto é o único owner do significado, invariantes e transições de seus aggregates. Outros contextos recebem IDs, snapshots, eventos ou DTOs publicados; nunca importam entidades internas.

## Proibições

- não compartilhar ORM models, state machines ou repositories entre contexts;
- não acessar tabelas de outro contexto;
- não publicar evento antes do commit autoritativo;
- não usar UI, API, broker, filesystem ou banco como substituto do modelo de domínio;
- não criar módulo `common`, `utils` ou `shared-domain` para escapar do boundary.

## Contratos

Contratos públicos são registrados em `contracts/contexts/CONTEXT_CONTRACT_OWNERSHIP.csv`. Mudança breaking exige ADR ou versão nova do contrato, migration e rollback quando aplicável.
