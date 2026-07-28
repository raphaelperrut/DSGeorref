# STORY-0189 / ISSUE-0299 — Executar testes de componente, acessibilidade e E2E: React/TypeScript/Vite, design system, cliente OpenAPI, seletor visual, acessibilidade e E2E

- **Tipo:** `História implementável`
- **Estado:** `Planned`
- **Épico pai:** `EPIC-031`
- **Sprint:** `SPRINT-009`
- **Domínio:** `WEB`
- **Bounded Context:** `BC-016 — Experiência e Orientação do Operador`
- **Papel executor:** `QA`
- **TaskEnvelope:** `.codex/tasks/TASK-0189.json`

## História de usuário

Como operador geoespacial, preciso executar testes de componente, acessibilidade e e2e para “React/TypeScript/Vite, design system, cliente OpenAPI, seletor visual, acessibilidade e E2E”, para que o resultado do épico seja implementável, verificável e integrável sem violar seus contratos.

## Resultado verificável

Executar testes de componente, acessibilidade e E2E para a capacidade **React/TypeScript/Vite, design system, cliente OpenAPI, seletor visual, acessibilidade e E2E**, com saída versionada, testes e evidência no commit candidato.

## Escopo

- `tests/web/react-typescript-vite-design-system-cliente-openapi-se/**`
- `tools/quality/contexts/operator_experience/react-typescript-vite-design-system-cliente-openapi-se/**`
- `.github/workflows/react-typescript-vite-design-system-cliente-openapi-se.yaml`
## Fora de escopo

- Alterar ADR, contrato compartilhado ou regra de produto sem issue de decisão aprovada.
- Ampliar o escopo para outro épico ou introduzir dependência não declarada.
- Declarar gate aprovado sem evidência independente.

## Requisitos

`REQ-FS1-005`, `REQ-FS1-007`

## ADRs e contratos

- `ADR-002`
- `contracts/README.md`

## Dependências


`STORY-0186`, `STORY-0187`, `STORY-0188`

## Critérios de aceitação

- [ ] O resultado de “React/TypeScript/Vite, design system, cliente OpenAPI, seletor visual, acessibilidade e E2E” é observável por contrato, interface, artifact ou evidência executável.
- [ ] Os requisitos REQ-FS1-005, REQ-FS1-007 possuem evidência explícita no commit candidato.
- [ ] Estados de erro e caminhos fail-closed aplicáveis são testados, sem fallback silencioso.
- [ ] Testes reais e fault injection cobrem o caminho feliz e falhas críticas.

## Testes obrigatórios

- `test_first_functional_slice_decision_05`
- `test_first_functional_slice_decision_07`
- `test_epic_031_validacao_happy_path`
- `test_epic_031_validacao_negative_paths`

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

Leia `AGENTS.md`, `.codex/roles/ROLE-008-qa.md`, este documento, o épico `EPIC-031` e o TaskEnvelope `TASK-0189`. Trabalhe somente nos paths permitidos. Implemente o menor incremento que satisfaça todos os critérios, execute os testes, registre evidências e interrompa quando qualquer condição de parada ocorrer.


## Revisão SAR

- **Estado arquitetural:** `RESOLVED`
- **Decisão tecnológica necessária antes de iniciar:** `Nenhuma`
- **Atributos de qualidade dominantes:** `testabilidade`, `confiabilidade`, `regressão`
- **Autoridade de dados:** PostgreSQL/PostGIS para estado; filesystem gerenciado para binários publicados; broker/telemetria são derivados.
- **Contrato de entrada:** referências e schemas listados no TaskEnvelope.
- **Contrato de saída:** artifact, código, schema, teste ou evidência versionada no commit candidato.
- **Migration/rollback:** obrigatório quando a história altera schema, estado persistido, artifact ou deployment; caso contrário `não aplicável` deve ser justificado no handoff.
- **Observabilidade:** falhas e transições relevantes devem emitir signal/event/audit sem cardinalidade ilimitada.
- **Gate de completude:** nenhum heading obrigatório vazio, placeholder, ID obsoleto ou dependência implícita.

`EVIDENCE_BOUND` não representa decisão arquitetural em aberto: indica parâmetro quantitativo cujo valor é promovido pelo Benchmark Profile declarado.


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-016` — Experiência e Orientação do Operador.
- **Impacto no modelo:** `CROSS_CONTEXT_INTEGRATION`.
- **Upstreams permitidos:** `BC-002, BC-003, BC-012, BC-013, BC-014`.
- **Regra de integração:** DTO, evento, port ou ACL publicado; entidade, repository, ORM model e state machine não atravessam o boundary.
- **Package de produção:** context-first conforme `DDD-090-CONTEXT-OWNERSHIP-AND-CODE-LAYOUT.md`.
- **Resultado:** `PASS`.

## Revisão de Requisitos — Fase B

- **Resultado:** `PASS`
- **Critérios rastreados:** `AC-ISSUE-0299-01, AC-ISSUE-0299-02, AC-ISSUE-0299-03, AC-ISSUE-0299-04`
- **Base de requisitos:** `MIXED`
- **ADRs governantes:** `ADR-003`, `ADR-004`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-046`, `ADR-055`
- **Conflito:** `Nenhum`
- **Redundância funcional:** `Nenhuma`
- **Requisito faltante:** `Não`
- **Requisito impossível:** `Não`
- **Dependência circular:** `Não`
- **Matriz canônica:** `docs/07-assurance/ACCEPTANCE_CRITERION_TRACEABILITY.csv`


## Revisão de ADRs — Fase D

- **Resultado:** `PASS`
- **ADRs aplicáveis:** `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-013`, `ADR-014`, `ADR-015`, `ADR-046`, `ADR-055`
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
| Arquivos | 3 write scopes; deny scopes declarados | PASS |
| API | APPLICABLE | PASS |
| Banco | NOT_APPLICABLE | PASS |
| Frontend | APPLICABLE | PASS |
| Geo | NOT_APPLICABLE | PASS |
| IA | NOT_APPLICABLE | PASS |
| Testes | 4 testes obrigatórios | PASS |
| Artefatos | EVIDENCE_ONLY | PASS |
| Critérios | 4 critérios com IDs estáveis | PASS |
| Review | QA, Reviewer; mesmo commit candidato | PASS |

- **Matriz canônica:** `docs/07-assurance/PHASE-F-ISSUE-DELIVERY-REVIEW.csv`
- **Relatório da sprint:** `docs/07-assurance/phase-f/SPRINT-009-REVIEW.md`
- **Baseline:** `SAR-v2.9-PHASE-F`
- **Resultado:** `PASS`
## CTO Review — Fase G

- **Resultado:** `PASS`
- **Risk tier:** `CRITICAL`
- **Controles aplicáveis:** `CTO-001, CTO-003, CTO-004, CTO-005, CTO-006, CTO-008, CTO-011, CTO-012, CTO-013, CTO-014, CTO-015`
- **Gate de produção:** `SECURITY_AND_PRIVACY_GATES`
- **Regra:** implementação não pode publicar claim de custo, escala, latência, GPU, RPO/RTO ou segurança sem a evidência listada no TaskEnvelope.
