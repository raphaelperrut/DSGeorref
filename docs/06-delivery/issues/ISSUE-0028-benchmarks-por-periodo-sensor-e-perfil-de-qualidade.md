# ISSUE-0028 — benchmarks por período, sensor e perfil de qualidade

- **Tipo:** `Envelope de entrega do épico`
- **Status:** `planned`
- **Épico pai:** `EPIC-028`
- **Sprint:** `SPRINT-005`
- **Bounded Context owner:** `BC-007 — Verificação Geométrica e Qualidade`
- **Papel owner:** `Geoprocessamento`
- **Revisão arquitetural obrigatória:** `Arquiteto`
- **QA obrigatório:** `QA`
- **Final review obrigatório:** `Reviewer`

## História

Como equipe de entrega do DSGeorref, precisamos benchmarks por período, sensor e perfil de qualidade, para que a capacidade de produto vinculada seja entregue com qualidade verificável e integração controlada.

## Critérios de aceitação

- [ ] O resultado de produto de `EPIC-028` é demonstravelmente satisfeito.
- [ ] Contratos, ADRs e profiles aplicáveis são identificados antes da implementação.
- [ ] Os TaskEnvelopes do Tech Lead definem write scopes disjuntos e ordem de merge.
- [ ] Testes automatizados e evidências obrigatórias passam.
- [ ] QA registra aprovação independente no commit candidato.
- [ ] Reviewer registra aprovação final no mesmo commit.

## Dependências

- `EPIC-024`

## Escopo permitido de mudança

O envelope pai não autoriza código. Cada história filha possui TaskEnvelope com paths exatos e disjuntos.

## Condições de parada

- há decisão material de produto ou arquitetura não resolvida;
- o contrato obrigatório está ausente ou contraditório;
- o escopo da tarefa sobrepõe outra lane ativa;
- a aceitação não pode ser demonstrada por testes ou evidência.

## Histórias filhas


- `STORY-0164` / `ISSUE-0274` — `Arquiteto` — Definir contrato científico e invariantes: benchmarks por período, sensor e perfil de qualidade
- `STORY-0165` / `ISSUE-0275` — `Geoprocessamento` — Consolidar slices e liberar integração: benchmarks por período, sensor e perfil de qualidade
- `STORY-0166` / `ISSUE-0276` — `Geoprocessamento` — Implementar o núcleo algorítmico: benchmarks por período, sensor e perfil de qualidade
- `STORY-0167` / `ISSUE-0277` — `Geoprocessamento` — Integrar ao ProcessingPlan e pipeline: benchmarks por período, sensor e perfil de qualidade
- `STORY-0168` / `ISSUE-0278` — `Geoprocessamento` — Produzir métricas, diagnóstico e lineage: benchmarks por período, sensor e perfil de qualidade
- `STORY-0169` / `ISSUE-0279` — `QA` — Executar benchmark, negativos e regressão científica: benchmarks por período, sensor e perfil de qualidade
- `STORY-0170` / `ISSUE-0280` — `Reviewer` — Auditar evidência científica e final: benchmarks por período, sensor e perfil de qualidade
- `STORY-0735` / `ISSUE-0845` — `Geoprocessamento` — Slice 1/3 — Preparar corpus, fixtures e representação tipada: benchmarks por período, sensor e perfil de qualidade [REQ-AI, REQ-AIE, REQ-CLASSICPROFILE]
- `STORY-0736` / `ISSUE-0846` — `Geoprocessamento` — Slice 2/3 — Preparar corpus, fixtures e representação tipada: benchmarks por período, sensor e perfil de qualidade [REQ-CLASSICPROFILE, REQ-SCP, REQ-SDR, REQ-SGVCAL]
- `STORY-0737` / `ISSUE-0847` — `Geoprocessamento` — Slice 3/3 — Preparar corpus, fixtures e representação tipada: benchmarks por período, sensor e perfil de qualidade [REQ-SGVCAL, REQ-SRG, REQ-TOOL, REQ-TST]

