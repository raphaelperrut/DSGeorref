# STORY-0473 / ISSUE-0583 — Validar acesso, redaction e exposição: canal append-only de auditoria, particionamento, digests, consulta e exportação assinada opcional

- **Tipo:** `História implementável`
- **Estado:** `Planned`
- **Épico pai:** `EPIC-075`
- **Sprint:** `SPRINT-011`
- **Domínio:** `OPS`
- **Bounded Context:** `BC-014 — Operações, Auditoria e Suporte`
- **Papel executor:** `Security`
- **TaskEnvelope:** `.codex/tasks/TASK-0473.json`

## História de usuário

Como administrador da instância, preciso validar acesso, redaction e exposição para “canal append-only de auditoria, particionamento, digests, consulta e exportação assinada opcional”, para que o resultado do épico seja implementável, verificável e integrável sem violar seus contratos.

## Resultado verificável

Validar acesso, redaction e exposição para a capacidade **canal append-only de auditoria, particionamento, digests, consulta e exportação assinada opcional**, com saída versionada, testes e evidência no commit candidato.

## Escopo

- `src/backend/dsgeorref/contexts/operations_audit/adapters/security/canal-append-only-de-auditoria-particionamento-digests/**`
- `tests/security/contexts/operations_audit/canal-append-only-de-auditoria-particionamento-digests/**`
## Fora de escopo

- Alterar ADR, contrato compartilhado ou regra de produto sem issue de decisão aprovada.
- Ampliar o escopo para outro épico ou introduzir dependência não declarada.
- Declarar gate aprovado sem evidência independente.

## Requisitos

Nenhum requisito exclusivo; valida integração do épico.

## ADRs e contratos

- `ADR-039`
- `ADR-054`
- `ADR-050`
- `ADR-026`
- `contracts/README.md`

## Dependências


`STORY-0470`, `STORY-0471`, `STORY-0472`

## Critérios de aceitação

- [ ] O resultado de “canal append-only de auditoria, particionamento, digests, consulta e exportação assinada opcional” é observável por contrato, interface, artifact ou evidência executável.
- [ ] Os requisitos vinculados possuem evidência explícita no commit candidato.
- [ ] Estados de erro e caminhos fail-closed aplicáveis são testados, sem fallback silencioso.
- [ ] Testes negativos cobrem abuso, autorização, secrets, path/egress e redaction aplicáveis.

## Testes obrigatórios

- `test_epic_075_seguranca_happy_path`
- `test_epic_075_seguranca_negative_paths`

## Evidências obrigatórias

- Resultado dos testes no commit candidato.
- Lista de arquivos alterados e justificativa de escopo.
- Handoff com limitações, riscos residuais e impacto em contratos.
- Aprovação independente aplicável ao mesmo commit.

## Condições de parada

- Decisão material de produto ou arquitetura não resolvida.
- Contrato necessário ausente, contraditório ou não versionado.
- Colisão de write scope com lane ativa.
- Critério de aceitação sem teste ou evidência objetiva.

## Prompt de execução Codex

Leia `AGENTS.md`, `.codex/roles/ROLE-010-security.md`, este documento, o épico `EPIC-075` e o TaskEnvelope `TASK-0473`. Trabalhe somente nos paths permitidos. Implemente o menor incremento que satisfaça todos os critérios, execute os testes, registre evidências e interrompa quando qualquer condição de parada ocorrer.


## Revisão SAR

- **Estado arquitetural:** `RESOLVED`
- **Decisão tecnológica necessária antes de iniciar:** `Nenhuma`
- **Atributos de qualidade dominantes:** `confidencialidade`, `integridade`, `auditabilidade`
- **Autoridade de dados:** PostgreSQL/PostGIS para estado; filesystem gerenciado para binários publicados; broker/telemetria são derivados.
- **Contrato de entrada:** referências e schemas listados no TaskEnvelope.
- **Contrato de saída:** artifact, código, schema, teste ou evidência versionada no commit candidato.
- **Migration/rollback:** obrigatório quando a história altera schema, estado persistido, artifact ou deployment; caso contrário `não aplicável` deve ser justificado no handoff.
- **Observabilidade:** falhas e transições relevantes devem emitir signal/event/audit sem cardinalidade ilimitada.
- **Gate de completude:** nenhum heading obrigatório vazio, placeholder, ID obsoleto ou dependência implícita.

