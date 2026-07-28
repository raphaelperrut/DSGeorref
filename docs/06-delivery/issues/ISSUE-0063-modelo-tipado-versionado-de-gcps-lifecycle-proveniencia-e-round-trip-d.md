# ISSUE-0063 — modelo tipado/versionado de GCPs, lifecycle, proveniência e round-trip dos exports

- **Tipo:** `Envelope de entrega do épico`
- **Status:** `planned`
- **Épico pai:** `EPIC-063`
- **Sprint:** `SPRINT-006`
- **Bounded Context owner:** `BC-011 — Revisão e Correção`
- **Papel owner:** `Geoprocessamento`
- **Revisão arquitetural obrigatória:** `Arquiteto`
- **QA obrigatório:** `QA`
- **Final review obrigatório:** `Reviewer`

## História

Como equipe de entrega do DSGeorref, precisamos modelo tipado/versionado de GCPs, lifecycle, proveniência e round-trip dos exports, para que a capacidade de produto vinculada seja entregue com qualidade verificável e integração controlada.

## Critérios de aceitação

- [ ] O resultado de produto de `EPIC-063` é demonstravelmente satisfeito.
- [ ] Contratos, ADRs e profiles aplicáveis são identificados antes da implementação.
- [ ] Os TaskEnvelopes do Tech Lead definem write scopes disjuntos e ordem de merge.
- [ ] Testes automatizados e evidências obrigatórias passam.
- [ ] QA registra aprovação independente no commit candidato.
- [ ] Reviewer registra aprovação final no mesmo commit.

## Dependências

- `EPIC-052`
- `EPIC-012`
- `EPIC-049`
- `EPIC-037`

## Escopo permitido de mudança

O envelope pai não autoriza código. Cada história filha possui TaskEnvelope com paths exatos e disjuntos.

## Condições de parada

- há decisão material de produto ou arquitetura não resolvida;
- o contrato obrigatório está ausente ou contraditório;
- o escopo da tarefa sobrepõe outra lane ativa;
- a aceitação não pode ser demonstrada por testes ou evidência.

## Histórias filhas


- `STORY-0391` / `ISSUE-0501` — `Arquiteto` — Definir contrato científico e invariantes: modelo tipado/versionado de GCPs, lifecycle, proveniência e round-trip dos exports
- `STORY-0392` / `ISSUE-0502` — `Geoprocessamento` — Preparar corpus, fixtures e representação tipada: modelo tipado/versionado de GCPs, lifecycle, proveniência e round-trip dos exports
- `STORY-0393` / `ISSUE-0503` — `Geoprocessamento` — Implementar o núcleo algorítmico: modelo tipado/versionado de GCPs, lifecycle, proveniência e round-trip dos exports
- `STORY-0394` / `ISSUE-0504` — `Geoprocessamento` — Integrar ao ProcessingPlan e pipeline: modelo tipado/versionado de GCPs, lifecycle, proveniência e round-trip dos exports
- `STORY-0395` / `ISSUE-0505` — `Geoprocessamento` — Produzir métricas, diagnóstico e lineage: modelo tipado/versionado de GCPs, lifecycle, proveniência e round-trip dos exports
- `STORY-0396` / `ISSUE-0506` — `QA` — Executar benchmark, negativos e regressão científica: modelo tipado/versionado de GCPs, lifecycle, proveniência e round-trip dos exports
- `STORY-0397` / `ISSUE-0507` — `Reviewer` — Auditar evidência científica e final: modelo tipado/versionado de GCPs, lifecycle, proveniência e round-trip dos exports

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
- **Critérios rastreados:** `AC-ISSUE-0063-01, AC-ISSUE-0063-02, AC-ISSUE-0063-03, AC-ISSUE-0063-04, AC-ISSUE-0063-05, AC-ISSUE-0063-06`
- **Requisitos do épico:** `2`
- **ADRs governantes:** `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-041`, `ADR-042`, `ADR-043`, `ADR-048`
- **Conflito:** `Nenhum`
- **Redundância funcional:** `Nenhuma`
- **Requisito faltante:** `Não`
- **Requisito impossível:** `Não`
- **Dependência circular:** `Não`
- **Matriz canônica:** `docs/07-assurance/ACCEPTANCE_CRITERION_TRACEABILITY.csv`


## Revisão de ADRs — Fase D

- **Resultado:** `PASS`
- **ADRs aplicáveis:** `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-041`, `ADR-042`, `ADR-043`, `ADR-048`
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
- **Relatório da sprint:** `docs/07-assurance/phase-f/SPRINT-006-REVIEW.md`
- **Baseline:** `SAR-v2.9-PHASE-F`
- **Resultado:** `PASS`
## CTO Review — Fase G

- **Resultado:** `PASS`
- **Risk tier agregado:** `HIGH`
- **Histórias revisadas:** `7`
- **Controles aplicáveis:** `CTO-001, CTO-003, CTO-004, CTO-005, CTO-006, CTO-007, CTO-008, CTO-010, CTO-011, CTO-012, CTO-013, CTO-014, CTO-015`
- **Gate de produção:** `BENCHMARK_AND_OPERATIONS_GATES`
