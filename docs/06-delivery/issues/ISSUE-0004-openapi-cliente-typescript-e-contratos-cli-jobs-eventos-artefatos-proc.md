# ISSUE-0004 — OpenAPI, cliente TypeScript e contratos CLI/jobs/eventos/artefatos/ProcessingPlan/QualityReport/FailureDiagnostic versionados

- **Tipo:** `Envelope de entrega do épico`
- **Status:** `planned`
- **Épico pai:** `EPIC-004`
- **Sprint:** `SPRINT-001`
- **Bounded Context owner:** `BC-001 — Governança de Engenharia e Entrega`
- **Papel owner:** `Tech Lead`
- **Revisão arquitetural obrigatória:** `Arquiteto`
- **QA obrigatório:** `QA`
- **Final review obrigatório:** `Reviewer`

## História

Como equipe de entrega do DSGeorref, precisamos OpenAPI, cliente TypeScript e contratos CLI/jobs/eventos/artefatos/ProcessingPlan/QualityReport/FailureDiagnostic versionados, para que a capacidade de produto vinculada seja entregue com qualidade verificável e integração controlada.

## Critérios de aceitação

- [ ] O resultado de produto de `EPIC-004` é demonstravelmente satisfeito.
- [ ] Contratos, ADRs e profiles aplicáveis são identificados antes da implementação.
- [ ] Os TaskEnvelopes do Tech Lead definem write scopes disjuntos e ordem de merge.
- [ ] Testes automatizados e evidências obrigatórias passam.
- [ ] QA registra aprovação independente no commit candidato.
- [ ] Reviewer registra aprovação final no mesmo commit.

## Dependências

- `EPIC-003`

## Escopo permitido de mudança

O envelope pai não autoriza código. Cada história filha possui TaskEnvelope com paths exatos e disjuntos.

## Condições de parada

- há decisão material de produto ou arquitetura não resolvida;
- o contrato obrigatório está ausente ou contraditório;
- o escopo da tarefa sobrepõe outra lane ativa;
- a aceitação não pode ser demonstrada por testes ou evidência.

## Histórias filhas


- `STORY-0016` / `ISSUE-0126` — `Arquiteto` — Consolidar slices e liberar integração: OpenAPI, cliente TypeScript e contratos CLI/jobs/eventos/artefatos/ProcessingPlan/QualityReport/FailureDiagnostic versionados
- `STORY-0017` / `ISSUE-0127` — `Tech Lead` — Consolidar slices e liberar integração: OpenAPI, cliente TypeScript e contratos CLI/jobs/eventos/artefatos/ProcessingPlan/QualityReport/FailureDiagnostic versionados
- `STORY-0018` / `ISSUE-0128` — `DevOps` — Automatizar validações e controles: OpenAPI, cliente TypeScript e contratos CLI/jobs/eventos/artefatos/ProcessingPlan/QualityReport/FailureDiagnostic versionados
- `STORY-0019` / `ISSUE-0129` — `Tech Lead` — Integrar a capacidade ao fluxo do repositório: OpenAPI, cliente TypeScript e contratos CLI/jobs/eventos/artefatos/ProcessingPlan/QualityReport/FailureDiagnostic versionados
- `STORY-0020` / `ISSUE-0130` — `Reviewer` — Validar evidência e realizar auditoria final: OpenAPI, cliente TypeScript e contratos CLI/jobs/eventos/artefatos/ProcessingPlan/QualityReport/FailureDiagnostic versionados
- `STORY-0701` / `ISSUE-0811` — `Arquiteto` — Slice 1/2 — Definir escopo, contratos e invariantes: OpenAPI, cliente TypeScript e contratos CLI/jobs/eventos/artefatos/ProcessingPlan/QualityReport/FailureDiagnostic versionados [REQ-CRS, REQ-DBSCHEMA, REQ-EPIC, REQ-FS1, REQ-RUN]
- `STORY-0702` / `ISSUE-0812` — `Arquiteto` — Slice 2/2 — Definir escopo, contratos e invariantes: OpenAPI, cliente TypeScript e contratos CLI/jobs/eventos/artefatos/ProcessingPlan/QualityReport/FailureDiagnostic versionados [REQ-RUNTIME, REQ-SCM, REQ-TOOL, REQ-TOP, REQ-UX]
- `STORY-0703` / `ISSUE-0813` — `Tech Lead` — Slice 1/3 — Materializar a fundação executável: OpenAPI, cliente TypeScript e contratos CLI/jobs/eventos/artefatos/ProcessingPlan/QualityReport/FailureDiagnostic versionados [REQ-ARTLAYOUT, REQ-DBSCHEMA, REQ-FS1]
- `STORY-0704` / `ISSUE-0814` — `Tech Lead` — Slice 2/3 — Materializar a fundação executável: OpenAPI, cliente TypeScript e contratos CLI/jobs/eventos/artefatos/ProcessingPlan/QualityReport/FailureDiagnostic versionados [REQ-RUN, REQ-RUNTIME]
- `STORY-0705` / `ISSUE-0815` — `Tech Lead` — Slice 3/3 — Materializar a fundação executável: OpenAPI, cliente TypeScript e contratos CLI/jobs/eventos/artefatos/ProcessingPlan/QualityReport/FailureDiagnostic versionados [REQ-RUNTIME, REQ-TOOL, REQ-UPG]

