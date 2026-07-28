# ISSUE-0039 — instrumentação OpenTelemetry, correlation IDs, métricas, dashboards e alertas para API, RabbitMQ e workers

- **Tipo:** `Envelope de entrega do épico`
- **Status:** `planned`
- **Épico pai:** `EPIC-039`
- **Sprint:** `SPRINT-011`
- **Bounded Context owner:** `BC-014 — Operações, Auditoria e Suporte`
- **Papel owner:** `DevOps`
- **Revisão arquitetural obrigatória:** `Arquiteto`
- **QA obrigatório:** `QA`
- **Final review obrigatório:** `Reviewer`

## História

Como equipe de entrega do DSGeorref, precisamos instrumentação OpenTelemetry, correlation IDs, métricas, dashboards e alertas para API, RabbitMQ e workers, para que a capacidade de produto vinculada seja entregue com qualidade verificável e integração controlada.

## Critérios de aceitação

- [ ] O resultado de produto de `EPIC-039` é demonstravelmente satisfeito.
- [ ] Contratos, ADRs e profiles aplicáveis são identificados antes da implementação.
- [ ] Os TaskEnvelopes do Tech Lead definem write scopes disjuntos e ordem de merge.
- [ ] Testes automatizados e evidências obrigatórias passam.
- [ ] QA registra aprovação independente no commit candidato.
- [ ] Reviewer registra aprovação final no mesmo commit.

## Dependências

- `EPIC-005`
- `EPIC-015`

## Escopo permitido de mudança

O envelope pai não autoriza código. Cada história filha possui TaskEnvelope com paths exatos e disjuntos.

## Condições de parada

- há decisão material de produto ou arquitetura não resolvida;
- o contrato obrigatório está ausente ou contraditório;
- o escopo da tarefa sobrepõe outra lane ativa;
- a aceitação não pode ser demonstrada por testes ou evidência.

## Histórias filhas


- `STORY-0232` / `ISSUE-0342` — `DevOps` — Definir SLO, runbook e controles operacionais: instrumentação OpenTelemetry, correlation IDs, métricas, dashboards e alertas para API, RabbitMQ e workers
- `STORY-0233` / `ISSUE-0343` — `DevOps` — Consolidar slices e liberar integração: instrumentação OpenTelemetry, correlation IDs, métricas, dashboards e alertas para API, RabbitMQ e workers
- `STORY-0234` / `ISSUE-0344` — `DevOps` — Instrumentar sinais, dashboards e alertas: instrumentação OpenTelemetry, correlation IDs, métricas, dashboards e alertas para API, RabbitMQ e workers
- `STORY-0235` / `ISSUE-0345` — `QA` — Executar drills, fault injection e recuperação: instrumentação OpenTelemetry, correlation IDs, métricas, dashboards e alertas para API, RabbitMQ e workers
- `STORY-0236` / `ISSUE-0346` — `Security` — Validar acesso, redaction e exposição: instrumentação OpenTelemetry, correlation IDs, métricas, dashboards e alertas para API, RabbitMQ e workers
- `STORY-0237` / `ISSUE-0347` — `Reviewer` — Auditar evidência operacional final: instrumentação OpenTelemetry, correlation IDs, métricas, dashboards e alertas para API, RabbitMQ e workers
- `STORY-0745` / `ISSUE-0855` — `DevOps` — Slice 1/2 — Implementar automação operacional: instrumentação OpenTelemetry, correlation IDs, métricas, dashboards e alertas para API, RabbitMQ e workers [REQ-AIE, REQ-ARTLAYOUT]
- `STORY-0746` / `ISSUE-0856` — `DevOps` — Slice 2/2 — Implementar automação operacional: instrumentação OpenTelemetry, correlation IDs, métricas, dashboards e alertas para API, RabbitMQ e workers [REQ-ARTLAYOUT, REQ-MET, REQ-WORKER]

## Revisão SAR do envelope

- **Arquitetura aplicável:** contexto, ADRs, módulos, contratos e qualidade estão referenciados pela matriz de rastreabilidade.
- **Decisões tecnológicas em aberto:** nenhuma; parâmetro quantitativo somente pode permanecer evidence-bound com Benchmark Profile.
- **Contract freeze:** obrigatório antes de abrir implementações paralelas.
- **Consistência:** histórias filhas devem formar subgrafo acíclico, possuir TaskEnvelope válido e não colidir em write scope sem serialização explícita.
- **Critério de encerramento:** todas as histórias necessárias concluídas, evidência agregada, QA e Reviewer no mesmo commit candidato, riscos residuais registrados.


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-014` — Operações, Auditoria e Suporte.
- **Classificação:** `Generic`.
- **Integrações cross-context:** obedecem ao Context Map e exigem contrato publicado antes de lanes paralelas.
- **Modelo compartilhado:** proibido; somente primitivas técnicas sem semântica de domínio podem ser reutilizadas.
- **Resultado:** `PASS`.

## Revisão de Requisitos — Fase B

- **Resultado:** `PASS`
- **Critérios rastreados:** `AC-ISSUE-0039-01, AC-ISSUE-0039-02, AC-ISSUE-0039-03, AC-ISSUE-0039-04, AC-ISSUE-0039-05, AC-ISSUE-0039-06`
- **Requisitos do épico:** `31`
- **ADRs governantes:** `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-010`, `ADR-011`, `ADR-012`, `ADR-017`, `ADR-018`, `ADR-020`, `ADR-023`, `ADR-024`, `ADR-030`, `ADR-031`, `ADR-032`, `ADR-033`, `ADR-034`, `ADR-037`, `ADR-038`, `ADR-046`, `ADR-051`, `ADR-052`, `ADR-053`, `ADR-054`, `ADR-055`
- **Conflito:** `Nenhum`
- **Redundância funcional:** `Nenhuma`
- **Requisito faltante:** `Não`
- **Requisito impossível:** `Não`
- **Dependência circular:** `Não`
- **Matriz canônica:** `docs/07-assurance/ACCEPTANCE_CRITERION_TRACEABILITY.csv`


## Revisão de ADRs — Fase D

- **Resultado:** `PASS`
- **ADRs aplicáveis:** `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-010`, `ADR-011`, `ADR-012`, `ADR-017`, `ADR-018`, `ADR-020`, `ADR-023`, `ADR-024`, `ADR-030`, `ADR-031`, `ADR-032`, `ADR-033`, `ADR-034`, `ADR-037`, `ADR-038`, `ADR-046`, `ADR-051`, `ADR-052`, `ADR-053`, `ADR-054`, `ADR-055`
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
| Critérios | `32` critérios / `PASS` |
| Review | Arquiteto → QA → Reviewer / `PASS` |

- **Histórias filhas revisadas:** `8`
- **Matriz canônica:** `docs/07-assurance/PHASE-F-ISSUE-DELIVERY-REVIEW.csv`
- **Relatório da sprint:** `docs/07-assurance/phase-f/SPRINT-011-REVIEW.md`
- **Baseline:** `SAR-v2.9-PHASE-F`
- **Resultado:** `PASS`
## CTO Review — Fase G

- **Resultado:** `PASS`
- **Risk tier agregado:** `CRITICAL`
- **Histórias revisadas:** `8`
- **Controles aplicáveis:** `CTO-001, CTO-002, CTO-003, CTO-004, CTO-005, CTO-006, CTO-007, CTO-008, CTO-009, CTO-010, CTO-011, CTO-012, CTO-013, CTO-014, CTO-015`
- **Gate de produção:** `SECURITY_AND_PRIVACY_GATES`
