# ISSUE-0013 — backup/restore consistente entre banco e arquivos

- **Tipo:** `Envelope de entrega do épico`
- **Status:** `planned`
- **Épico pai:** `EPIC-013`
- **Sprint:** `SPRINT-002`
- **Bounded Context owner:** `BC-013 — Artifacts, Proveniência e Lifecycle`
- **Papel owner:** `Backend`
- **Revisão arquitetural obrigatória:** `Arquiteto`
- **QA obrigatório:** `QA`
- **Final review obrigatório:** `Reviewer`

## História

Como equipe de entrega do DSGeorref, precisamos backup/restore consistente entre banco e arquivos, para que a capacidade de produto vinculada seja entregue com qualidade verificável e integração controlada.

## Critérios de aceitação

- [ ] O resultado de produto de `EPIC-013` é demonstravelmente satisfeito.
- [ ] Contratos, ADRs e profiles aplicáveis são identificados antes da implementação.
- [ ] Os TaskEnvelopes do Tech Lead definem write scopes disjuntos e ordem de merge.
- [ ] Testes automatizados e evidências obrigatórias passam.
- [ ] QA registra aprovação independente no commit candidato.
- [ ] Reviewer registra aprovação final no mesmo commit.

## Dependências

- `EPIC-012`

## Escopo permitido de mudança

O envelope pai não autoriza código. Cada história filha possui TaskEnvelope com paths exatos e disjuntos.

## Condições de parada

- há decisão material de produto ou arquitetura não resolvida;
- o contrato obrigatório está ausente ou contraditório;
- o escopo da tarefa sobrepõe outra lane ativa;
- a aceitação não pode ser demonstrada por testes ou evidência.

## Histórias filhas


- `STORY-0062` / `ISSUE-0172` — `Arquiteto` — Definir modelo, invariantes e contratos de dados: backup/restore consistente entre banco e arquivos
- `STORY-0063` / `ISSUE-0173` — `Backend` — Implementar persistência e migrations: backup/restore consistente entre banco e arquivos
- `STORY-0064` / `ISSUE-0174` — `Backend` — Implementar armazenamento e lifecycle: backup/restore consistente entre banco e arquivos
- `STORY-0065` / `ISSUE-0175` — `Backend` — Expor serviços e integrar consumers: backup/restore consistente entre banco e arquivos
- `STORY-0066` / `ISSUE-0176` — `Security` — Validar segurança, recuperação e concorrência: backup/restore consistente entre banco e arquivos
- `STORY-0067` / `ISSUE-0177` — `Reviewer` — Executar QA e auditoria final: backup/restore consistente entre banco e arquivos

## Revisão SAR do envelope

- **Arquitetura aplicável:** contexto, ADRs, módulos, contratos e qualidade estão referenciados pela matriz de rastreabilidade.
- **Decisões tecnológicas em aberto:** nenhuma; parâmetro quantitativo somente pode permanecer evidence-bound com Benchmark Profile.
- **Contract freeze:** obrigatório antes de abrir implementações paralelas.
- **Consistência:** histórias filhas devem formar subgrafo acíclico, possuir TaskEnvelope válido e não colidir em write scope sem serialização explícita.
- **Critério de encerramento:** todas as histórias necessárias concluídas, evidência agregada, QA e Reviewer no mesmo commit candidato, riscos residuais registrados.


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-013` — Artifacts, Proveniência e Lifecycle.
- **Classificação:** `Supporting`.
- **Integrações cross-context:** obedecem ao Context Map e exigem contrato publicado antes de lanes paralelas.
- **Modelo compartilhado:** proibido; somente primitivas técnicas sem semântica de domínio podem ser reutilizadas.
- **Resultado:** `PASS`.

## Revisão de Requisitos — Fase B

- **Resultado:** `PASS`
- **Critérios rastreados:** `AC-ISSUE-0013-01, AC-ISSUE-0013-02, AC-ISSUE-0013-03, AC-ISSUE-0013-04, AC-ISSUE-0013-05, AC-ISSUE-0013-06`
- **Requisitos do épico:** `6`
- **ADRs governantes:** `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-016`, `ADR-018`, `ADR-019`, `ADR-026`, `ADR-027`, `ADR-030`, `ADR-031`, `ADR-032`, `ADR-055`
- **Conflito:** `Nenhum`
- **Redundância funcional:** `Nenhuma`
- **Requisito faltante:** `Não`
- **Requisito impossível:** `Não`
- **Dependência circular:** `Não`
- **Matriz canônica:** `docs/07-assurance/ACCEPTANCE_CRITERION_TRACEABILITY.csv`


## Revisão de ADRs — Fase D

- **Resultado:** `PASS`
- **ADRs aplicáveis:** `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-016`, `ADR-018`, `ADR-019`, `ADR-026`, `ADR-027`, `ADR-030`, `ADR-031`, `ADR-032`, `ADR-055`
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
| Critérios | `24` critérios / `PASS` |
| Review | Arquiteto → QA → Reviewer / `PASS` |

- **Histórias filhas revisadas:** `6`
- **Matriz canônica:** `docs/07-assurance/PHASE-F-ISSUE-DELIVERY-REVIEW.csv`
- **Relatório da sprint:** `docs/07-assurance/phase-f/SPRINT-002-REVIEW.md`
- **Baseline:** `SAR-v2.9-PHASE-F`
- **Resultado:** `PASS`
## CTO Review — Fase G

- **Resultado:** `PASS`
- **Risk tier agregado:** `CRITICAL`
- **Histórias revisadas:** `6`
- **Controles aplicáveis:** `CTO-001, CTO-002, CTO-003, CTO-004, CTO-005, CTO-006, CTO-008, CTO-010, CTO-011, CTO-012, CTO-013, CTO-014, CTO-015`
- **Gate de produção:** `SECURITY_AND_PRIVACY_GATES`