## Revisão SAR do envelope

- **Arquitetura aplicável:** contexto, ADRs, módulos, contratos e qualidade estão referenciados pela matriz de rastreabilidade.
- **Decisões tecnológicas em aberto:** nenhuma; parâmetro quantitativo somente pode permanecer evidence-bound com Benchmark Profile.
- **Contract freeze:** obrigatório antes de abrir implementações paralelas.
- **Consistência:** histórias filhas devem formar subgrafo acíclico, possuir TaskEnvelope válido e não colidir em write scope sem serialização explícita.
- **Critério de encerramento:** todas as histórias necessárias concluídas, evidência agregada, QA e Reviewer no mesmo commit candidato, riscos residuais registrados.

## Contract freeze completo

- [ ] As 56 operações possuem request/response específicos, permissão, idempotência, erros e exemplos.
- [ ] `CommandRequest` e `ResourceEnvelope` não existem no OpenAPI.
- [ ] Cliente TypeScript e contract tests serão gerados do digest congelado.


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-001` — Governança de Engenharia e Entrega.
- **Classificação:** `Enabling`.
- **Integrações cross-context:** obedecem ao Context Map e exigem contrato publicado antes de lanes paralelas.
- **Modelo compartilhado:** proibido; somente primitivas técnicas sem semântica de domínio podem ser reutilizadas.
- **Resultado:** `PASS`.

## Revisão de Requisitos — Fase B

- **Resultado:** `PASS`
- **Critérios rastreados:** `AC-ISSUE-0004-01, AC-ISSUE-0004-02, AC-ISSUE-0004-03, AC-ISSUE-0004-04, AC-ISSUE-0004-05, AC-ISSUE-0004-06`
- **Requisitos do épico:** `40`
- **ADRs governantes:** `ADR-001`, `ADR-002`, `ADR-003`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-010`, `ADR-011`, `ADR-013`, `ADR-014`, `ADR-015`, `ADR-017`, `ADR-019`, `ADR-021`, `ADR-023`, `ADR-033`, `ADR-034`, `ADR-035`, `ADR-040`, `ADR-041`, `ADR-044`, `ADR-045`, `ADR-046`, `ADR-053`, `ADR-055`
- **Conflito:** `Nenhum`
- **Redundância funcional:** `Nenhuma`
- **Requisito faltante:** `Não`
- **Requisito impossível:** `Não`
- **Dependência circular:** `Não`
- **Matriz canônica:** `docs/07-assurance/ACCEPTANCE_CRITERION_TRACEABILITY.csv`


## Revisão de ADRs — Fase D

- **Resultado:** `PASS`
- **ADRs aplicáveis:** `ADR-001`, `ADR-002`, `ADR-003`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-010`, `ADR-011`, `ADR-013`, `ADR-014`, `ADR-015`, `ADR-017`, `ADR-019`, `ADR-021`, `ADR-023`, `ADR-033`, `ADR-034`, `ADR-035`, `ADR-040`, `ADR-041`, `ADR-044`, `ADR-045`, `ADR-046`, `ADR-053`, `ADR-055`
- **Conflito ou sobreposição:** `Nenhum`
- **Decisão em aberto:** `Nenhuma`


## Specification Review — Fase E

- **Especificações aplicáveis:** `SPEC-001`, `SPEC-004`
- **Status:** `PASS`

## Sprint Review — Fase F

| Dimensão | Resultado do envelope |
|---|---|
| Dependências | `PASS` |
| Arquivos e write scopes | `PASS` |
| API | `APPLICABLE` / `PASS` |
| Banco | `NOT_APPLICABLE` / `PASS` |
| Frontend | `NOT_APPLICABLE` / `PASS` |
| Geo | `NOT_APPLICABLE` / `PASS` |
| IA | `APPLICABLE` / `PASS` |
| Testes | `PASS` |
| Artefatos | `PRODUCT_AND_EVIDENCE` / `PASS` |
| Critérios | `40` critérios / `PASS` |
| Review | Arquiteto → QA → Reviewer / `PASS` |

- **Histórias filhas revisadas:** `10`
- **Matriz canônica:** `docs/07-assurance/PHASE-F-ISSUE-DELIVERY-REVIEW.csv`
- **Relatório da sprint:** `docs/07-assurance/phase-f/SPRINT-001-REVIEW.md`
- **Baseline:** `SAR-v2.9-PHASE-F`
- **Resultado:** `PASS`
## CTO Review — Fase G

- **Resultado:** `PASS`
- **Risk tier agregado:** `CRITICAL`
- **Histórias revisadas:** `10`
- **Controles aplicáveis:** `CTO-001, CTO-002, CTO-003, CTO-004, CTO-005, CTO-006, CTO-007, CTO-008, CTO-009, CTO-010, CTO-011, CTO-012, CTO-013, CTO-014, CTO-015`
- **Gate de produção:** `SECURITY_AND_PRIVACY_GATES`
