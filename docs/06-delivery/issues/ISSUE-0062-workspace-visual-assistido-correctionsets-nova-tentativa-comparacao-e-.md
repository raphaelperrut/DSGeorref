# ISSUE-0062 — workspace visual assistido, CorrectionSets, nova tentativa, comparação e auditoria sem bloquear o ciclo automático

- **Tipo:** `Envelope de entrega do épico`
- **Status:** `planned`
- **Épico pai:** `EPIC-062`
- **Sprint:** `SPRINT-009`
- **Bounded Context owner:** `BC-011 — Revisão e Correção`
- **Papel owner:** `Frontend`
- **Revisão arquitetural obrigatória:** `Arquiteto`
- **QA obrigatório:** `QA`
- **Final review obrigatório:** `Reviewer`

## História

Como equipe de entrega do DSGeorref, precisamos workspace visual assistido, CorrectionSets, nova tentativa, comparação e auditoria sem bloquear o ciclo automático, para que a capacidade de produto vinculada seja entregue com qualidade verificável e integração controlada.

## Critérios de aceitação

- [ ] O resultado de produto de `EPIC-062` é demonstravelmente satisfeito.
- [ ] Contratos, ADRs e profiles aplicáveis são identificados antes da implementação.
- [ ] Os TaskEnvelopes do Tech Lead definem write scopes disjuntos e ordem de merge.
- [ ] Testes automatizados e evidências obrigatórias passam.
- [ ] QA registra aprovação independente no commit candidato.
- [ ] Reviewer registra aprovação final no mesmo commit.

## Dependências

- `EPIC-032`
- `EPIC-034`
- `EPIC-024`
- `EPIC-035`
- `EPIC-049`

## Escopo permitido de mudança

O envelope pai não autoriza código. Cada história filha possui TaskEnvelope com paths exatos e disjuntos.

## Condições de parada

- há decisão material de produto ou arquitetura não resolvida;
- o contrato obrigatório está ausente ou contraditório;
- o escopo da tarefa sobrepõe outra lane ativa;
- a aceitação não pode ser demonstrada por testes ou evidência.

## Histórias filhas


- `STORY-0385` / `ISSUE-0495` — `Product Owner` — Definir fluxo de revisão e decisões permitidas: workspace visual assistido, CorrectionSets, nova tentativa, comparação e auditoria sem bloquear o ciclo automático
- `STORY-0386` / `ISSUE-0496` — `Arquiteto` — Definir contratos de correção e nova tentativa: workspace visual assistido, CorrectionSets, nova tentativa, comparação e auditoria sem bloquear o ciclo automático
- `STORY-0387` / `ISSUE-0497` — `Frontend` — Implementar workspace e comparação: workspace visual assistido, CorrectionSets, nova tentativa, comparação e auditoria sem bloquear o ciclo automático
- `STORY-0388` / `ISSUE-0498` — `Backend` — Implementar lifecycle e auditoria: workspace visual assistido, CorrectionSets, nova tentativa, comparação e auditoria sem bloquear o ciclo automático
- `STORY-0389` / `ISSUE-0499` — `QA` — Executar testes de revisão, hard gates e concorrência: workspace visual assistido, CorrectionSets, nova tentativa, comparação e auditoria sem bloquear o ciclo automático
- `STORY-0390` / `ISSUE-0500` — `Reviewer` — Auditar rastreabilidade e evidência final: workspace visual assistido, CorrectionSets, nova tentativa, comparação e auditoria sem bloquear o ciclo automático

## Revisão SAR do envelope

- **Arquitetura aplicável:** contexto, ADRs, módulos, contratos e qualidade estão referenciados pela matriz de rastreabilidade.
- **Decisões tecnológicas em aberto:** nenhuma; parâmetro quantitativo somente pode permanecer evidence-bound com Benchmark Profile.
- **Contract freeze:** obrigatório antes de abrir implementações paralelas.
- **Consistência:** histórias filhas devem formar subgrafo acíclico, possuir TaskEnvelope válido e não colidir em write scope sem serialização explícita.
- **Critério de encerramento:** todas as histórias necessárias concluídas, evidência agregada, QA e Reviewer no mesmo commit candidato, riscos residuais registrados.


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-011` — Revisão e Correção.
- **Classificação:** `Supporting`.
- **Integrações cross-context:** obedecem ao Context Map e exigem contrato publicado antes de lanes paralelas.
- **Modelo compartilhado:** proibido; somente primitivas técnicas sem semântica de domínio podem ser reutilizadas.
- **Resultado:** `PASS`.

## Revisão de Requisitos — Fase B

- **Resultado:** `PASS`
- **Critérios rastreados:** `AC-ISSUE-0062-01, AC-ISSUE-0062-02, AC-ISSUE-0062-03, AC-ISSUE-0062-04, AC-ISSUE-0062-05, AC-ISSUE-0062-06`
- **Requisitos do épico:** `3`
- **ADRs governantes:** `ADR-002`, `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-014`, `ADR-016`, `ADR-048`
- **Conflito:** `Nenhum`
- **Redundância funcional:** `Nenhuma`
- **Requisito faltante:** `Não`
- **Requisito impossível:** `Não`
- **Dependência circular:** `Não`
- **Matriz canônica:** `docs/07-assurance/ACCEPTANCE_CRITERION_TRACEABILITY.csv`


## Revisão de ADRs — Fase D

- **Resultado:** `PASS`
- **ADRs aplicáveis:** `ADR-002`, `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-014`, `ADR-016`, `ADR-048`
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
| Frontend | `APPLICABLE` / `PASS` |
| Geo | `NOT_APPLICABLE` / `PASS` |
| IA | `NOT_APPLICABLE` / `PASS` |
| Testes | `PASS` |
| Artefatos | `EVIDENCE_ONLY` / `PASS` |
| Critérios | `24` critérios / `PASS` |
| Review | Arquiteto → QA → Reviewer / `PASS` |

- **Histórias filhas revisadas:** `6`
- **Matriz canônica:** `docs/07-assurance/PHASE-F-ISSUE-DELIVERY-REVIEW.csv`
- **Relatório da sprint:** `docs/07-assurance/phase-f/SPRINT-009-REVIEW.md`
- **Baseline:** `SAR-v2.9-PHASE-F`
- **Resultado:** `PASS`
## CTO Review — Fase G

- **Resultado:** `PASS`
- **Risk tier agregado:** `HIGH`
- **Histórias revisadas:** `6`
- **Controles aplicáveis:** `CTO-001, CTO-002, CTO-003, CTO-004, CTO-005, CTO-006, CTO-008, CTO-010, CTO-011, CTO-012, CTO-013, CTO-014, CTO-015`
- **Gate de produção:** `BENCHMARK_AND_OPERATIONS_GATES`
