# ISSUE-0012 — raízes de workspace, API de navegação segura, catálogo, hashes e lineage

- **Tipo:** `Envelope de entrega do épico`
- **Status:** `planned`
- **Épico pai:** `EPIC-012`
- **Sprint:** `SPRINT-002`
- **Bounded Context owner:** `BC-003 — Projetos, Workspace e Assets`
- **Papel owner:** `Backend`
- **Revisão arquitetural obrigatória:** `Arquiteto`
- **QA obrigatório:** `QA`
- **Final review obrigatório:** `Reviewer`

## História

Como equipe de entrega do DSGeorref, precisamos raízes de workspace, API de navegação segura, catálogo, hashes e lineage, para que a capacidade de produto vinculada seja entregue com qualidade verificável e integração controlada.

## Critérios de aceitação

- [ ] O resultado de produto de `EPIC-012` é demonstravelmente satisfeito.
- [ ] Contratos, ADRs e profiles aplicáveis são identificados antes da implementação.
- [ ] Os TaskEnvelopes do Tech Lead definem write scopes disjuntos e ordem de merge.
- [ ] Testes automatizados e evidências obrigatórias passam.
- [ ] QA registra aprovação independente no commit candidato.
- [ ] Reviewer registra aprovação final no mesmo commit.

## Dependências

- `EPIC-005`
- `EPIC-010`

## Escopo permitido de mudança

O envelope pai não autoriza código. Cada história filha possui TaskEnvelope com paths exatos e disjuntos.

## Condições de parada

- há decisão material de produto ou arquitetura não resolvida;
- o contrato obrigatório está ausente ou contraditório;
- o escopo da tarefa sobrepõe outra lane ativa;
- a aceitação não pode ser demonstrada por testes ou evidência.

## Histórias filhas


- `STORY-0056` / `ISSUE-0166` — `Arquiteto` — Definir modelo, invariantes e contratos de dados: raízes de workspace, API de navegação segura, catálogo, hashes e lineage
- `STORY-0057` / `ISSUE-0167` — `Backend` — Consolidar slices e liberar integração: raízes de workspace, API de navegação segura, catálogo, hashes e lineage
- `STORY-0058` / `ISSUE-0168` — `Backend` — Implementar armazenamento e lifecycle: raízes de workspace, API de navegação segura, catálogo, hashes e lineage
- `STORY-0059` / `ISSUE-0169` — `Backend` — Expor serviços e integrar consumers: raízes de workspace, API de navegação segura, catálogo, hashes e lineage
- `STORY-0060` / `ISSUE-0170` — `Security` — Validar segurança, recuperação e concorrência: raízes de workspace, API de navegação segura, catálogo, hashes e lineage
- `STORY-0061` / `ISSUE-0171` — `Reviewer` — Executar QA e auditoria final: raízes de workspace, API de navegação segura, catálogo, hashes e lineage
- `STORY-0718` / `ISSUE-0828` — `Backend` — Slice 1/3 — Implementar persistência e migrations: raízes de workspace, API de navegação segura, catálogo, hashes e lineage [REQ-ART, REQ-ARTLAYOUT, REQ-CAT, REQ-DBSCHEMA, REQ-FS]
- `STORY-0719` / `ISSUE-0829` — `Backend` — Slice 2/3 — Implementar persistência e migrations: raízes de workspace, API de navegação segura, catálogo, hashes e lineage [REQ-PRV, REQ-RUN, REQ-SCM, REQ-TOOL]
- `STORY-0720` / `ISSUE-0830` — `Backend` — Slice 3/3 — Implementar persistência e migrations: raízes de workspace, API de navegação segura, catálogo, hashes e lineage [REQ-UPG]

## Revisão SAR do envelope

- **Arquitetura aplicável:** contexto, ADRs, módulos, contratos e qualidade estão referenciados pela matriz de rastreabilidade.
- **Decisões tecnológicas em aberto:** nenhuma; parâmetro quantitativo somente pode permanecer evidence-bound com Benchmark Profile.
- **Contract freeze:** obrigatório antes de abrir implementações paralelas.
- **Consistência:** histórias filhas devem formar subgrafo acíclico, possuir TaskEnvelope válido e não colidir em write scope sem serialização explícita.
- **Critério de encerramento:** todas as histórias necessárias concluídas, evidência agregada, QA e Reviewer no mesmo commit candidato, riscos residuais registrados.


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-003` — Projetos, Workspace e Assets.
- **Classificação:** `Supporting`.
- **Integrações cross-context:** obedecem ao Context Map e exigem contrato publicado antes de lanes paralelas.
- **Modelo compartilhado:** proibido; somente primitivas técnicas sem semântica de domínio podem ser reutilizadas.
- **Resultado:** `PASS`.

## Revisão de Requisitos — Fase B

- **Resultado:** `PASS`
- **Critérios rastreados:** `AC-ISSUE-0012-01, AC-ISSUE-0012-02, AC-ISSUE-0012-03, AC-ISSUE-0012-04, AC-ISSUE-0012-05, AC-ISSUE-0012-06`
- **Requisitos do épico:** `30`
- **ADRs governantes:** `ADR-001`, `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-012`, `ADR-013`, `ADR-014`, `ADR-015`, `ADR-016`, `ADR-017`, `ADR-018`, `ADR-019`, `ADR-020`, `ADR-023`, `ADR-025`, `ADR-026`, `ADR-030`, `ADR-031`, `ADR-032`, `ADR-040`, `ADR-041`, `ADR-043`, `ADR-045`, `ADR-055`
- **Conflito:** `Nenhum`
- **Redundância funcional:** `Nenhuma`
- **Requisito faltante:** `Não`
- **Requisito impossível:** `Não`
- **Dependência circular:** `Não`
- **Matriz canônica:** `docs/07-assurance/ACCEPTANCE_CRITERION_TRACEABILITY.csv`


## Revisão de ADRs — Fase D

- **Resultado:** `PASS`
- **ADRs aplicáveis:** `ADR-001`, `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-012`, `ADR-013`, `ADR-014`, `ADR-015`, `ADR-016`, `ADR-017`, `ADR-018`, `ADR-019`, `ADR-020`, `ADR-023`, `ADR-025`, `ADR-026`, `ADR-030`, `ADR-031`, `ADR-032`, `ADR-040`, `ADR-041`, `ADR-043`, `ADR-045`, `ADR-055`
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
- **Controles aplicáveis:** `CTO-001, CTO-002, CTO-003, CTO-004, CTO-005, CTO-006, CTO-008, CTO-009, CTO-010, CTO-011, CTO-012, CTO-013, CTO-014, CTO-015`
- **Gate de produção:** `SECURITY_AND_PRIVACY_GATES`
