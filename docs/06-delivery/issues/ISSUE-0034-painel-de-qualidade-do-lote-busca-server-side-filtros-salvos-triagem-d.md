# ISSUE-0034 — painel de qualidade do lote, busca server-side, filtros salvos, triagem, deformação e retry/revisão de subconjuntos

- **Tipo:** `Envelope de entrega do épico`
- **Status:** `planned`
- **Épico pai:** `EPIC-034`
- **Sprint:** `SPRINT-009`
- **Bounded Context owner:** `BC-016 — Experiência e Orientação do Operador`
- **Papel owner:** `Frontend`
- **Revisão arquitetural obrigatória:** `Arquiteto`
- **QA obrigatório:** `QA`
- **Final review obrigatório:** `Reviewer`

## História

Como equipe de entrega do DSGeorref, precisamos painel de qualidade do lote, busca server-side, filtros salvos, triagem, deformação e retry/revisão de subconjuntos, para que a capacidade de produto vinculada seja entregue com qualidade verificável e integração controlada.

## Critérios de aceitação

- [ ] O resultado de produto de `EPIC-034` é demonstravelmente satisfeito.
- [ ] Contratos, ADRs e profiles aplicáveis são identificados antes da implementação.
- [ ] Os TaskEnvelopes do Tech Lead definem write scopes disjuntos e ordem de merge.
- [ ] Testes automatizados e evidências obrigatórias passam.
- [ ] QA registra aprovação independente no commit candidato.
- [ ] Reviewer registra aprovação final no mesmo commit.

## Dependências

- `EPIC-032`
- `EPIC-030`
- `EPIC-018`

## Escopo permitido de mudança

O envelope pai não autoriza código. Cada história filha possui TaskEnvelope com paths exatos e disjuntos.

## Condições de parada

- há decisão material de produto ou arquitetura não resolvida;
- o contrato obrigatório está ausente ou contraditório;
- o escopo da tarefa sobrepõe outra lane ativa;
- a aceitação não pode ser demonstrada por testes ou evidência.

## Histórias filhas


- `STORY-0203` / `ISSUE-0313` — `Product Owner` — Definir jornada, estados e acessibilidade: painel de qualidade do lote, busca server-side, filtros salvos, triagem, deformação e retry/revisão de subconjuntos
- `STORY-0204` / `ISSUE-0314` — `Frontend` — Consolidar slices e liberar integração: painel de qualidade do lote, busca server-side, filtros salvos, triagem, deformação e retry/revisão de subconjuntos
- `STORY-0205` / `ISSUE-0315` — `Frontend` — Implementar componentes e interação: painel de qualidade do lote, busca server-side, filtros salvos, triagem, deformação e retry/revisão de subconjuntos
- `STORY-0206` / `ISSUE-0316` — `Frontend` — Integrar mapa, fluxo e estados de erro: painel de qualidade do lote, busca server-side, filtros salvos, triagem, deformação e retry/revisão de subconjuntos
- `STORY-0207` / `ISSUE-0317` — `QA` — Executar testes de componente, acessibilidade e E2E: painel de qualidade do lote, busca server-side, filtros salvos, triagem, deformação e retry/revisão de subconjuntos
- `STORY-0208` / `ISSUE-0318` — `Reviewer` — Auditar UX, contrato e evidência final: painel de qualidade do lote, busca server-side, filtros salvos, triagem, deformação e retry/revisão de subconjuntos
- `STORY-0741` / `ISSUE-0851` — `Frontend` — Slice 1/2 — Integrar contratos e cliente tipado: painel de qualidade do lote, busca server-side, filtros salvos, triagem, deformação e retry/revisão de subconjuntos [REQ-BAT, REQ-BEX]
- `STORY-0742` / `ISSUE-0852` — `Frontend` — Slice 2/2 — Integrar contratos e cliente tipado: painel de qualidade do lote, busca server-side, filtros salvos, triagem, deformação e retry/revisão de subconjuntos [REQ-EPIC, REQ-QUAL, REQ-SCL, REQ-SMO]

## Revisão SAR do envelope

- **Arquitetura aplicável:** contexto, ADRs, módulos, contratos e qualidade estão referenciados pela matriz de rastreabilidade.
- **Decisões tecnológicas em aberto:** nenhuma; parâmetro quantitativo somente pode permanecer evidence-bound com Benchmark Profile.
- **Contract freeze:** obrigatório antes de abrir implementações paralelas.
- **Consistência:** histórias filhas devem formar subgrafo acíclico, possuir TaskEnvelope válido e não colidir em write scope sem serialização explícita.
- **Critério de encerramento:** todas as histórias necessárias concluídas, evidência agregada, QA e Reviewer no mesmo commit candidato, riscos residuais registrados.


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-016` — Experiência e Orientação do Operador.
- **Classificação:** `Supporting`.
- **Integrações cross-context:** obedecem ao Context Map e exigem contrato publicado antes de lanes paralelas.
- **Modelo compartilhado:** proibido; somente primitivas técnicas sem semântica de domínio podem ser reutilizadas.
- **Resultado:** `PASS`.

## Revisão de Requisitos — Fase B

- **Resultado:** `PASS`
- **Critérios rastreados:** `AC-ISSUE-0034-01, AC-ISSUE-0034-02, AC-ISSUE-0034-03, AC-ISSUE-0034-04, AC-ISSUE-0034-05, AC-ISSUE-0034-06`
- **Requisitos do épico:** `21`
- **ADRs governantes:** `ADR-002`, `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-012`, `ADR-014`, `ADR-025`, `ADR-030`, `ADR-037`, `ADR-038`, `ADR-039`, `ADR-040`, `ADR-046`, `ADR-053`
- **Conflito:** `Nenhum`
- **Redundância funcional:** `Nenhuma`
- **Requisito faltante:** `Não`
- **Requisito impossível:** `Não`
- **Dependência circular:** `Não`
- **Matriz canônica:** `docs/07-assurance/ACCEPTANCE_CRITERION_TRACEABILITY.csv`


## Revisão de ADRs — Fase D

- **Resultado:** `PASS`
- **ADRs aplicáveis:** `ADR-002`, `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-012`, `ADR-014`, `ADR-025`, `ADR-030`, `ADR-037`, `ADR-038`, `ADR-039`, `ADR-040`, `ADR-046`, `ADR-053`
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
| Frontend | `APPLICABLE` / `PASS` |
| Geo | `NOT_APPLICABLE` / `PASS` |
| IA | `APPLICABLE` / `PASS` |
| Testes | `PASS` |
| Artefatos | `PRODUCT_AND_EVIDENCE` / `PASS` |
| Critérios | `32` critérios / `PASS` |
| Review | Arquiteto → QA → Reviewer / `PASS` |

- **Histórias filhas revisadas:** `8`
- **Matriz canônica:** `docs/07-assurance/PHASE-F-ISSUE-DELIVERY-REVIEW.csv`
- **Relatório da sprint:** `docs/07-assurance/phase-f/SPRINT-009-REVIEW.md`
- **Baseline:** `SAR-v2.9-PHASE-F`
- **Resultado:** `PASS`
## CTO Review — Fase G

- **Resultado:** `PASS`
- **Risk tier agregado:** `CRITICAL`
- **Histórias revisadas:** `8`
- **Controles aplicáveis:** `CTO-001, CTO-003, CTO-004, CTO-005, CTO-006, CTO-007, CTO-008, CTO-009, CTO-010, CTO-011, CTO-012, CTO-013, CTO-014, CTO-015`
- **Gate de produção:** `SECURITY_AND_PRIVACY_GATES`
