# Controles executáveis SGVCAL/SRG/SRP/SUP/TOOL/UPG — parte 4

## Escopo entregue

Esta slice final materializa no control plane de `BC-001` validadores puros, imutáveis e
fail-closed para:

- calibração estratificada com holdout cego e budget bloqueante de falso aceite;
- zona cinzenta sem override de hard gate e promoção shadow/canary com evidência e rollback;
- seleção de testes por grafo de impacto, tiers obrigatórios e matriz completa para promotion
  candidates;
- replay offline e determinístico das decisões de admissão, fairness, lease, backpressure e
  breaker sem workload científico nem providers;
- release com locks e pins imutáveis, SBOM, scanning, checksums, assinatura OCI e provenance;
- gates locais/CI de Ruff e mypy, integração com PostGIS/RabbitMQ reais e frontend strict com
  Vitest, Testing Library e Playwright;
- cutover atômico condicionado a invariantes, readers históricos, health e canary.

O contrato SGVCAL congelado é reutilizado como baseline; nenhum contrato, registry, profile,
schema ou segunda autoridade é criado.

## Rastreabilidade verificável

| Requisito | Controle executável | Prova focada |
|---|---|---|
| REQ-SGVCAL-008 | calibração estratificada, holdout separado e budget bloqueante | `test_req_sgvcal_008` |
| REQ-SGVCAL-009 | reviewable sem override; hard gate falho rejeita | `test_req_sgvcal_009` |
| REQ-SGVCAL-010 | shadow/canary com digests, profile imutável e rollback | `test_req_sgvcal_0010` |
| REQ-SRG-002 | grafo de impacto, tiers obrigatórios e full matrix | `test_change_impact_graph_mandatory_tiers_and_full_promotion_matrix` |
| REQ-SRP-002 | replay completo offline sem workload ou provider | `test_offline_scheduler_decision_replay_without_scientific_workload_or_providers` |
| REQ-SUP-001 | locks, pins, SBOM, scan, checksums, assinatura OCI e provenance | `test_release_sbom_signature_provenance_immutable_pins` |
| REQ-TOOL-006 | `make python-quality` executa Ruff e mypy versionados; `make verify` e CI bloqueiam falhas | `test_ruff_mypy_gate` |
| REQ-TOOL-007 | PostGIS autoritativo e RabbitMQ somente transporte | `test_pytest_real_services` |
| REQ-TOOL-009 | workspace mínimo executa TypeScript strict, Vitest + Testing Library e Playwright; `make verify` e CI bloqueiam falhas | `test_frontend_strict_and_browser` |
| REQ-UPG-003 | quatro dimensões evidenciadas antes do cutover atômico | `test_post_migration_multidimensional_evidence_gate_canary_and_atomic_cutover` |

## Compatibilidade, determinismo e erros

- DTOs e resultados usam tuples ordenadas e dataclasses congeladas; o replay devolve a mesma
  sequência para o mesmo snapshot e não possui I/O.
- Digests são SHA-256 lowercase; booleanos coercíveis, dimensões duplicadas ou incompletas,
  resultados sem evidência e estados permissivos são rejeitados.
- Toda dimensão requerida precisa passar. Promotion candidate sem full matrix, replay com
  provider/workload e cutover sem qualquer gate falham explicitamente.
- Evidência ausente ou de tipo incorreto gera `DecisionRejected` com todos os requisitos afetados,
  sem default permissivo ou fallback silencioso.
- REQ-TOOL-006 e REQ-TOOL-009 não aceitam DTO, booleano ou lista declarativa: sua prova é a
  execução dos comandos versionados conectados ao mesmo `make verify` chamado pelo CI.

## Contratos, migrations, riscos e rollback

O diff não altera contrato congelado, endpoint, schema, tabela, migration ou estado persistente.
A aplicabilidade de banco do épico permanece preservada. O frontend acrescentado é somente o
tooling mínimo de validação, sem produto, rota, componente, endpoint ou estado. PostgreSQL/PostGIS
permanece autoritativo e RabbitMQ somente transporte.

Risco residual: attestations das demais capacidades ainda dependem de seus producers e
verificadores preservarem identidade, digest e provenance. Ruff, mypy, TypeScript, Vitest,
Testing Library e Playwright, porém, são executados diretamente e falham de forma bloqueante.
Não se reivindica aprovação de QA, Arquiteto ou Reviewer.

Rollback antes de consumo é a reversão do commit. Após consumo, uma substituição deve aceitar as
mesmas evidências conformes ou ser versionada, repetir os dez testes canônicos e preservar a
rejeição fail-closed. Não há rollback de banco para este diff.
