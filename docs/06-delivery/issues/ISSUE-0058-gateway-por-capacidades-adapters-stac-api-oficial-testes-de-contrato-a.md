# ISSUE-0058 — gateway por capacidades, adapters STAC/API oficial, testes de contrato, allowlist, SSRF/egress e estados de licença/disponibilidade

- **Tipo:** `Envelope de entrega do épico`
- **Status:** `planned`
- **Épico pai:** `EPIC-058`
- **Sprint:** `SPRINT-006`
- **Bounded Context owner:** `BC-005 — Descoberta e Aquisição de Referências`
- **Papel owner:** `Geoprocessamento`
- **Revisão arquitetural obrigatória:** `Arquiteto`
- **QA obrigatório:** `QA`
- **Final review obrigatório:** `Reviewer`

## História

Como equipe de entrega do DSGeorref, precisamos gateway por capacidades, adapters STAC/API oficial, testes de contrato, allowlist, SSRF/egress e estados de licença/disponibilidade, para que a capacidade de produto vinculada seja entregue com qualidade verificável e integração controlada.

## Critérios de aceitação

- [ ] O resultado de produto de `EPIC-058` é demonstravelmente satisfeito.
- [ ] Contratos, ADRs e profiles aplicáveis são identificados antes da implementação.
- [ ] Os TaskEnvelopes do Tech Lead definem write scopes disjuntos e ordem de merge.
- [ ] Testes automatizados e evidências obrigatórias passam.
- [ ] QA registra aprovação independente no commit candidato.
- [ ] Reviewer registra aprovação final no mesmo commit.

## Dependências

- `EPIC-027`
- `EPIC-004`
- `EPIC-041`

## Escopo permitido de mudança

O envelope pai não autoriza código. Cada história filha possui TaskEnvelope com paths exatos e disjuntos.

## Condições de parada

- há decisão material de produto ou arquitetura não resolvida;
- o contrato obrigatório está ausente ou contraditório;
- o escopo da tarefa sobrepõe outra lane ativa;
- a aceitação não pode ser demonstrada por testes ou evidência.

## Histórias filhas


- `STORY-0358` / `ISSUE-0468` — `Arquiteto` — Definir contrato científico e invariantes: gateway por capacidades, adapters STAC/API oficial, testes de contrato, allowlist, SSRF/egress e estados de licença/disponibilidade
- `STORY-0359` / `ISSUE-0469` — `Geoprocessamento` — Preparar corpus, fixtures e representação tipada: gateway por capacidades, adapters STAC/API oficial, testes de contrato, allowlist, SSRF/egress e estados de licença/disponibilidade
- `STORY-0360` / `ISSUE-0470` — `Geoprocessamento` — Implementar o núcleo algorítmico: gateway por capacidades, adapters STAC/API oficial, testes de contrato, allowlist, SSRF/egress e estados de licença/disponibilidade
- `STORY-0361` / `ISSUE-0471` — `Geoprocessamento` — Integrar ao ProcessingPlan e pipeline: gateway por capacidades, adapters STAC/API oficial, testes de contrato, allowlist, SSRF/egress e estados de licença/disponibilidade
- `STORY-0362` / `ISSUE-0472` — `Geoprocessamento` — Produzir métricas, diagnóstico e lineage: gateway por capacidades, adapters STAC/API oficial, testes de contrato, allowlist, SSRF/egress e estados de licença/disponibilidade
- `STORY-0363` / `ISSUE-0473` — `QA` — Executar benchmark, negativos e regressão científica: gateway por capacidades, adapters STAC/API oficial, testes de contrato, allowlist, SSRF/egress e estados de licença/disponibilidade
- `STORY-0364` / `ISSUE-0474` — `Reviewer` — Auditar evidência científica e final: gateway por capacidades, adapters STAC/API oficial, testes de contrato, allowlist, SSRF/egress e estados de licença/disponibilidade

## Revisão SAR do envelope

- **Arquitetura aplicável:** contexto, ADRs, módulos, contratos e qualidade estão referenciados pela matriz de rastreabilidade.
- **Decisões tecnológicas em aberto:** nenhuma; parâmetro quantitativo somente pode permanecer evidence-bound com Benchmark Profile.
- **Contract freeze:** obrigatório antes de abrir implementações paralelas.
- **Consistência:** histórias filhas devem formar subgrafo acíclico, possuir TaskEnvelope válido e não colidir em write scope sem serialização explícita.
- **Critério de encerramento:** todas as histórias necessárias concluídas, evidência agregada, QA e Reviewer no mesmo commit candidato, riscos residuais registrados.


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-005` — Descoberta e Aquisição de Referências.
- **Classificação:** `Supporting`.
- **Integrações cross-context:** obedecem ao Context Map e exigem contrato publicado antes de lanes paralelas.
- **Modelo compartilhado:** proibido; somente primitivas técnicas sem semântica de domínio podem ser reutilizadas.
- **Resultado:** `PASS`.

## Revisão de Requisitos — Fase B

- **Resultado:** `PASS`
- **Critérios rastreados:** `AC-ISSUE-0058-01, AC-ISSUE-0058-02, AC-ISSUE-0058-03, AC-ISSUE-0058-04, AC-ISSUE-0058-05, AC-ISSUE-0058-06`
- **Requisitos do épico:** `6`
- **ADRs governantes:** `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-012`, `ADR-034`, `ADR-041`, `ADR-042`, `ADR-043`, `ADR-047`, `ADR-049`, `ADR-052`
- **Conflito:** `Nenhum`
- **Redundância funcional:** `Nenhuma`
- **Requisito faltante:** `Não`
- **Requisito impossível:** `Não`
- **Dependência circular:** `Não`
- **Matriz canônica:** `docs/07-assurance/ACCEPTANCE_CRITERION_TRACEABILITY.csv`


## Revisão de ADRs — Fase D

- **Resultado:** `PASS`
- **ADRs aplicáveis:** `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-012`, `ADR-034`, `ADR-041`, `ADR-042`, `ADR-043`, `ADR-047`, `ADR-049`, `ADR-052`
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
| Critérios | `28` critérios / `PASS` |
| Review | Arquiteto → QA → Reviewer / `PASS` |

- **Histórias filhas revisadas:** `7`
- **Matriz canônica:** `docs/07-assurance/PHASE-F-ISSUE-DELIVERY-REVIEW.csv`
- **Relatório da sprint:** `docs/07-assurance/phase-f/SPRINT-006-REVIEW.md`
- **Baseline:** `SAR-v2.9-PHASE-F`
- **Resultado:** `PASS`
## CTO Review — Fase G

- **Resultado:** `PASS`
- **Risk tier agregado:** `CRITICAL`
- **Histórias revisadas:** `7`
- **Controles aplicáveis:** `CTO-001, CTO-003, CTO-004, CTO-005, CTO-006, CTO-007, CTO-008, CTO-010, CTO-011, CTO-012, CTO-013, CTO-014, CTO-015`
- **Gate de produção:** `SECURITY_AND_PRIVACY_GATES`
