# ISSUE-0065 — taxonomia de retry técnico, orçamento, backoff, idempotência e PlanVariants algorítmicos

- **Tipo:** `Envelope de entrega do épico`
- **Status:** `planned`
- **Épico pai:** `EPIC-065`
- **Sprint:** `SPRINT-004`
- **Bounded Context owner:** `BC-010 — Orquestração de Jobs e Recursos`
- **Papel owner:** `Backend`
- **Revisão arquitetural obrigatória:** `Arquiteto`
- **QA obrigatório:** `QA`
- **Final review obrigatório:** `Reviewer`

## História

Como equipe de entrega do DSGeorref, precisamos taxonomia de retry técnico, orçamento, backoff, idempotência e PlanVariants algorítmicos, para que a capacidade de produto vinculada seja entregue com qualidade verificável e integração controlada.

## Critérios de aceitação

- [ ] O resultado de produto de `EPIC-065` é demonstravelmente satisfeito.
- [ ] Contratos, ADRs e profiles aplicáveis são identificados antes da implementação.
- [ ] Os TaskEnvelopes do Tech Lead definem write scopes disjuntos e ordem de merge.
- [ ] Testes automatizados e evidências obrigatórias passam.
- [ ] QA registra aprovação independente no commit candidato.
- [ ] Reviewer registra aprovação final no mesmo commit.

## Dependências

- `EPIC-014`
- `EPIC-015`
- `EPIC-030`

## Escopo permitido de mudança

O envelope pai não autoriza código. Cada história filha possui TaskEnvelope com paths exatos e disjuntos.

## Condições de parada

- há decisão material de produto ou arquitetura não resolvida;
- o contrato obrigatório está ausente ou contraditório;
- o escopo da tarefa sobrepõe outra lane ativa;
- a aceitação não pode ser demonstrada por testes ou evidência.

## Histórias filhas


- `STORY-0404` / `ISSUE-0514` — `Arquiteto` — Definir estados, envelopes e invariantes: taxonomia de retry técnico, orçamento, backoff, idempotência e PlanVariants algorítmicos
- `STORY-0405` / `ISSUE-0515` — `Backend` — Implementar modelo e application services: taxonomia de retry técnico, orçamento, backoff, idempotência e PlanVariants algorítmicos
- `STORY-0406` / `ISSUE-0516` — `Backend` — Implementar runner, worker ou scheduler: taxonomia de retry técnico, orçamento, backoff, idempotência e PlanVariants algorítmicos
- `STORY-0407` / `ISSUE-0517` — `Backend` — Expor comandos, progresso e reconciliação: taxonomia de retry técnico, orçamento, backoff, idempotência e PlanVariants algorítmicos
- `STORY-0408` / `ISSUE-0518` — `DevOps` — Automatizar testes de resiliência, retry e recuperação: taxonomia de retry técnico, orçamento, backoff, idempotência e PlanVariants algorítmicos
- `STORY-0409` / `ISSUE-0519` — `QA` — Executar integração real, carga e fault injection: taxonomia de retry técnico, orçamento, backoff, idempotência e PlanVariants algorítmicos
- `STORY-0410` / `ISSUE-0520` — `Reviewer` — Auditar evidência e integração final: taxonomia de retry técnico, orçamento, backoff, idempotência e PlanVariants algorítmicos

## Revisão SAR do envelope

- **Arquitetura aplicável:** contexto, ADRs, módulos, contratos e qualidade estão referenciados pela matriz de rastreabilidade.
- **Decisões tecnológicas em aberto:** nenhuma; parâmetro quantitativo somente pode permanecer evidence-bound com Benchmark Profile.
- **Contract freeze:** obrigatório antes de abrir implementações paralelas.
- **Consistência:** histórias filhas devem formar subgrafo acíclico, possuir TaskEnvelope válido e não colidir em write scope sem serialização explícita.
- **Critério de encerramento:** todas as histórias necessárias concluídas, evidência agregada, QA e Reviewer no mesmo commit candidato, riscos residuais registrados.


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-010` — Orquestração de Jobs e Recursos.
- **Classificação:** `Supporting`.
- **Integrações cross-context:** obedecem ao Context Map e exigem contrato publicado antes de lanes paralelas.
- **Modelo compartilhado:** proibido; somente primitivas técnicas sem semântica de domínio podem ser reutilizadas.
- **Resultado:** `PASS`.

## Revisão de Requisitos — Fase B

- **Resultado:** `PASS`
- **Critérios rastreados:** `AC-ISSUE-0065-01, AC-ISSUE-0065-02, AC-ISSUE-0065-03, AC-ISSUE-0065-04, AC-ISSUE-0065-05, AC-ISSUE-0065-06`
- **Requisitos do épico:** `10`
- **ADRs governantes:** `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-010`, `ADR-011`, `ADR-012`, `ADR-016`, `ADR-033`, `ADR-034`, `ADR-037`, `ADR-038`, `ADR-039`, `ADR-040`, `ADR-046`
- **Conflito:** `Nenhum`
- **Redundância funcional:** `Nenhuma`
- **Requisito faltante:** `Não`
- **Requisito impossível:** `Não`
- **Dependência circular:** `Não`
- **Matriz canônica:** `docs/07-assurance/ACCEPTANCE_CRITERION_TRACEABILITY.csv`


## Revisão de ADRs — Fase D

- **Resultado:** `PASS`
- **ADRs aplicáveis:** `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-010`, `ADR-011`, `ADR-012`, `ADR-016`, `ADR-033`, `ADR-034`, `ADR-037`, `ADR-038`, `ADR-039`, `ADR-040`, `ADR-046`
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
| Banco | `APPLICABLE` / `PASS` |
| Frontend | `NOT_APPLICABLE` / `PASS` |
| Geo | `NOT_APPLICABLE` / `PASS` |
| IA | `NOT_APPLICABLE` / `PASS` |
| Testes | `PASS` |
| Artefatos | `EVIDENCE_ONLY` / `PASS` |
| Critérios | `28` critérios / `PASS` |
| Review | Arquiteto → QA → Reviewer / `PASS` |

- **Histórias filhas revisadas:** `7`
- **Matriz canônica:** `docs/07-assurance/PHASE-F-ISSUE-DELIVERY-REVIEW.csv`
- **Relatório da sprint:** `docs/07-assurance/phase-f/SPRINT-004-REVIEW.md`
- **Baseline:** `SAR-v2.9-PHASE-F`
- **Resultado:** `PASS`
## CTO Review — Fase G

- **Resultado:** `PASS`
- **Risk tier agregado:** `CRITICAL`
- **Histórias revisadas:** `7`
- **Controles aplicáveis:** `CTO-001, CTO-002, CTO-003, CTO-004, CTO-005, CTO-006, CTO-008, CTO-009, CTO-010, CTO-011, CTO-012, CTO-013, CTO-014, CTO-015`
- **Gate de produção:** `SECURITY_AND_PRIVACY_GATES`
