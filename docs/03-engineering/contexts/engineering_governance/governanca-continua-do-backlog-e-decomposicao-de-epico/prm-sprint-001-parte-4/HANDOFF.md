# Handoff — materialização de portfolio e escopo mínimo da SPRINT-001

## Escopo entregue

Este incremento materializa somente os controles de `REQ-PRM-002..010` e
`REQ-SPRINT-001-001`. A policy é local a `BC-001`, declarativa e validada de forma
estrita e fail-closed. Ela não cria Project, Story, Issue, prerequisite, registry,
endpoint, persistência ou automação operacional.

## Rastreabilidade requisito → evidência

| Requisito | Controle | Evidência |
|---|---|---|
| `REQ-PRM-002` | ondas limitadas por dependência, gate e risco | `test_portfolio_materialization_decision_02` |
| `REQ-PRM-003` | autoridade e direção por campo | `test_portfolio_materialization_decision_03` |
| `REQ-PRM-004` | reconciliação de três vias e conflito explícito | `test_portfolio_materialization_decision_04` |
| `REQ-PRM-005` | ChangeSet aprovado e tombstones | `test_portfolio_materialization_decision_05` |
| `REQ-PRM-006` | idempotência, checkpoints, backoff e retomada segura | `test_portfolio_materialization_decision_06` |
| `REQ-PRM-007` | evidence set anterior à convergência | `test_portfolio_materialization_decision_07` |
| `REQ-PRM-008` | run record por execução, imutável e sanitizado | `test_portfolio_materialization_decision_08` |
| `REQ-PRM-009` | snapshot, compensações seguras e forward reconciliation | `test_portfolio_materialization_decision_09` |
| `REQ-PRM-010` | identidade dedicada e credencial curta | `test_portfolio_materialization_decision_10` |
| `REQ-SPRINT-001-001` | sete capacidades mínimas de `AP-008` | `test_sprint_zero_baseline_decision_01` |

O hardening adicional rejeita campo desconhecido, controle ou evidência ausente,
raiz com tipo inválido, chave JSON duplicada e arquivo ausente. Cada teste obrigatório
também exercita o estado de falha específico do próprio controle, sem default ou
fallback silencioso.

## Impacto em contratos

Nenhum contrato congelado, ADR, schema público, API ou formato de artifact é
alterado. A policy é evidência local de implementação de decisões já vigentes e não
se declara contrato público. API, PostgreSQL, RabbitMQ, migration, frontend, geo, IA
operacional e SGV não são aplicáveis a este slice.

## Riscos e limitações

- O incremento valida configuração versionada; não executa sincronização com GitHub
  nem materializa um Project real.
- A enforcement operacional continuará a exigir adapters e credenciais aprovados em
  tarefa própria; este slice não antecipa essa implementação.
- O status `CANDIDATE` não equivale a aprovação, convergência operacional ou
  production readiness.

## Rollback

Reverter conjuntamente a policy, o validador, os testes, este handoff e a evidência
do incremento. Como não há estado runtime, banco, migration, endpoint ou Project
criado, não existe rollback operacional nem migração reversa. Se a policy já tiver
sido consumida, substituí-la por nova versão revisada, sem sobrescrita silenciosa.

QA e Reviewer devem validar de forma independente o mesmo commit candidato; este
handoff não constitui autoaprovação.
