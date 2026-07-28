# ISSUE-0002 — repositório privado, Project central/views/campos, labels, Issue Forms, templates, ruleset, checks e configuração reproduzível

- **Tipo:** `Envelope de entrega do épico`
- **Status:** `planned`
- **Épico pai:** `EPIC-002`
- **Sprint:** `SPRINT-001`
- **Bounded Context owner:** `BC-001 — Governança de Engenharia e Entrega`
- **Papel owner:** `Tech Lead`
- **Revisão arquitetural obrigatória:** `Arquiteto`
- **QA obrigatório:** `QA`
- **Final review obrigatório:** `Reviewer`

## História

Como equipe de entrega do DSGeorref, precisamos repositório privado, Project central/views/campos, labels, Issue Forms, templates, ruleset, checks e configuração reproduzível, para que a capacidade de produto vinculada seja entregue com qualidade verificável e integração controlada.

## Critérios de aceitação

- [ ] O resultado de produto de `EPIC-002` é demonstravelmente satisfeito.
- [ ] Contratos, ADRs e profiles aplicáveis são identificados antes da implementação.
- [ ] Os TaskEnvelopes do Tech Lead definem write scopes disjuntos e ordem de merge.
- [ ] Testes automatizados e evidências obrigatórias passam.
- [ ] QA registra aprovação independente no commit candidato.
- [ ] Reviewer registra aprovação final no mesmo commit.

## Dependências

- `EPIC-001`

## Escopo permitido de mudança

O envelope pai não autoriza código. Cada história filha possui TaskEnvelope com paths exatos e disjuntos.

## Condições de parada

- há decisão material de produto ou arquitetura não resolvida;
- o contrato obrigatório está ausente ou contraditório;
- o escopo da tarefa sobrepõe outra lane ativa;
- a aceitação não pode ser demonstrada por testes ou evidência.

## Histórias filhas


- `STORY-0006` / `ISSUE-0116` — `Arquiteto` — Consolidar slices e liberar integração: repositório privado, Project central/views/campos, labels, Issue Forms, templates, ruleset, checks e configuração reproduzível
- `STORY-0007` / `ISSUE-0117` — `Tech Lead` — Consolidar slices e liberar integração: repositório privado, Project central/views/campos, labels, Issue Forms, templates, ruleset, checks e configuração reproduzível
- `STORY-0008` / `ISSUE-0118` — `DevOps` — Automatizar validações e controles: repositório privado, Project central/views/campos, labels, Issue Forms, templates, ruleset, checks e configuração reproduzível
- `STORY-0009` / `ISSUE-0119` — `Tech Lead` — Integrar a capacidade ao fluxo do repositório: repositório privado, Project central/views/campos, labels, Issue Forms, templates, ruleset, checks e configuração reproduzível
- `STORY-0010` / `ISSUE-0120` — `Reviewer` — Validar evidência e realizar auditoria final: repositório privado, Project central/views/campos, labels, Issue Forms, templates, ruleset, checks e configuração reproduzível
- `STORY-0690` / `ISSUE-0800` — `Arquiteto` — Slice 1/2 — Definir escopo, contratos e invariantes: repositório privado, Project central/views/campos, labels, Issue Forms, templates, ruleset, checks e configuração reproduzível [REQ-CLASSICPROFILE, REQ-ISS, REQ-NATIVE, REQ-PLN, REQ-PRJ, REQ-RUN, REQ-SPRINT-001]
- `STORY-0691` / `ISSUE-0801` — `Arquiteto` — Slice 2/2 — Definir escopo, contratos e invariantes: repositório privado, Project central/views/campos, labels, Issue Forms, templates, ruleset, checks e configuração reproduzível [REQ-WORKER]
- `STORY-0692` / `ISSUE-0802` — `Tech Lead` — Slice 1/9 — Materializar a fundação executável: repositório privado, Project central/views/campos, labels, Issue Forms, templates, ruleset, checks e configuração reproduzível [REQ-CLASSICPROFILE, REQ-GOV, REQ-GOV-ADR]
- `STORY-0693` / `ISSUE-0803` — `Tech Lead` — Slice 2/9 — Materializar a fundação executável: repositório privado, Project central/views/campos, labels, Issue Forms, templates, ruleset, checks e configuração reproduzível [REQ-GOV-ADR, REQ-ISM, REQ-ISS, REQ-NATIVE]
- `STORY-0694` / `ISSUE-0804` — `Tech Lead` — Slice 3/9 — Materializar a fundação executável: repositório privado, Project central/views/campos, labels, Issue Forms, templates, ruleset, checks e configuração reproduzível [REQ-NATIVE, REQ-PLN]
- `STORY-0695` / `ISSUE-0805` — `Tech Lead` — Slice 4/9 — Materializar a fundação executável: repositório privado, Project central/views/campos, labels, Issue Forms, templates, ruleset, checks e configuração reproduzível [REQ-PLN, REQ-PRJ]
- `STORY-0696` / `ISSUE-0806` — `Tech Lead` — Slice 5/9 — Materializar a fundação executável: repositório privado, Project central/views/campos, labels, Issue Forms, templates, ruleset, checks e configuração reproduzível [REQ-PRJ, REQ-PRM]
- `STORY-0697` / `ISSUE-0807` — `Tech Lead` — Slice 6/9 — Materializar a fundação executável: repositório privado, Project central/views/campos, labels, Issue Forms, templates, ruleset, checks e configuração reproduzível [REQ-PRM, REQ-RUN]
- `STORY-0698` / `ISSUE-0808` — `Tech Lead` — Slice 7/9 — Materializar a fundação executável: repositório privado, Project central/views/campos, labels, Issue Forms, templates, ruleset, checks e configuração reproduzível [REQ-RUNTIME, REQ-SPRINT-001]
- `STORY-0699` / `ISSUE-0809` — `Tech Lead` — Slice 8/9 — Materializar a fundação executável: repositório privado, Project central/views/campos, labels, Issue Forms, templates, ruleset, checks e configuração reproduzível [REQ-SPRINT-001, REQ-TOOL, REQ-WORKER]
- `STORY-0700` / `ISSUE-0810` — `Tech Lead` — Slice 9/9 — Materializar a fundação executável: repositório privado, Project central/views/campos, labels, Issue Forms, templates, ruleset, checks e configuração reproduzível [REQ-WORKER]

