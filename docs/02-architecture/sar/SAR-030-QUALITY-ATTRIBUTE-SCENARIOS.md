# SAR-030 — Cenários de atributos de qualidade

| Atributo | Estímulo | Resposta arquitetural | Evidência |
|---|---|---|---|
| Integridade | crash durante publicação | staging, fsync, validação e rename atômico; nenhum parcial vigente | fault injection + manifest/checksum |
| Reprodutibilidade | replay em ambiente suportado | inputs, versions, profiles, seeds, hardware e digests registrados | reproduction bundle + equivalence tier |
| Segurança | request malicioso/path traversal | IDs opacos, root-relative resolution, allowlist e fail-closed | threat tests |
| Disponibilidade | worker/broker interrompido | ack após commit, redelivery idempotente, checkpoints e reconciliação | integration/fault tests |
| Performance | lote até 300 imagens | chunking, backpressure, fairness e budgets | BP-004 + scale ladder |
| Modificabilidade | troca compatível de framework | ports/adapters, OpenAPI e profiles; core sem tipos de framework | dependency tests |
| Auditabilidade | operação administrativa ou resultado | audit append-only, correlation IDs, lineage e snapshots | audit query + tamper tests |
| Recuperabilidade | perda/restauração da instância | BackupSet coordenado e restore drill isolado | RPO/RTO evidence |
| Usabilidade | resultado ambíguo | diagnóstico, métricas, deformação e remediação explicável | UX/E2E/accessibility tests |

Thresholds quantitativos são definidos exclusivamente pelos Benchmark Profiles associados.
