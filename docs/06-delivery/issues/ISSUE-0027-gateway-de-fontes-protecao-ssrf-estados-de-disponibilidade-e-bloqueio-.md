# ISSUE-0027 — gateway de fontes, proteção SSRF, estados de disponibilidade e bloqueio de compra

- **Tipo:** `Envelope de entrega do épico`
- **Status:** `planned`
- **Épico pai:** `EPIC-027`
- **Sprint:** `SPRINT-005`
- **Bounded Context owner:** `BC-005 — Descoberta e Aquisição de Referências`
- **Papel owner:** `Geoprocessamento`
- **Revisão arquitetural obrigatória:** `Arquiteto`
- **QA obrigatório:** `QA`
- **Final review obrigatório:** `Reviewer`

## História

Como equipe de entrega do DSGeorref, precisamos gateway de fontes, proteção SSRF, estados de disponibilidade e bloqueio de compra, para que a capacidade de produto vinculada seja entregue com qualidade verificável e integração controlada.

## Critérios de aceitação

- [ ] O resultado de produto de `EPIC-027` é demonstravelmente satisfeito.
- [ ] Contratos, ADRs e profiles aplicáveis são identificados antes da implementação.
- [ ] Os TaskEnvelopes do Tech Lead definem write scopes disjuntos e ordem de merge.
- [ ] Testes automatizados e evidências obrigatórias passam.
- [ ] QA registra aprovação independente no commit candidato.
- [ ] Reviewer registra aprovação final no mesmo commit.

## Dependências

- `EPIC-005`

## Escopo permitido de mudança

O envelope pai não autoriza código. Cada história filha possui TaskEnvelope com paths exatos e disjuntos.

## Condições de parada

- há decisão material de produto ou arquitetura não resolvida;
- o contrato obrigatório está ausente ou contraditório;
- o escopo da tarefa sobrepõe outra lane ativa;
- a aceitação não pode ser demonstrada por testes ou evidência.

## Histórias filhas


- `STORY-0157` / `ISSUE-0267` — `Arquiteto` — Definir contrato científico e invariantes: gateway de fontes, proteção SSRF, estados de disponibilidade e bloqueio de compra
- `STORY-0158` / `ISSUE-0268` — `Geoprocessamento` — Preparar corpus, fixtures e representação tipada: gateway de fontes, proteção SSRF, estados de disponibilidade e bloqueio de compra
- `STORY-0159` / `ISSUE-0269` — `Geoprocessamento` — Implementar o núcleo algorítmico: gateway de fontes, proteção SSRF, estados de disponibilidade e bloqueio de compra
- `STORY-0160` / `ISSUE-0270` — `Geoprocessamento` — Integrar ao ProcessingPlan e pipeline: gateway de fontes, proteção SSRF, estados de disponibilidade e bloqueio de compra
- `STORY-0161` / `ISSUE-0271` — `Geoprocessamento` — Produzir métricas, diagnóstico e lineage: gateway de fontes, proteção SSRF, estados de disponibilidade e bloqueio de compra
- `STORY-0162` / `ISSUE-0272` — `QA` — Executar benchmark, negativos e regressão científica: gateway de fontes, proteção SSRF, estados de disponibilidade e bloqueio de compra
- `STORY-0163` / `ISSUE-0273` — `Reviewer` — Auditar evidência científica e final: gateway de fontes, proteção SSRF, estados de disponibilidade e bloqueio de compra

## Revisão SAR do envelope

- **Arquitetura aplicável:** contexto, ADRs, módulos, contratos e qualidade estão referenciados pela matriz de rastreabilidade.
- **Decisões tecnológicas em aberto:** nenhuma; parâmetro quantitativo somente pode permanecer evidence-bound com Benchmark Profile.
- **Contract freeze:** obrigatório antes de abrir implementações paralelas.
- **Consistência:** histórias filhas devem formar subgrafo acíclico, possuir TaskEnvelope válido e não colidir em write scope sem serialização explícita.
- **Critério de encerramento:** todas as histórias necessárias concluídas, evidência agregada, QA e Reviewer no mesmo commit candidato, riscos residuais registrados.


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-005` — Descoberta e Aquisição de Referências.
- **Classificação:** `Supporting`.
- **Integrações cross-context:** obedecem ao Context Map e exigem contrato publicado antes de lanes paralelas.
- **Modelo compartilhado:** proibido; somente primitivas técnicas sem semântica de domínio podem ser reutilizadas.
- **Resultado:** `PASS`.

## Revisão de Requisitos — Fase B

- **Resultado:** `PASS`
- **Critérios rastreados:** `AC-ISSUE-0027-01, AC-ISSUE-0027-02, AC-ISSUE-0027-03, AC-ISSUE-0027-04, AC-ISSUE-0027-05, AC-ISSUE-0027-06`
- **Requisitos do épico:** `2`
- **ADRs governantes:** `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-041`, `ADR-042`, `ADR-043`, `ADR-047`
- **Conflito:** `Nenhum`
- **Redundância funcional:** `Nenhuma`
- **Requisito faltante:** `Não`
- **Requisito impossível:** `Não`
- **Dependência circular:** `Não`
- **Matriz canônica:** `docs/07-assurance/ACCEPTANCE_CRITERION_TRACEABILITY.csv`


## Revisão de ADRs — Fase D

- **Resultado:** `PASS`
- **ADRs aplicáveis:** `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-041`, `ADR-042`, `ADR-043`, `ADR-047`
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
| Geo | `APPLICABLE` / `PASS` |
| IA | `NOT_APPLICABLE` / `PASS` |
| Testes | `PASS` |
| Artefatos | `PRODUCT_AND_EVIDENCE` / `PASS` |
| Critérios | `28` critérios / `PASS` |
| Review | Arquiteto → QA → Reviewer / `PASS` |

- **Histórias filhas revisadas:** `7`
- **Matriz canônica:** `docs/07-assurance/PHASE-F-ISSUE-DELIVERY-REVIEW.csv`
- **Relatório da sprint:** `docs/07-assurance/phase-f/SPRINT-005-REVIEW.md`
- **Baseline:** `SAR-v2.9-PHASE-F`
- **Resultado:** `PASS`
## CTO Review — Fase G

- **Resultado:** `PASS`
- **Risk tier agregado:** `HIGH`
- **Histórias revisadas:** `7`
- **Controles aplicáveis:** `CTO-001, CTO-003, CTO-004, CTO-005, CTO-006, CTO-007, CTO-008, CTO-010, CTO-011, CTO-012, CTO-013, CTO-014, CTO-015`
- **Gate de produção:** `BENCHMARK_AND_OPERATIONS_GATES`
