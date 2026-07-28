# ISSUE-0031 — React/TypeScript/Vite, design system, cliente OpenAPI, seletor visual, acessibilidade e E2E

- **Tipo:** `Envelope de entrega do épico`
- **Status:** `planned`
- **Épico pai:** `EPIC-031`
- **Sprint:** `SPRINT-009`
- **Bounded Context owner:** `BC-016 — Experiência e Orientação do Operador`
- **Papel owner:** `Frontend`
- **Revisão arquitetural obrigatória:** `Arquiteto`
- **QA obrigatório:** `QA`
- **Final review obrigatório:** `Reviewer`

## História

Como equipe de entrega do DSGeorref, precisamos React/TypeScript/Vite, design system, cliente OpenAPI, seletor visual, acessibilidade e E2E, para que a capacidade de produto vinculada seja entregue com qualidade verificável e integração controlada.

## Critérios de aceitação

- [ ] O resultado de produto de `EPIC-031` é demonstravelmente satisfeito.
- [ ] Contratos, ADRs e profiles aplicáveis são identificados antes da implementação.
- [ ] Os TaskEnvelopes do Tech Lead definem write scopes disjuntos e ordem de merge.
- [ ] Testes automatizados e evidências obrigatórias passam.
- [ ] QA registra aprovação independente no commit candidato.
- [ ] Reviewer registra aprovação final no mesmo commit.

## Dependências

- `EPIC-011`
- `EPIC-004`

## Escopo permitido de mudança

O envelope pai não autoriza código. Cada história filha possui TaskEnvelope com paths exatos e disjuntos.

## Condições de parada

- há decisão material de produto ou arquitetura não resolvida;
- o contrato obrigatório está ausente ou contraditório;
- o escopo da tarefa sobrepõe outra lane ativa;
- a aceitação não pode ser demonstrada por testes ou evidência.

## Histórias filhas


- `STORY-0185` / `ISSUE-0295` — `Product Owner` — Definir jornada, estados e acessibilidade: React/TypeScript/Vite, design system, cliente OpenAPI, seletor visual, acessibilidade e E2E
- `STORY-0186` / `ISSUE-0296` — `Frontend` — Consolidar slices e liberar integração: React/TypeScript/Vite, design system, cliente OpenAPI, seletor visual, acessibilidade e E2E
- `STORY-0187` / `ISSUE-0297` — `Frontend` — Implementar componentes e interação: React/TypeScript/Vite, design system, cliente OpenAPI, seletor visual, acessibilidade e E2E
- `STORY-0188` / `ISSUE-0298` — `Frontend` — Integrar mapa, fluxo e estados de erro: React/TypeScript/Vite, design system, cliente OpenAPI, seletor visual, acessibilidade e E2E
- `STORY-0189` / `ISSUE-0299` — `QA` — Executar testes de componente, acessibilidade e E2E: React/TypeScript/Vite, design system, cliente OpenAPI, seletor visual, acessibilidade e E2E
- `STORY-0190` / `ISSUE-0300` — `Reviewer` — Auditar UX, contrato e evidência final: React/TypeScript/Vite, design system, cliente OpenAPI, seletor visual, acessibilidade e E2E
- `STORY-0738` / `ISSUE-0848` — `Frontend` — Slice 1/3 — Integrar contratos e cliente tipado: React/TypeScript/Vite, design system, cliente OpenAPI, seletor visual, acessibilidade e E2E [REQ-EPIC, REQ-FS1, REQ-RUN]
- `STORY-0739` / `ISSUE-0849` — `Frontend` — Slice 2/3 — Integrar contratos e cliente tipado: React/TypeScript/Vite, design system, cliente OpenAPI, seletor visual, acessibilidade e E2E [REQ-RUN, REQ-RUNTIME]
- `STORY-0740` / `ISSUE-0850` — `Frontend` — Slice 3/3 — Integrar contratos e cliente tipado: React/TypeScript/Vite, design system, cliente OpenAPI, seletor visual, acessibilidade e E2E [REQ-UX]

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
- **Critérios rastreados:** `AC-ISSUE-0031-01, AC-ISSUE-0031-02, AC-ISSUE-0031-03, AC-ISSUE-0031-04, AC-ISSUE-0031-05, AC-ISSUE-0031-06`
- **Requisitos do épico:** `26`
- **ADRs governantes:** `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-013`, `ADR-014`, `ADR-015`, `ADR-017`, `ADR-023`, `ADR-040`, `ADR-044`, `ADR-045`, `ADR-046`, `ADR-055`
- **Conflito:** `Nenhum`
- **Redundância funcional:** `Nenhuma`
- **Requisito faltante:** `Não`
- **Requisito impossível:** `Não`
- **Dependência circular:** `Não`
- **Matriz canônica:** `docs/07-assurance/ACCEPTANCE_CRITERION_TRACEABILITY.csv`


## Revisão de ADRs — Fase D

- **Resultado:** `PASS`
- **ADRs aplicáveis:** `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-013`, `ADR-014`, `ADR-015`, `ADR-017`, `ADR-023`, `ADR-040`, `ADR-044`, `ADR-045`, `ADR-046`, `ADR-055`
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
| IA | `NOT_APPLICABLE` / `PASS` |
| Testes | `PASS` |
| Artefatos | `PRODUCT_AND_EVIDENCE` / `PASS` |
| Critérios | `36` critérios / `PASS` |
| Review | Arquiteto → QA → Reviewer / `PASS` |

- **Histórias filhas revisadas:** `9`
- **Matriz canônica:** `docs/07-assurance/PHASE-F-ISSUE-DELIVERY-REVIEW.csv`
- **Relatório da sprint:** `docs/07-assurance/phase-f/SPRINT-009-REVIEW.md`
- **Baseline:** `SAR-v2.9-PHASE-F`
- **Resultado:** `PASS`
## CTO Review — Fase G

- **Resultado:** `PASS`
- **Risk tier agregado:** `CRITICAL`
- **Histórias revisadas:** `9`
- **Controles aplicáveis:** `CTO-001, CTO-003, CTO-004, CTO-005, CTO-006, CTO-008, CTO-009, CTO-010, CTO-011, CTO-012, CTO-013, CTO-014, CTO-015`
- **Gate de produção:** `SECURITY_AND_PRIVACY_GATES`