`EVIDENCE_BOUND` não representa decisão arquitetural em aberto: indica parâmetro quantitativo cujo valor é promovido pelo Benchmark Profile declarado.


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-014` — Operações, Auditoria e Suporte.
- **Impacto no modelo:** `LOCAL_MODEL`.
- **Upstreams permitidos:** `BC-002, BC-010, BC-012, BC-013`.
- **Regra de integração:** DTO, evento, port ou ACL publicado; entidade, repository, ORM model e state machine não atravessam o boundary.
- **Package de produção:** context-first conforme `DDD-090-CONTEXT-OWNERSHIP-AND-CODE-LAYOUT.md`.
- **Resultado:** `PASS`.

## Revisão de Requisitos — Fase B

- **Resultado:** `PASS`
- **Critérios rastreados:** `AC-ISSUE-0583-01, AC-ISSUE-0583-02, AC-ISSUE-0583-03, AC-ISSUE-0583-04`
- **Base de requisitos:** `DERIVED_CONTROL`
- **ADRs governantes:** `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-030`, `ADR-031`, `ADR-032`
- **Conflito:** `Nenhum`
- **Redundância funcional:** `Nenhuma`
- **Requisito faltante:** `Não`
- **Requisito impossível:** `Não`
- **Dependência circular:** `Não`
- **Matriz canônica:** `docs/07-assurance/ACCEPTANCE_CRITERION_TRACEABILITY.csv`


## Revisão de ADRs — Fase D

- **Resultado:** `PASS`
- **ADRs aplicáveis:** `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-030`, `ADR-031`, `ADR-032`
- **Decisão em aberto:** `Nenhuma`
- **Regra:** implementar somente os boundaries listados; divergência ou lacuna interrompe a tarefa.


## Specification Review — Fase E

- **Especificações aplicáveis:** `SPEC-001`, `SPEC-004`
- **Status:** `PASS`
- A história deve parar se texto, schema, exemplo ou versão aplicável estiver ausente ou contraditório.

## Sprint Review — Fase F

| Dimensão | Aplicabilidade | Resultado |
|---|---|---|
| Dependências | 3 predecessores explícitos | PASS |
| Arquivos | 2 write scopes; deny scopes declarados | PASS |
| API | NOT_APPLICABLE | PASS |
| Banco | NOT_APPLICABLE | PASS |
| Frontend | NOT_APPLICABLE | PASS |
| Geo | NOT_APPLICABLE | PASS |
| IA | NOT_APPLICABLE | PASS |
| Testes | 2 testes obrigatórios | PASS |
| Artefatos | EVIDENCE_ONLY | PASS |
| Critérios | 4 critérios com IDs estáveis | PASS |
| Review | QA, Reviewer; mesmo commit candidato | PASS |

- **Matriz canônica:** `docs/07-assurance/PHASE-F-ISSUE-DELIVERY-REVIEW.csv`
- **Relatório da sprint:** `docs/07-assurance/phase-f/SPRINT-011-REVIEW.md`
- **Baseline:** `SAR-v2.9-PHASE-F`
- **Resultado:** `PASS`
## CTO Review — Fase G

- **Resultado:** `PASS`
- **Risk tier:** `CRITICAL`
- **Controles aplicáveis:** `CTO-001, CTO-003, CTO-004, CTO-005, CTO-006, CTO-008, CTO-010, CTO-012, CTO-013, CTO-014, CTO-015`
- **Gate de produção:** `SECURITY_AND_PRIVACY_GATES`
- **Regra:** implementação não pode publicar claim de custo, escala, latência, GPU, RPO/RTO ou segurança sem a evidência listada no TaskEnvelope.