## Revisão SAR do envelope

- **Arquitetura aplicável:** contexto, ADRs, módulos, contratos e qualidade estão referenciados pela matriz de rastreabilidade.
- **Decisões tecnológicas em aberto:** nenhuma; parâmetro quantitativo somente pode permanecer evidence-bound com Benchmark Profile.
- **Contract freeze:** obrigatório antes de abrir implementações paralelas.
- **Consistência:** histórias filhas devem formar subgrafo acíclico, possuir TaskEnvelope válido e não colidir em write scope sem serialização explícita.
- **Critério de encerramento:** todas as histórias necessárias concluídas, evidência agregada, QA e Reviewer no mesmo commit candidato, riscos residuais registrados.

## Packages e write scopes estáveis

- [ ] Nenhum TaskEnvelope usa path de produção derivado de épico, issue, story ou task.
- [ ] `write-scope-catalog.yaml` cobre todas as histórias.
- [ ] Write scopes concorrentes são disjuntos ou serializados.


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-001` — Governança de Engenharia e Entrega.
- **Classificação:** `Enabling`.
- **Integrações cross-context:** obedecem ao Context Map e exigem contrato publicado antes de lanes paralelas.
- **Modelo compartilhado:** proibido; somente primitivas técnicas sem semântica de domínio podem ser reutilizadas.
- **Resultado:** `PASS`.

## Revisão de Requisitos — Fase B

- **Resultado:** `PASS`
- **Critérios rastreados:** `AC-ISSUE-0002-01, AC-ISSUE-0002-02, AC-ISSUE-0002-03, AC-ISSUE-0002-04, AC-ISSUE-0002-05, AC-ISSUE-0002-06`
- **Requisitos do épico:** `99`
- **ADRs governantes:** `ADR-001`, `ADR-002`, `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-012`, `ADR-013`, `ADR-015`, `ADR-016`, `ADR-017`, `ADR-018`, `ADR-020`, `ADR-022`, `ADR-025`, `ADR-033`, `ADR-034`, `ADR-035`, `ADR-037`, `ADR-038`, `ADR-039`, `ADR-040`, `ADR-041`, `ADR-042`, `ADR-043`, `ADR-044`, `ADR-045`, `ADR-050`, `ADR-053`, `ADR-055`
- **Conflito:** `Nenhum`
- **Redundância funcional:** `Nenhuma`
- **Requisito faltante:** `Não`
- **Requisito impossível:** `Não`
- **Dependência circular:** `Não`
- **Matriz canônica:** `docs/07-assurance/ACCEPTANCE_CRITERION_TRACEABILITY.csv`


## Revisão de ADRs — Fase D

- **Resultado:** `PASS`
- **ADRs aplicáveis:** `ADR-001`, `ADR-002`, `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-012`, `ADR-013`, `ADR-015`, `ADR-016`, `ADR-017`, `ADR-018`, `ADR-020`, `ADR-022`, `ADR-025`, `ADR-033`, `ADR-034`, `ADR-035`, `ADR-037`, `ADR-038`, `ADR-039`, `ADR-040`, `ADR-041`, `ADR-042`, `ADR-043`, `ADR-044`, `ADR-045`, `ADR-050`, `ADR-053`, `ADR-055`
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
| Banco | `NOT_APPLICABLE` / `PASS` |
| Frontend | `NOT_APPLICABLE` / `PASS` |
| Geo | `NOT_APPLICABLE` / `PASS` |
| IA | `APPLICABLE` / `PASS` |
| Testes | `PASS` |
| Artefatos | `PRODUCT_AND_EVIDENCE` / `PASS` |
| Critérios | `64` critérios / `PASS` |
| Review | Arquiteto → QA → Reviewer / `PASS` |

- **Histórias filhas revisadas:** `16`
- **Matriz canônica:** `docs/07-assurance/PHASE-F-ISSUE-DELIVERY-REVIEW.csv`
- **Relatório da sprint:** `docs/07-assurance/phase-f/SPRINT-001-REVIEW.md`
- **Baseline:** `SAR-v2.9-PHASE-F`
- **Resultado:** `PASS`
## CTO Review — Fase G

- **Resultado:** `PASS`
- **Risk tier agregado:** `CRITICAL`
- **Histórias revisadas:** `16`
- **Controles aplicáveis:** `CTO-001, CTO-002, CTO-003, CTO-004, CTO-005, CTO-006, CTO-007, CTO-008, CTO-009, CTO-010, CTO-011, CTO-012, CTO-013, CTO-014, CTO-015`
- **Gate de produção:** `SECURITY_AND_PRIVACY_GATES`
