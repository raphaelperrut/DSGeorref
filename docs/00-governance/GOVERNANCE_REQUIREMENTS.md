# Requisitos de governança e entrega

Controles do sistema de engenharia orientado por IA, sem registros históricos ou aliases substituídos.

**Total:** 33 requisitos.

| ID | Prioridade | Requisito | Owner |
|---|---:|---|---|
| `REQ-CIT-001` | P1 | Releases públicas fornecem metadados e instruções de citação | `CITATION_POLICY` |
| `REQ-FRZ-001` | P0 | A Foundation deve possuir baseline identificável e mudanças materiais devem ser orientadas por evidências e supersession explícita | `GOVERNANCE` |
| `REQ-FRZ-002` | P0 | A aprovação final deve autorizar somente a SPRINT-001 e manter a implementação funcional bloqueada pelo executable Foundation Gate | `GOVERNANCE` |
| `REQ-FRZ-003` | P0 | A fronteira entre issue, ADR e owner decision record deve ser proporcional, auditável e impedir divergência silenciosa | `GOVERNANCE` |
| `REQ-FRZ-004` | P0 | O fechamento deve produzir `FoundationClosureEvidenceSet` verificável e critérios explícitos de reabertura | `GOVERNANCE` |
| `REQ-GOV-001` | P1 | Um único GitHub Project central oferece views de roadmap, backlog, sprint, riscos, ADRs, releases e Geo/IA sem duplicar itens | `GITHUB_OPERATING_MODEL` |
| `REQ-GOV-002` | P0 | Épicos representam outcomes encerráveis; histórias implementáveis possuem critérios, ADRs, riscos, testes, evidências, migration e rollback aplicáveis. | `GITHUB_OPERATING_MODEL` |
| `REQ-GOV-003` | P1 | O fluxo limita WIP, preserva histórico de itens incompletos e não usa velocidade como meta de produtividade | `GITHUB_OPERATING_MODEL` |
| `REQ-GOV-004` | P0 | Codex atua somente em issue Ready, branch/worktree curta e PR, sem merge autônomo ou decisão sobre gates sensíveis | `GITHUB_OPERATING_MODEL` |
| `REQ-GOV-005` | P0 | SPRINT-001 termina por SprintEvidenceSet e foundation gate, sem duração fixa ou aprovação automática por calendário | `AP-008` |
| `REQ-GOV-ADR-002` | P0 | Uma proposta de ADR deve demonstrar boundary independente, impacto duradouro e alto custo de reversão. | `ADR_CLASSIFICATION_POLICY` |
| `REQ-GOV-ADR-003` | P0 | Refinements, profiles, benchmarks e detalhes locais não podem ser promovidos artificialmente a ADR. | `ADR_CLASSIFICATION_POLICY` |
| `REQ-GOV-ADR-018` | P1 | Toda ADR nova ou alterada passa por verificação de sobreposição, owner normativo e gate de decisão do Owner. | `ADR_CLASSIFICATION_POLICY` |
| `REQ-GOV-DEC-001` | P1 | toda proposta declara `NEW_ADR`, `REFINE_EXISTING`, `APPLICATION_PROFILE`, `BENCHMARK_PROFILE` ou `ISSUE_DETAIL` antes de receber identificador | `PRODUCT_BASELINE` |
| `REQ-GOV-DEC-002` | P1 | somente escolhas arquiteturais independentes, duráveis e caras de reverter recebem ADR própria | `PRODUCT_BASELINE` |
| `REQ-ISM-001` | P1 | manter taxonomia canônica de domínios com domínio primário e afetados | `GITHUB_OPERATING_MODEL` |
| `REQ-ISM-002` | P1 | Definir cada épico por um outcome verificável e encerrável. | `GITHUB_OPERATING_MODEL` |
| `REQ-ISM-003` | P1 | decompor outcomes em fatias verticais finas e integráveis | `GITHUB_OPERATING_MODEL` |
| `REQ-ISM-004` | P1 | manter catálogo versionado de portfólio reconciliado com o GitHub | `GITHUB_OPERATING_MODEL` |
| `REQ-ISM-005` | P1 | atribuir identificadores estáveis independentes do número GitHub | `GITHUB_OPERATING_MODEL` |
| `REQ-ISM-006` | P1 | sincronizar issues de forma idempotente, com dry-run e campos gerenciados | `PRODUCT_BASELINE` |
| `REQ-ISM-007` | P1 | derivar critérios e evidências de ADRs, requisitos, riscos e gates | `PRODUCT_BASELINE` |
| `REQ-ISM-008` | P1 | representar trabalho transversal sem duplicação de issues | `GITHUB_OPERATING_MODEL` |
| `REQ-ISM-009` | P1 | limitar spikes por pergunta, budget, evidência e decisão de saída | `PRODUCT_BASELINE` |
| `REQ-ISM-010` | P1 | preservar snapshots, tombstones e deltas aprovados da baseline | `GITHUB_OPERATING_MODEL` |
| `REQ-ISS-001` | P0 | Todos os épicos devem possuir issue épica e decomposição rastreável em fatias implementáveis | `GITHUB_OPERATING_MODEL` |
| `REQ-ISS-002` | P1 | A previsão total deve usar intervalo, cenário central, confiança e snapshots versionados | `GITHUB_OPERATING_MODEL` |
| `REQ-ISS-003` | P0 | Toda issue deve apontar ADRs/requisitos/riscos/gates ou justificar decisão local reversível | `GITHUB_OPERATING_MODEL` |
| `REQ-ISS-004` | P1 | O portfólio deve possuir skeleton completo e detalhamento progressivo das próximas fases | `GITHUB_OPERATING_MODEL` |
| `REQ-ISS-006` | P1 | A sincronização de issues é idempotente, suporta dry-run e altera apenas campos sob autoridade do repositório. | `GITHUB_OPERATING_MODEL` |
| `REQ-ISS-007` | P1 | Critérios de aceite e evidências são derivados dos contratos; mudanças de contrato exigem revisão explícita. | `GITHUB_OPERATING_MODEL` |
| `REQ-ISS-009` | P1 | Spikes possuem orçamento, pergunta verificável, saída decisória e critério objetivo de encerramento. | `GITHUB_OPERATING_MODEL` |
| `REQ-OSS-001` | P0 | Código novo publicado sob licença open source aprovada, com notices e inventário de dependências | `GOVERNANCE` |

A especificação individual, a evidência e os vínculos de entrega estão em `docs/01-product/requirements/` e `REQUIREMENT_INDEX.csv`.
