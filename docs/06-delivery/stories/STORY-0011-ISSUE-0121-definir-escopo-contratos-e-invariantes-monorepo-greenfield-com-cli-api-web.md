# STORY-0011 / ISSUE-0121 — Definir escopo, contratos e invariantes: monorepo greenfield com CLI/API/Web mínimos e checks reproduzíveis

- **Tipo:** `História implementável`
- **Estado:** `Planned`
- **Épico pai:** `EPIC-003`
- **Sprint:** `SPRINT-001`
- **Domínio:** `FND`
- **Bounded Context:** `BC-001 — Governança de Engenharia e Entrega`
- **Papel executor:** `Arquiteto`
- **TaskEnvelope:** `.codex/tasks/TASK-0011.json`

## História de usuário

Como mantenedor de engenharia, preciso definir escopo, contratos e invariantes para “monorepo greenfield com CLI/API/Web mínimos e checks reproduzíveis”, para que o resultado do épico seja implementável, verificável e integrável sem violar seus contratos.

## Resultado verificável

Definir escopo, contratos e invariantes para a capacidade **monorepo greenfield com CLI/API/Web mínimos e checks reproduzíveis**, com saída versionada, testes e evidência no commit candidato.

## Escopo

- `contracts/contexts/engineering_governance/fnd/monorepo-greenfield-com-cli-api-web-minimos-e-checks-r/**`
- `docs/02-architecture/design-reviews/monorepo-greenfield-com-cli-api-web-minimos-e-checks-r/**`
## Fora de escopo

- Alterar ADR, contrato compartilhado ou regra de produto sem issue de decisão aprovada.
- Ampliar o escopo para outro épico ou introduzir dependência não declarada.
- Declarar gate aprovado sem evidência independente.

## Requisitos

`REQ-TOP-001`

## ADRs e contratos

- `ADR-002`
- `contracts/README.md`
- `contracts/http/openapi.yaml`

## Dependências


`STORY-0005`

## Critérios de aceitação

- [ ] O resultado de “monorepo greenfield com CLI/API/Web mínimos e checks reproduzíveis” é observável por contrato, interface, artifact ou evidência executável.
- [ ] Os requisitos REQ-TOP-001 possuem evidência explícita no commit candidato.
- [ ] Estados de erro e caminhos fail-closed aplicáveis são testados, sem fallback silencioso.
- [ ] Schemas, estados, compatibilidade e autoridade de dados estão versionados e revisados pelo Arquiteto.

## Testes obrigatórios

- `cli_api_semantic_contract`
- `test_epic_003_contrato`

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

Leia `AGENTS.md`, `.codex/roles/ROLE-002-arquiteto.md`, este documento, o épico `EPIC-003` e o TaskEnvelope `TASK-0011`. Trabalhe somente nos paths permitidos. Implemente o menor incremento que satisfaça todos os critérios, execute os testes, registre evidências e interrompa quando qualquer condição de parada ocorrer.


## Revisão SAR

- **Estado arquitetural:** `RESOLVED`
- **Decisão tecnológica necessária antes de iniciar:** `Nenhuma`
- **Atributos de qualidade dominantes:** `modificabilidade`, `compatibilidade`, `integridade`
- **Autoridade de dados:** PostgreSQL/PostGIS para estado; filesystem gerenciado para binários publicados; broker/telemetria são derivados.
- **Contrato de entrada:** referências e schemas listados no TaskEnvelope.
- **Contrato de saída:** artifact, código, schema, teste ou evidência versionada no commit candidato.
- **Migration/rollback:** obrigatório quando a história altera schema, estado persistido, artifact ou deployment; caso contrário `não aplicável` deve ser justificado no handoff.
- **Observabilidade:** falhas e transições relevantes devem emitir signal/event/audit sem cardinalidade ilimitada.
- **Gate de completude:** nenhum heading obrigatório vazio, placeholder, ID obsoleto ou dependência implícita.

`EVIDENCE_BOUND` não representa decisão arquitetural em aberto: indica parâmetro quantitativo cujo valor é promovido pelo Benchmark Profile declarado.


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-001` — Governança de Engenharia e Entrega.
- **Impacto no modelo:** `PUBLIC_CONTRACT`.
- **Upstreams permitidos:** `Nenhum`.
- **Regra de integração:** DTO, evento, port ou ACL publicado; entidade, repository, ORM model e state machine não atravessam o boundary.
- **Package de produção:** context-first conforme `DDD-090-CONTEXT-OWNERSHIP-AND-CODE-LAYOUT.md`.
- **Resultado:** `PASS`.

## Revisão de Requisitos — Fase B

- **Resultado:** `PASS`
- **Critérios rastreados:** `AC-ISSUE-0121-01, AC-ISSUE-0121-02, AC-ISSUE-0121-03, AC-ISSUE-0121-04`
- **Base de requisitos:** `MIXED`
- **ADRs governantes:** `ADR-003`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-014`
- **Conflito:** `Nenhum`
- **Redundância funcional:** `Nenhuma`
- **Requisito faltante:** `Não`
- **Requisito impossível:** `Não`
- **Dependência circular:** `Não`
- **Matriz canônica:** `docs/07-assurance/ACCEPTANCE_CRITERION_TRACEABILITY.csv`


## Revisão de ADRs — Fase D

- **Resultado:** `PASS`
- **ADRs aplicáveis:** `ADR-003`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-014`
- **Decisão em aberto:** `Nenhuma`
- **Regra:** implementar somente os boundaries listados; divergência ou lacuna interrompe a tarefa.


## Specification Review — Fase E

- **Especificações aplicáveis:** `SPEC-001`, `SPEC-004`
- **Status:** `PASS`
- A história deve parar se texto, schema, exemplo ou versão aplicável estiver ausente ou contraditório.

## Sprint Review — Fase F

| Dimensão | Aplicabilidade | Resultado |
|---|---|---|
| Dependências | 1 predecessores explícitos | PASS |
| Arquivos | 2 write scopes; deny scopes declarados | PASS |
| API | APPLICABLE | PASS |
| Banco | NOT_APPLICABLE | PASS |
| Frontend | NOT_APPLICABLE | PASS |
| Geo | NOT_APPLICABLE | PASS |
| IA | NOT_APPLICABLE | PASS |
| Testes | 2 testes obrigatórios | PASS |
| Artefatos | EVIDENCE_ONLY | PASS |
| Critérios | 4 critérios com IDs estáveis | PASS |
| Review | Arquiteto, Reviewer; mesmo commit candidato | PASS |

- **Matriz canônica:** `docs/07-assurance/PHASE-F-ISSUE-DELIVERY-REVIEW.csv`
- **Relatório da sprint:** `docs/07-assurance/phase-f/SPRINT-001-REVIEW.md`
- **Baseline:** `SAR-v2.9-PHASE-F`
- **Resultado:** `PASS`
## CTO Review — Fase G

- **Resultado:** `PASS`
- **Risk tier:** `HIGH`
- **Controles aplicáveis:** `CTO-001, CTO-003, CTO-004, CTO-005, CTO-006, CTO-008, CTO-011, CTO-012, CTO-013, CTO-014, CTO-015`
- **Gate de produção:** `BENCHMARK_AND_OPERATIONS_GATES`
- **Regra:** implementação não pode publicar claim de custo, escala, latência, GPU, RPO/RTO ou segurança sem a evidência listada no TaskEnvelope.
