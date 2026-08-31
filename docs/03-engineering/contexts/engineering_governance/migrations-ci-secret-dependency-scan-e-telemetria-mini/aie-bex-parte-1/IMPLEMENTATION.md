# Controles executáveis de decisão AIE/BEX — parte 1

## Escopo entregue

Esta slice materializa no control plane de `BC-001` dois validadores puros e fail-closed:

- `validate_ai_escalation`, para as decisões cobertas por `REQ-AIE-002`, `003`, `004`,
  `006`, `007`, `008`, `009` e `010`;
- `validate_batch_execution`, para `REQ-BEX-002` e `REQ-BEX-004`.

Os validadores recebem evidência já produzida pelos owners de runtime e policy. Não criam uma
segunda autoridade, não escolhem parâmetros quantitativos e não executam IA, SGV, scheduler,
migration, scanner, exporter ou publicação de artifact. Uma violação gera `DecisionRejected`
com os IDs dos requisitos não satisfeitos; não há coerção, default permissivo ou fallback
silencioso.

## Rastreabilidade verificável

| Requisito | Controle executável | Prova focada |
|---|---|---|
| REQ-AIE-002 | baseline clássica, checkpoint e trigger obrigatórios | `test_ai_escalation_decision_02` |
| REQ-AIE-003 | recomendação repetível e capabilities compatíveis | `test_ai_escalation_decision_03` |
| REQ-AIE-004 | attempts, tempo, memória, device e prioridade dentro do profile | `test_ai_escalation_decision_04` |
| REQ-AIE-006 | IA opcional, baseline CPU funcional e indisponibilidade explícita | `test_ai_escalation_decision_06` |
| REQ-AIE-007 | SGV independente; consenso e revisão equivalentes ao risco | `test_ai_escalation_decision_07` |
| REQ-AIE-008 | ModelPack assinado, pinado, licenciado, opt-in e offline | `test_ai_escalation_decision_08` |
| REQ-AIE-009 | explicação completa sem bypass de quality gate | `test_ai_escalation_decision_09` |
| REQ-AIE-010 | corpus, shadow, dual-run, canary, gate multidimensional e rollback | `test_ai_escalation_decision_10` |
| REQ-BEX-002 | preflight e chunking adaptativo precedem admission | `test_batch_execution_decision_02` |
| REQ-BEX-004 | classe, fairness, aging e override auditado | `test_batch_execution_decision_04` |

## Compatibilidade, impacto e limites

- Contratos congelados das predecessoras permanecem inalterados; o protocolo `AIBackend`
  continua com SGV e publicação fora deste validator.
- Persistência e migration: N/A. Esta slice não cria tabela, estado autoritativo ou migration;
  o requisito de migration do épico pertence às slices explicitamente separadas.
- Telemetria, CI e scans: não alterados nesta slice; nenhuma capacidade das slices irmãs é
  antecipada.
- Idempotência: validadores são determinísticos, imutáveis e sem I/O ou estado global.
- Rollback: reverter o commit antes do consumo; após consumo, substituir por mudança compatível
  e retestar o mesmo conjunto canônico.

## Riscos residuais e próximo gate

Os controles provam completude e rejeição das evidências de decisão, não eficácia científica,
execução real de backend, SGV, scheduler ou promoção. Os digests e referências são tratados
como evidência opaca; verificação criptográfica permanece com os owners dos artifacts. QA
sentinela e Reviewer independentes devem avaliar o mesmo commit candidato; nenhuma aprovação
independente é reivindicada aqui.
