# ISSUE-0024 — Strong Geometric Verifier fail-closed para homografia projetiva, QualityProfiles e Image Deformation Profile

- **Tipo:** `Envelope de entrega do épico`
- **Status:** `planned`
- **Épico pai:** `EPIC-024`
- **Sprint:** `SPRINT-005`
- **Bounded Context owner:** `BC-007 — Verificação Geométrica e Qualidade`
- **Papel owner:** `Geoprocessamento`
- **Revisão arquitetural obrigatória:** `Arquiteto`
- **QA obrigatório:** `QA`
- **Final review obrigatório:** `Reviewer`

## História

Como equipe de entrega do DSGeorref, precisamos Strong Geometric Verifier fail-closed para homografia projetiva, QualityProfiles e Image Deformation Profile, para que a capacidade de produto vinculada seja entregue com qualidade verificável e integração controlada.

## Critérios de aceitação

- [ ] O resultado de produto de `EPIC-024` é demonstravelmente satisfeito.
- [ ] Contratos, ADRs e profiles aplicáveis são identificados antes da implementação.
- [ ] Os TaskEnvelopes do Tech Lead definem write scopes disjuntos e ordem de merge.
- [ ] Testes automatizados e evidências obrigatórias passam.
- [ ] QA registra aprovação independente no commit candidato.
- [ ] Reviewer registra aprovação final no mesmo commit.

## Dependências

- `EPIC-022`
- `EPIC-023`

## Escopo permitido de mudança

O envelope pai não autoriza código. Cada história filha possui TaskEnvelope com paths exatos e disjuntos.

## Condições de parada

- há decisão material de produto ou arquitetura não resolvida;
- o contrato obrigatório está ausente ou contraditório;
- o escopo da tarefa sobrepõe outra lane ativa;
- a aceitação não pode ser demonstrada por testes ou evidência.

## Histórias filhas


- `STORY-0136` / `ISSUE-0246` — `Arquiteto` — Definir contrato científico e invariantes: Strong Geometric Verifier fail-closed para homografia projetiva, QualityProfiles e Image Deformation Profile
- `STORY-0137` / `ISSUE-0247` — `Geoprocessamento` — Consolidar slices e liberar integração: Strong Geometric Verifier fail-closed para homografia projetiva, QualityProfiles e Image Deformation Profile
- `STORY-0138` / `ISSUE-0248` — `Geoprocessamento` — Implementar o núcleo algorítmico: Strong Geometric Verifier fail-closed para homografia projetiva, QualityProfiles e Image Deformation Profile
- `STORY-0139` / `ISSUE-0249` — `Geoprocessamento` — Integrar ao ProcessingPlan e pipeline: Strong Geometric Verifier fail-closed para homografia projetiva, QualityProfiles e Image Deformation Profile
- `STORY-0140` / `ISSUE-0250` — `Geoprocessamento` — Produzir métricas, diagnóstico e lineage: Strong Geometric Verifier fail-closed para homografia projetiva, QualityProfiles e Image Deformation Profile
- `STORY-0141` / `ISSUE-0251` — `QA` — Executar benchmark, negativos e regressão científica: Strong Geometric Verifier fail-closed para homografia projetiva, QualityProfiles e Image Deformation Profile
- `STORY-0142` / `ISSUE-0252` — `Reviewer` — Auditar evidência científica e final: Strong Geometric Verifier fail-closed para homografia projetiva, QualityProfiles e Image Deformation Profile
- `STORY-0729` / `ISSUE-0839` — `Geoprocessamento` — Slice 1/3 — Preparar corpus, fixtures e representação tipada: Strong Geometric Verifier fail-closed para homografia projetiva, QualityProfiles e Image Deformation Profile [REQ-AIE, REQ-ANC, REQ-CRS, REQ-EPIC]
- `STORY-0730` / `ISSUE-0840` — `Geoprocessamento` — Slice 2/3 — Preparar corpus, fixtures e representação tipada: Strong Geometric Verifier fail-closed para homografia projetiva, QualityProfiles e Image Deformation Profile [REQ-EST, REQ-FS1, REQ-MSK, REQ-QUAL, REQ-RAS, REQ-REF]
- `STORY-0731` / `ISSUE-0841` — `Geoprocessamento` — Slice 3/3 — Preparar corpus, fixtures e representação tipada: Strong Geometric Verifier fail-closed para homografia projetiva, QualityProfiles e Image Deformation Profile [REQ-RMV]

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
- **Critérios rastreados:** `AC-ISSUE-0024-01, AC-ISSUE-0024-02, AC-ISSUE-0024-03, AC-ISSUE-0024-04, AC-ISSUE-0024-05, AC-ISSUE-0024-06`
- **Requisitos do épico:** `43`
- **ADRs governantes:** `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-010`, `ADR-011`, `ADR-015`, `ADR-023`, `ADR-030`, `ADR-038`, `ADR-040`, `ADR-041`, `ADR-042`, `ADR-043`, `ADR-044`, `ADR-045`, `ADR-046`, `ADR-048`, `ADR-049`, `ADR-050`, `ADR-051`, `ADR-052`, `ADR-053`, `ADR-055`
- **Conflito:** `Nenhum`
- **Redundância funcional:** `Nenhuma`
- **Requisito faltante:** `Não`
- **Requisito impossível:** `Não`
- **Dependência circular:** `Não`
- **Matriz canônica:** `docs/07-assurance/ACCEPTANCE_CRITERION_TRACEABILITY.csv`


## Revisão de ADRs — Fase D

- **Resultado:** `PASS`
- **ADRs aplicáveis:** `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-010`, `ADR-011`, `ADR-015`, `ADR-023`, `ADR-030`, `ADR-038`, `ADR-040`, `ADR-041`, `ADR-042`, `ADR-043`, `ADR-044`, `ADR-045`, `ADR-046`, `ADR-048`, `ADR-049`, `ADR-050`, `ADR-051`, `ADR-052`, `ADR-053`, `ADR-055`
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
