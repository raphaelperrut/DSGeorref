# ISSUE-0041 — threat model validado, scanning e testes ofensivos

- **Tipo:** `Envelope de entrega do épico`
- **Status:** `planned`
- **Épico pai:** `EPIC-041`
- **Sprint:** `SPRINT-002`
- **Bounded Context owner:** `BC-014 — Operações, Auditoria e Suporte`
- **Papel owner:** `Security`
- **Revisão arquitetural obrigatória:** `Arquiteto`
- **QA obrigatório:** `QA`
- **Final review obrigatório:** `Reviewer`

## História

Como equipe de entrega do DSGeorref, precisamos threat model validado, scanning e testes ofensivos, para que a capacidade de produto vinculada seja entregue com qualidade verificável e integração controlada.

## Critérios de aceitação

- [ ] O resultado de produto de `EPIC-041` é demonstravelmente satisfeito.
- [ ] Contratos, ADRs e profiles aplicáveis são identificados antes da implementação.
- [ ] Os TaskEnvelopes do Tech Lead definem write scopes disjuntos e ordem de merge.
- [ ] Testes automatizados e evidências obrigatórias passam.
- [ ] QA registra aprovação independente no commit candidato.
- [ ] Reviewer registra aprovação final no mesmo commit.

## Dependências

- `EPIC-012`
- `EPIC-027`

## Escopo permitido de mudança

O envelope pai não autoriza código. Cada história filha possui TaskEnvelope com paths exatos e disjuntos.

## Condições de parada

- há decisão material de produto ou arquitetura não resolvida;
- o contrato obrigatório está ausente ou contraditório;
- o escopo da tarefa sobrepõe outra lane ativa;
- a aceitação não pode ser demonstrada por testes ou evidência.

## Histórias filhas


- `STORY-0244` / `ISSUE-0354` — `Security` — Modelar ameaças e requisitos de controle: threat model validado, scanning e testes ofensivos
- `STORY-0245` / `ISSUE-0355` — `Arquiteto` — Consolidar slices e liberar integração: threat model validado, scanning e testes ofensivos
- `STORY-0246` / `ISSUE-0356` — `Backend` — Implementar controles e enforcement: threat model validado, scanning e testes ofensivos
- `STORY-0247` / `ISSUE-0357` — `Security` — Executar testes negativos e ofensivos: threat model validado, scanning e testes ofensivos
- `STORY-0248` / `ISSUE-0358` — `DevOps` — Instrumentar detecção, resposta e runbook: threat model validado, scanning e testes ofensivos
- `STORY-0249` / `ISSUE-0359` — `Reviewer` — Auditar evidência de segurança final: threat model validado, scanning e testes ofensivos
- `STORY-0747` / `ISSUE-0857` — `Arquiteto` — Slice 1/3 — Definir políticas e contratos fail-closed: threat model validado, scanning e testes ofensivos [REQ-AIE]
- `STORY-0748` / `ISSUE-0858` — `Arquiteto` — Slice 2/3 — Definir políticas e contratos fail-closed: threat model validado, scanning e testes ofensivos [REQ-ARTLAYOUT, REQ-AUTH-IMPL]
- `STORY-0749` / `ISSUE-0859` — `Arquiteto` — Slice 3/3 — Definir políticas e contratos fail-closed: threat model validado, scanning e testes ofensivos [REQ-AUTH-IMPL, REQ-EPIC, REQ-FS, REQ-SRC]

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
- **Critérios rastreados:** `AC-ISSUE-0041-01, AC-ISSUE-0041-02, AC-ISSUE-0041-03, AC-ISSUE-0041-04, AC-ISSUE-0041-05, AC-ISSUE-0041-06`
- **Requisitos do épico:** `26`
- **ADRs governantes:** `ADR-002`, `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-014`, `ADR-016`, `ADR-023`, `ADR-028`, `ADR-029`, `ADR-030`, `ADR-031`, `ADR-032`, `ADR-033`, `ADR-034`, `ADR-038`, `ADR-046`, `ADR-047`, `ADR-051`, `ADR-052`, `ADR-053`, `ADR-055`
- **Conflito:** `Nenhum`
- **Redundância funcional:** `Nenhuma`
- **Requisito faltante:** `Não`
- **Requisito impossível:** `Não`
- **Dependência circular:** `Não`
- **Matriz canônica:** `docs/07-assurance/ACCEPTANCE_CRITERION_TRACEABILITY.csv`


## Revisão de ADRs — Fase D

- **Resultado:** `PASS`
- **ADRs aplicáveis:** `ADR-002`, `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-014`, `ADR-016`, `ADR-023`, `ADR-028`, `ADR-029`, `ADR-030`, `ADR-031`, `ADR-032`, `ADR-033`, `ADR-034`, `ADR-038`, `ADR-046`, `ADR-047`, `ADR-051`, `ADR-052`, `ADR-053`, `ADR-055`
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
| API | `NOT_APPLICABLE` / `PASS` |
| Banco | `APPLICABLE` / `PASS` |
| Frontend | `NOT_APPLICABLE` / `PASS` |
| Geo | `NOT_APPLICABLE` / `PASS` |
| IA | `APPLICABLE` / `PASS` |
| Testes | `PASS` |
| Artefatos | `PRODUCT_AND_EVIDENCE` / `PASS` |
| Critérios | `36` critérios / `PASS` |
| Review | Arquiteto → QA → Reviewer / `PASS` |

- **Histórias filhas revisadas:** `9`
- **Matriz canônica:** `docs/07-assurance/PHASE-F-ISSUE-DELIVERY-REVIEW.csv`
- **Relatório da sprint:** `docs/07-assurance/phase-f/SPRINT-002-REVIEW.md`
- **Baseline:** `SAR-v2.9-PHASE-F`
- **Resultado:** `PASS`
## CTO Review — Fase G

- **Resultado:** `PASS`
- **Risk tier agregado:** `CRITICAL`
- **Histórias revisadas:** `9`
- **Controles aplicáveis:** `CTO-001, CTO-002, CTO-003, CTO-004, CTO-005, CTO-006, CTO-007, CTO-008, CTO-009, CTO-010, CTO-011, CTO-012, CTO-013, CTO-014, CTO-015`
- **Gate de produção:** `SECURITY_AND_PRIVACY_GATES`
