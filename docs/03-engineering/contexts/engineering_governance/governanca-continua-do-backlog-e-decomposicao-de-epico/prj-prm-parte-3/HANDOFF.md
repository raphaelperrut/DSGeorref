# Handoff — governança de Project e primeira materialização

## Escopo entregue

Este incremento materializa somente os controles de `REQ-PRJ-001`, `REQ-PRJ-002`,
`REQ-PRJ-003`, `REQ-PRJ-005`, `REQ-PRJ-006`, `REQ-PRJ-007`, `REQ-PRJ-008`,
`REQ-PRJ-009`, `REQ-PRJ-010` e `REQ-PRM-001`. A policy é local a `BC-001`,
declarativa e validada de forma fail-closed. Ela não cria Project, Story, Issue,
prerequisite, registry, endpoint, persistência ou automação operacional.

## Evidência

| Requisito | Controle | Teste |
|---|---|---|
| `REQ-PRJ-001` | taxonomia canônica, form por tipo e rejeição de tipo desconhecido | `test_issue_type_forms` |
| `REQ-PRJ-002` | núcleo e extensões por tipo obrigatórios | `test_mandatory_core_type_fields` |
| `REQ-PRJ-003` | parent primário único e hierarquia limitada | `test_single_parent_limited_hierarchy` |
| `REQ-PRJ-005` | Definition of Ready proporcional | `test_definition_of_ready_gate` |
| `REQ-PRJ-006` | Definition of Done baseada em evidência e checks aplicáveis | `test_evidence_based_definition_of_done` |
| `REQ-PRJ-007` | dependência tipada e ciclo material rejeitado | `test_typed_dependency_cycle_detection` |
| `REQ-PRJ-008` | impacto, urgência, risco e gate separados | `test_derived_priority_dimensions` |
| `REQ-PRJ-009` | faixa relativa, confiança e regra de divisão | `test_relative_size_uncertainty_split` |
| `REQ-PRJ-010` | integridade e decisão material humana | `test_guarded_project_automation` |
| `REQ-PRM-001` | staging representativo antes do Project operacional | `test_portfolio_materialization_decision_01` |

O teste adicional `test_policy_input_is_strict_and_fail_closed` cobre campo
desconhecido, controle obrigatório ausente, evidência obrigatória ausente, raiz com
tipo inválido, chave JSON duplicada e arquivo inexistente. Não há default,
preenchimento por inferência ou fallback silencioso.

## Impacto em contratos

Nenhum contrato congelado, ADR, schema público, API ou formato de artifact é alterado.
O contrato `backlog-governance-profile` 1.0.0 de `BC-001` permanece upstream e
imutável. Esta policy é evidência local de implementação e não se declara um novo
contrato público. Persistência, migration, RabbitMQ, IA e SGV não são aplicáveis.

## Riscos e limitações

- O incremento valida a configuração versionada; não materializa nem reconcilia um
  GitHub Project real.
- A primeira execução real continua condicionada a staging representativo e revisão
  independente; o status `CANDIDATE` não equivale a aprovação.
- Os controles de `REQ-PRM-002..010` pertencem a slices posteriores e não são
  antecipados aqui.

## Rollback

Reverter conjuntamente os quatro arquivos deste incremento antes de qualquer consumo.
Como não há estado runtime, banco, migration, endpoint ou Project criado, não existe
rollback operacional nem migração reversa. Se a policy já tiver sido consumida, a
mudança deve ser substituída por nova versão revisada, sem sobrescrita silenciosa.

QA e Reviewer devem validar de forma independente o mesmo commit candidato; este
handoff não constitui autoaprovação.