## Revisão SAR do envelope

- **Arquitetura aplicável:** contexto, ADRs, módulos, contratos e qualidade estão referenciados pela matriz de rastreabilidade.
- **Decisões tecnológicas em aberto:** nenhuma; parâmetro quantitativo somente pode permanecer evidence-bound com Benchmark Profile.
- **Contract freeze:** obrigatório antes de abrir implementações paralelas.
- **Consistência:** histórias filhas devem formar subgrafo acíclico, possuir TaskEnvelope válido e não colidir em write scope sem serialização explícita.
- **Critério de encerramento:** todas as histórias necessárias concluídas, evidência agregada, QA e Reviewer no mesmo commit candidato, riscos residuais registrados.


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-007` — Verificação Geométrica e Qualidade.
- **Classificação:** `Core`.
- **Integrações cross-context:** obedecem ao Context Map e exigem contrato publicado antes de lanes paralelas.
- **Modelo compartilhado:** proibido; somente primitivas técnicas sem semântica de domínio podem ser reutilizadas.
- **Resultado:** `PASS`.

## Revisão de Requisitos — Fase B

- **Resultado:** `PASS`
- **Critérios rastreados:** `AC-ISSUE-0028-01, AC-ISSUE-0028-02, AC-ISSUE-0028-03, AC-ISSUE-0028-04, AC-ISSUE-0028-05, AC-ISSUE-0028-06`
- **Requisitos do épico:** `42`
- **ADRs governantes:** `ADR-002`, `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-010`, `ADR-011`, `ADR-018`, `ADR-025`, `ADR-030`, `ADR-038`, `ADR-039`, `ADR-041`, `ADR-042`, `ADR-043`, `ADR-044`, `ADR-045`, `ADR-046`, `ADR-051`, `ADR-052`, `ADR-053`
- **Conflito:** `Nenhum`
- **Redundância funcional:** `Nenhuma`
- **Requisito faltante:** `Não`
- **Requisito impossível:** `Não`
- **Dependência circular:** `Não`
- **Matriz canônica:** `docs/07-assurance/ACCEPTANCE_CRITERION_TRACEABILITY.csv`


## Revisão de ADRs — Fase D

- **Resultado:** `PASS`
- **ADRs aplicáveis:** `ADR-002`, `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-010`, `ADR-011`, `ADR-018`, `ADR-025`, `ADR-030`, `ADR-038`, `ADR-039`, `ADR-041`, `ADR-042`, `ADR-043`, `ADR-044`, `ADR-045`, `ADR-046`, `ADR-051`, `ADR-052`, `ADR-053`
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
| IA | `APPLICABLE` / `PASS` |
| Testes | `PASS` |
| Artefatos | `PRODUCT_AND_EVIDENCE` / `PASS` |
| Critérios | `40` critérios / `PASS` |
| Review | Arquiteto → QA → Reviewer / `PASS` |

- **Histórias filhas revisadas:** `10`
- **Matriz canônica:** `docs/07-assurance/PHASE-F-ISSUE-DELIVERY-REVIEW.csv`
- **Relatório da sprint:** `docs/07-assurance/phase-f/SPRINT-005-REVIEW.md`
- **Baseline:** `SAR-v2.9-PHASE-F`
- **Resultado:** `PASS`
## CTO Review — Fase G

- **Resultado:** `PASS`
- **Risk tier agregado:** `CRITICAL`
- **Histórias revisadas:** `10`
- **Controles aplicáveis:** `CTO-001, CTO-003, CTO-004, CTO-005, CTO-006, CTO-007, CTO-008, CTO-009, CTO-010, CTO-011, CTO-012, CTO-013, CTO-014, CTO-015`
- **Gate de produção:** `SECURITY_AND_PRIVACY_GATES`
