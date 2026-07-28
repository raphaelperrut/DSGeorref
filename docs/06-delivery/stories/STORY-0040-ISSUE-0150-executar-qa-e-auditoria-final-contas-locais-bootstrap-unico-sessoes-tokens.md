# STORY-0040 / ISSUE-0150 — Executar QA e auditoria final: contas locais, bootstrap único, sessões, tokens e adapter OIDC

- **Tipo:** `História implementável`
- **Estado:** `Planned`
- **Épico pai:** `EPIC-008`
- **Sprint:** `SPRINT-002`
- **Domínio:** `PLT`
- **Bounded Context:** `BC-002 — Identidade e Controle de Acesso`
- **Papel executor:** `Reviewer`
- **TaskEnvelope:** `.codex/tasks/TASK-0040.json`

## História de usuário

Como administrador da instância, preciso executar qa e auditoria final para “contas locais, bootstrap único, sessões, tokens e adapter OIDC”, para que o resultado do épico seja implementável, verificável e integrável sem violar seus contratos.

## Resultado verificável

Executar QA e auditoria final para a capacidade **contas locais, bootstrap único, sessões, tokens e adapter OIDC**, com saída versionada, testes e evidência no commit candidato.

## Escopo

- `evidence/reviews/contas-locais-bootstrap-unico-sessoes-tokens-e-adapter/**`
## Fora de escopo

- Alterar ADR, contrato compartilhado ou regra de produto sem issue de decisão aprovada.
- Ampliar o escopo para outro épico ou introduzir dependência não declarada.
- Declarar gate aprovado sem evidência independente.

## Requisitos

Nenhum requisito exclusivo; valida integração do épico.

## ADRs e contratos

- `ADR-018`
- `ADR-028`
- `ADR-034`
- `contracts/README.md`

## Dependências


`STORY-0039`

## Critérios de aceitação

- [ ] O resultado de “contas locais, bootstrap único, sessões, tokens e adapter OIDC” é observável por contrato, interface, artifact ou evidência executável.
- [ ] Os requisitos vinculados possuem evidência explícita no commit candidato.
- [ ] Estados de erro e caminhos fail-closed aplicáveis são testados, sem fallback silencioso.
- [ ] QA e Reviewer referenciam o mesmo commit, evidências e riscos residuais; nenhuma aprovação é implícita.

## Testes obrigatórios

- `test_epic_008_aceite_happy_path`
- `test_epic_008_aceite_negative_paths`

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

Leia `AGENTS.md`, `.codex/roles/ROLE-011-reviewer.md`, este documento, o épico `EPIC-008` e o TaskEnvelope `TASK-0040`. Trabalhe somente nos paths permitidos. Implemente o menor incremento que satisfaça todos os critérios, execute os testes, registre evidências e interrompa quando qualquer condição de parada ocorrer.


## Revisão SAR

- **Estado arquitetural:** `RESOLVED`
- **Decisão tecnológica necessária antes de iniciar:** `Nenhuma`
- **Atributos de qualidade dominantes:** `consistência`, `completude`, `risco residual`
- **Autoridade de dados:** PostgreSQL/PostGIS para estado; filesystem gerenciado para binários publicados; broker/telemetria são derivados.
- **Contrato de entrada:** referências e schemas listados no TaskEnvelope.
- **Contrato de saída:** artifact, código, schema, teste ou evidência versionada no commit candidato.
- **Migration/rollback:** obrigatório quando a história altera schema, estado persistido, artifact ou deployment; caso contrário `não aplicável` deve ser justificado no handoff.
- **Observabilidade:** falhas e transições relevantes devem emitir signal/event/audit sem cardinalidade ilimitada.
- **Gate de completude:** nenhum heading obrigatório vazio, placeholder, ID obsoleto ou dependência implícita.

`EVIDENCE_BOUND` não representa decisão arquitetural em aberto: indica parâmetro quantitativo cujo valor é promovido pelo Benchmark Profile declarado.


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-002` — Identidade e Controle de Acesso.
- **Impacto no modelo:** `CROSS_CONTEXT_INTEGRATION`.
- **Upstreams permitidos:** `Nenhum`.
- **Regra de integração:** DTO, evento, port ou ACL publicado; entidade, repository, ORM model e state machine não atravessam o boundary.
- **Package de produção:** context-first conforme `DDD-090-CONTEXT-OWNERSHIP-AND-CODE-LAYOUT.md`.
- **Resultado:** `PASS`.

## Revisão de Requisitos — Fase B

- **Resultado:** `PASS`
- **Critérios rastreados:** `AC-ISSUE-0150-01, AC-ISSUE-0150-02, AC-ISSUE-0150-03, AC-ISSUE-0150-04`
- **Base de requisitos:** `DERIVED_CONTROL`
- **ADRs governantes:** `ADR-003`, `ADR-006`, `ADR-007`, `ADR-008`
- **Conflito:** `Nenhum`
- **Redundância funcional:** `Nenhuma`
- **Requisito faltante:** `Não`
- **Requisito impossível:** `Não`
- **Dependência circular:** `Não`
- **Matriz canônica:** `docs/07-assurance/ACCEPTANCE_CRITERION_TRACEABILITY.csv`


## Revisão de ADRs — Fase D

- **Resultado:** `PASS`
- **ADRs aplicáveis:** `ADR-003`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`
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
| Arquivos | 1 write scopes; deny scopes declarados | PASS |
| API | NOT_APPLICABLE | PASS |
| Banco | NOT_APPLICABLE | PASS |
| Frontend | NOT_APPLICABLE | PASS |
| Geo | NOT_APPLICABLE | PASS |
| IA | NOT_APPLICABLE | PASS |
| Testes | 2 testes obrigatórios | PASS |
| Artefatos | EVIDENCE_ONLY | PASS |
| Critérios | 4 critérios com IDs estáveis | PASS |
| Review | Reviewer; mesmo commit candidato | PASS |

- **Matriz canônica:** `docs/07-assurance/PHASE-F-ISSUE-DELIVERY-REVIEW.csv`
- **Relatório da sprint:** `docs/07-assurance/phase-f/SPRINT-002-REVIEW.md`
- **Baseline:** `SAR-v2.9-PHASE-F`
- **Resultado:** `PASS`
## CTO Review — Fase G

- **Resultado:** `PASS`
- **Risk tier:** `MEDIUM`
- **Controles aplicáveis:** `CTO-003, CTO-004, CTO-006, CTO-011, CTO-012, CTO-013, CTO-014, CTO-015`
- **Gate de produção:** `IMPLEMENTATION_AUTHORIZATION`
- **Regra:** implementação não pode publicar claim de custo, escala, latência, GPU, RPO/RTO ou segurança sem a evidência listada no TaskEnvelope.
