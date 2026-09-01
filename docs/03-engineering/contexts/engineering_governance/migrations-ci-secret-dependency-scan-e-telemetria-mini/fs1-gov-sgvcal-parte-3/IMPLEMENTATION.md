# Controles executáveis FS1/GOV/SGVCAL — parte 3

## Escopo entregue

Esta slice materializa três validadores puros, imutáveis e fail-closed no control plane de
`BC-001`:

- `validate_functional_slice`, para publicação atômica do `ArtifactSet`, equivalência do core
  compartilhado nas quatro superfícies e promoção pelo corpus inicial estratificado;
- `validate_sgv_calibration`, para imutabilidade por estrato, declaração completa das métricas,
  erro simétrico robusto, coverage, estabilidade e Jacobiano adaptativo;
- `validate_delivery_governance`, para exigir issue autorizada, TaskEnvelope, branch/worktree
  dedicadas e PR sem direct-main, automerge ou decisão de gate sensível pelo executor.

Os valores canônicos são reutilizados do foundation checkpoint e do contrato SGVCAL congelado
dos predecessores. Esta slice valida evidência de admissão; não cria contrato, registry, profile,
pipeline científico, superfície de execução ou segunda autoridade.

## Rastreabilidade verificável

| Requisito | Controle executável | Prova focada |
|---|---|---|
| REQ-FS1-008 | bundle imutável COG/provenance-manifest/report, digests, publicação atômica após SGV | `test_first_functional_slice_decision_08` |
| REQ-FS1-009 | mesmo application service e semântica em REST, CLI, direct runner e Celery | `test_first_functional_slice_decision_09` |
| REQ-FS1-010 | corpus versionado/estratificado e quatro gates com evidência | `test_first_functional_slice_decision_10` |
| REQ-GOV-004 | issue/TaskEnvelope/branch/worktree/PR sem main direto, automerge ou gate autônomo | `test_codex_issue_scope_required_pr_no_direct_main_or_automerge` |
| REQ-SGVCAL-001 | profile, invariantes e digest imutáveis por estrato | `test_req_sgvcal_001` |
| REQ-SGVCAL-002 | espaço, unidade, direção e normalização por métrica | `test_req_sgvcal_002` |
| REQ-SGVCAL-003 | transferência simétrica e distribuição robusta | `test_req_sgvcal_003` |
| REQ-SGVCAL-004 | leverage e suporte espacial obrigatórios | `test_req_sgvcal_004` |
| REQ-SGVCAL-005 | condicionamento, degenerescência e leave-one-out obrigatórios | `test_req_sgvcal_005` |
| REQ-SGVCAL-006 | deformação local por Jacobiano adaptativo | `test_req_sgvcal_006` |

## Compatibilidade, determinismo e erros

- `foundation-checkpoint.json` e `sgvcal-conformance.json` permanecem inalterados e são usados
  pelos testes como baselines canônicas.
- DTOs usam estruturas ordenadas e imutáveis. Surfaces, kinds, dimensões e checks precisam ser
  exatos; digest precisa ser SHA-256 lowercase; booleanos coercíveis não são aceitos.
- Toda dimensão de promoção precisa passar e apresentar evidência. Métrica sem qualquer uma das
  quatro declarações, profile móvel, SGV incompleto ou estado `WARN` é rejeitado explicitamente.
- Evidência ausente ou de tipo incorreto retorna `DecisionRejected` com todos os requisitos
  afetados, sem default permissivo ou fallback silencioso.

## Contratos, migrations, limites e rollback

Nenhum contrato congelado, endpoint, schema, tabela, migration ou estado persistente é alterado.
A aplicabilidade de banco do épico permanece preservada, mas não é implementada novamente por
esta slice de control plane. O diff também não executa REST, CLI, runner, Celery, publicação COG,
matching ou SGV físico; ele valida evidência produzida pelos respectivos owners.

Rollback antes de consumo é a reversão do commit. Após consumo, uma substituição deve manter a
compatibilidade das evidências aceitas e repetir os dez testes canônicos. Não há rollback de banco.
QA, Arquiteto e Reviewer independentes devem avaliar o mesmo commit candidato; nenhuma aprovação
independente é reivindicada neste handoff. A parte 4 não é referenciada nem antecipada pelo código.
