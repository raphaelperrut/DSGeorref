# ISSUE-0001 — governança de decisões arquiteturais e manutenção da baseline normativa

- **Tipo:** `Envelope de entrega do épico`
- **Status:** `blocked-external`
- **Épico pai:** `EPIC-001`
- **Sprint:** `SPRINT-001`
- **Bounded Context owner:** `BC-001 — Governança de Engenharia e Entrega`
- **Papel owner:** `Tech Lead`
- **Revisão arquitetural obrigatória:** `Arquiteto`
- **QA obrigatório:** `QA`
- **Final review obrigatório:** `Reviewer`

## História

Como equipe de entrega do DSGeorref, precisamos governança de decisões arquiteturais e manutenção da baseline normativa, para que a capacidade de produto vinculada seja entregue com qualidade verificável e integração controlada.

## Critérios de aceitação

- [ ] O resultado de produto de `EPIC-001` é demonstravelmente satisfeito.
- [ ] Contratos, ADRs e profiles aplicáveis são identificados antes da implementação.
- [ ] Os TaskEnvelopes do Tech Lead definem write scopes disjuntos e ordem de merge.
- [ ] Testes automatizados e evidências obrigatórias passam.
- [ ] QA registra aprovação independente no commit candidato.
- [ ] Reviewer registra aprovação final no mesmo commit.

## Dependências

- Nenhuma

## Escopo permitido de mudança

O envelope pai não autoriza código. Cada história filha possui TaskEnvelope com paths exatos e disjuntos.

## Condições de parada

- há decisão material de produto ou arquitetura não resolvida;
- o contrato obrigatório está ausente ou contraditório;
- o escopo da tarefa sobrepõe outra lane ativa;
- a aceitação não pode ser demonstrada por testes ou evidência.

## Histórias filhas


- `STORY-0001` / `ISSUE-0111` — `Arquiteto` — Definir escopo, contratos e invariantes: governança de decisões arquiteturais e manutenção da baseline normativa
- `STORY-0002` / `ISSUE-0112` — `Tech Lead` — Consolidar slices e liberar integração: governança de decisões arquiteturais e manutenção da baseline normativa
- `STORY-0003` / `ISSUE-0113` — `DevOps` — Automatizar validações e controles: governança de decisões arquiteturais e manutenção da baseline normativa
- `STORY-0004` / `ISSUE-0114` — `Tech Lead` — Integrar a capacidade ao fluxo do repositório: governança de decisões arquiteturais e manutenção da baseline normativa
- `STORY-0005` / `ISSUE-0115` — `Reviewer` — Validar evidência e realizar auditoria final: governança de decisões arquiteturais e manutenção da baseline normativa
- `STORY-0688` / `ISSUE-0798` — `Tech Lead` — Slice 1/2 — Materializar a fundação executável: governança de decisões arquiteturais e manutenção da baseline normativa [REQ-FRZ, REQ-GOV-ADR, REQ-GOV-DEC, REQ-ISM, REQ-SPRINT-001]
- `STORY-0689` / `ISSUE-0799` — `Tech Lead` — Slice 2/2 — Materializar a fundação executável: governança de decisões arquiteturais e manutenção da baseline normativa [REQ-SPRINT-001, REQ-TOOL]

## Revisão SAR do envelope

- **Arquitetura aplicável:** contexto, ADRs, módulos, contratos e qualidade estão referenciados pela matriz de rastreabilidade.
- **Decisões tecnológicas em aberto:** nenhuma; parâmetro quantitativo somente pode permanecer evidence-bound com Benchmark Profile.
- **Contract freeze:** obrigatório antes de abrir implementações paralelas.
- **Consistência:** histórias filhas devem formar subgrafo acíclico, possuir TaskEnvelope válido e não colidir em write scope sem serialização explícita.
- **Critério de encerramento:** todas as histórias necessárias concluídas, evidência agregada, QA e Reviewer no mesmo commit candidato, riscos residuais registrados.

## Fechamento normativo da Fase A

- [ ] ADR-007 a ADR-009 permanecem Accepted e sem sobreposição normativa.
- [ ] O registro de decisões informa 22 ADRs e zero decisão arquitetural aberta.
- [ ] O Architecture Review de fechamento autoriza a Fase B.


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-001` — Governança de Engenharia e Entrega.
- **Classificação:** `Enabling`.
- **Integrações cross-context:** obedecem ao Context Map e exigem contrato publicado antes de lanes paralelas.
- **Modelo compartilhado:** proibido; somente primitivas técnicas sem semântica de domínio podem ser reutilizadas.
- **Resultado:** `PASS`.

## Revisão de Requisitos — Fase B

- **Resultado:** `PASS`
- **Critérios rastreados:** `AC-ISSUE-0001-01, AC-ISSUE-0001-02, AC-ISSUE-0001-03, AC-ISSUE-0001-04, AC-ISSUE-0001-05, AC-ISSUE-0001-06`
- **Requisitos do épico:** `23`
- **ADRs governantes:** `ADR-001`, `ADR-003`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-010`, `ADR-011`, `ADR-012`, `ADR-033`, `ADR-034`, `ADR-035`, `ADR-040`, `ADR-057`
- **Conflito:** `Nenhum`
- **Redundância funcional:** `Nenhuma`
- **Requisito faltante:** `Não`
- **Requisito impossível:** `Não`
- **Dependência circular:** `Não`
- **Matriz canônica:** `docs/07-assurance/ACCEPTANCE_CRITERION_TRACEABILITY.csv`


## Revisão de ADRs — Fase D

- **Resultado:** `PASS`
- **ADRs aplicáveis:** `ADR-001`, `ADR-003`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-010`, `ADR-011`, `ADR-012`, `ADR-033`, `ADR-034`, `ADR-035`, `ADR-040`, `ADR-057`
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
| Geo | `NOT_APPLICABLE` / `PASS` |
| IA | `NOT_APPLICABLE` / `PASS` |
| Testes | `PASS` |
| Artefatos | `EVIDENCE_ONLY` / `PASS` |
| Critérios | `28` critérios / `PASS` |
| Review | Arquiteto → QA → Reviewer / `PASS` |

- **Histórias filhas revisadas:** `7`
- **Matriz canônica:** `docs/07-assurance/PHASE-F-ISSUE-DELIVERY-REVIEW.csv`
- **Relatório da sprint:** `docs/07-assurance/phase-f/SPRINT-001-REVIEW.md`
- **Baseline:** `SAR-v2.9-PHASE-F`
- **Resultado:** `PASS`
## CTO Review — Fase G

- **Resultado:** `PASS`
- **Risk tier agregado:** `CRITICAL`
- **Histórias revisadas:** `7`
- **Controles aplicáveis:** `CTO-001, CTO-002, CTO-003, CTO-004, CTO-005, CTO-006, CTO-008, CTO-009, CTO-011, CTO-012, CTO-013, CTO-014, CTO-015`
- **Gate de produção:** `SECURITY_AND_PRIVACY_GATES`
