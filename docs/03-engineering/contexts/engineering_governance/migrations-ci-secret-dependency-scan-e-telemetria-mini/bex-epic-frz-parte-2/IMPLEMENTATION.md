# Controles executáveis BEX/EPIC/FRZ/FS1 — parte 2

## Escopo entregue

Esta slice materializa quatro validadores puros e fail-closed no control plane de `BC-001`:

- `validate_batch_execution`, para cooperação escopada, leases e backpressure, progresso e
  promoção de lote;
- `validate_external_file`, para arquivos externos hostis, roots registrados, limites, scanner
  e digest;
- `validate_sprint_authorization`, para restringir a aprovação final à `SPRINT-001` e manter
  trabalho funcional atrás do Foundation Gate executável;
- `validate_first_functional_slice`, para alvo/referência locais, ingestão imutável,
  pipeline clássico e SGV tri-state.

Os validadores recebem evidência já produzida pelos owners de runtime, segurança e qualidade.
Eles não executam worker, migration, scanner, matching ou SGV, não criam uma segunda autoridade
e não escolhem parâmetros quantitativos. Evidência ausente, coercível, contraditória ou fora do
boundary gera `DecisionRejected` com os requisitos afetados, sem default permissivo.

## Rastreabilidade verificável

| Requisito | Controle executável | Prova focada |
|---|---|---|
| REQ-BEX-007 | cancel/pause escopado, token persistente e safe point | `test_batch_execution_decision_07` |
| REQ-BEX-008 | lease PostgreSQL, fencing/revision, budgets e backpressure | `test_batch_execution_decision_08` |
| REQ-BEX-009 | work units monotônicas persistidas e ETA com confiança ou desconhecida | `test_batch_execution_decision_09` |
| REQ-BEX-010 | escala crescente, fault injection e invariantes multidimensionais | `test_batch_execution_decision_10` |
| REQ-EPIC-041 | path/root, tipo, symlink, limites, scanner e SHA-256 | `test_malicious_file_suite` |
| REQ-FRZ-002 | somente Sprint 001 e gate funcional executável | `test_sprint_zero_authorization_and_functional_foundation_gate_blocking` |
| REQ-FS1-002 | alvo e referência sob roots locais registrados | `test_first_functional_slice_decision_02` |
| REQ-FS1-003 | originals, hashes, metadados e ingestão fail-closed | `test_first_functional_slice_decision_03` |
| REQ-FS1-005 | pipeline clássico repetível/substituível e audit trail | `test_first_functional_slice_decision_05` |
| REQ-FS1-007 | SGV obrigatório com `ACCEPTED`, `REVIEWABLE` ou `REJECTED` coerente | `test_first_functional_slice_decision_07` |

## Compatibilidade, persistência e determinismo

- Os contratos congelados e o módulo da parte 1 permanecem inalterados; esta slice adiciona
  somente controle local de evidência.
- Lease, fencing, revision e progresso somente são aceitos com PostgreSQL como autoridade.
  RabbitMQ e telemetria derivada não podem ser apresentados como estado autoritativo.
- Banco/migration: nenhum schema, tabela ou migration é criado por esta slice de control plane.
  A aplicabilidade de migration do épico permanece intacta e não é satisfeita por estado local
  ou por fila.
- A validação é determinística, imutável e sem I/O. ETA desconhecida é representada
  explicitamente por ausência conjunta de valor e confiança, sem precisão inventada.
- Paths relativos, fora do root, com travessia, symlink declarado ou root não registrado são
  rejeitados. Scanner indisponível ou resultado não limpo também bloqueia a admissão.

## Limites, riscos e rollback

Esta slice comprova conformidade da evidência de admissão; não comprova eficácia do scanner,
execução real de migrations, performance do scheduler, qualidade científica do matching ou
execução física do SGV. Digests e referências são entradas opacas cuja verificação e produção
permanecem com seus owners. Nenhuma capability das partes 3/4 é antecipada.

Rollback antes de consumo é a reversão do commit. Após consumo, a substituição deve preservar
compatibilidade dos registros aceitos e repetir os dez testes canônicos. Não existe rollback de
banco nesta mudança porque nenhum estado persistente ou schema é alterado. QA e Reviewer
independentes devem avaliar o mesmo commit candidato; nenhuma aprovação independente é
reivindicada neste handoff.
