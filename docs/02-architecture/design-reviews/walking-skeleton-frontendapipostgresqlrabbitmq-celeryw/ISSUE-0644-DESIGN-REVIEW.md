# Design review — ISSUE-0644

- **Candidate:** `ISSUE-0644` / `STORY-0534` / `TASK-0534`
- **Owner:** `BC-001 — Governança de Engenharia e Entrega`
- **Status:** implementação candidata; revisão independente pendente
- **Contract version:** `1.0.0`

## Propósito e contenção

Congelar o menor contrato executável para o walking skeleton
frontend → API → PostgreSQL → RabbitMQ/Celery → worker → artefato diagnóstico.
Esta Story define ordem, interfaces, autoridade, compatibilidade, falhas e prova; a
materialização do runtime permanece exclusivamente nas Stories downstream do EPIC-086.

Não são criados endpoint, tabela, evento, fila, estado ou artifact kind. O contrato
reutiliza o OpenAPI e os schemas de Job, Attempt, JobEvent, FailureDiagnostic,
ArtifactSetManifest e ArtifactPublicationRecord já versionados.

## Fluxo congelado

1. O frontend React/TypeScript submete o job pelo cliente derivado do OpenAPI.
2. O adapter FastAPI/Pydantic chama o application service, sem acesso direto a banco,
   broker, filesystem ou regra de domínio.
3. PostgreSQL/PostGIS confirma estado autoritativo e outbox na mesma transação.
4. RabbitMQ/Celery transporta somente o TaskEnvelope mínimo.
5. O worker idempotente recarrega o estado autoritativo e executa o caso de uso.
6. O filesystem gerenciado recebe o artifact validado e hasheado; PostgreSQL preserva
   a referência, lineage e estado publicados.

A observação pública usa somente as operações congeladas
`post_projects_projectid_jobs`, `get_jobs_jobid`,
`get_attempts_attemptid_diagnostics` e
`get_artifact_sets_artifactsetid_manifest`. Progresso e transições observados derivam do
estado persistido; broker e telemetria nunca são autoridade.

O state model v1 exercita somente `queued`, `running`, `succeeded` e `failed`, estados
comuns aos contratos referenciados e suficientes ao caminho diagnóstico mínimo. Estados
adicionais não são mapeados por inferência; um consumidor deve rejeitá-los até que um
contrato compatível explicite seu uso.

## Invariantes e failure modes

- PostgreSQL/PostGIS é a única autoridade de jobs, attempts, estados, lineage e
  referências; binários publicados pertencem ao filesystem gerenciado.
- Outbox e estado são transacionais; falha do dispatcher mantém o registro persistido e
  reconciliável.
- Mensagens carregam apenas IDs, revisions, idempotency, resource class e trace context;
  raster bytes, secrets e objetos Python serializados são proibidos.
- Consumidores são idempotentes, deduplicam e toleram redelivery.
- Falha de commit não despacha nem publica artifact.
- TaskEnvelope inválido ou incompatível vai para quarantine sem execução.
- Falha do worker persiste estado explícito e referência diagnóstica.
- Falha de validação ou hash impede publicação e persiste a falha.
- Estado não suportado ou sem mapeamento explícito é rejeitado sem transição.
- Não há fallback silencioso, publicação parcial ou inferência de campo obrigatório.

## Compatibilidade, migration e rollback

O contrato usa SemVer e JSON Schema Draft 2020-12; propriedades desconhecidas são
rejeitadas. Adições opcionais compatíveis cabem na major atual. Remoção, renomeação,
mudança de tipo, relaxamento de invariante ou alteração de autoridade exige nova major e
revisão arquitetural.

Esta Story não altera schema persistido e portanto não produz migration. A implementação
downstream que materializar persistência deve usar migration versionada
expand-migrate-contract, sem migration implícita no restart, e declarar rollback antes do
contract ou estratégia forward-fix/restore.

## Rastreabilidade e prova

| AC / requisito | Implementação | Prova executável |
|---|---|---|
| `AC-ISSUE-0644-01`, `REQ-EPIC-001` | schema + exemplo com seis estágios e operações públicas | `test_executable_foundation_gate_clean_room_end_to_end` |
| `AC-ISSUE-0644-02`, `REQ-SPRINT-001-004` | manifesto com mapeamento explícito e boundaries preservados | `test_sprint_zero_baseline_decision_04` |
| `AC-ISSUE-0644-03` | política fail-closed e seis caminhos de falha | `test_walking_skeleton_fail_closed_paths` |
| `AC-ISSUE-0644-04` | manifesto, schemas/estados versionados, SemVer, authority e ownership registry | `test_epic_086_contrato` |

O executor registra a implementação candidata, mas não concede aprovação independente.
O Reviewer deve avaliar o mesmo commit candidato.
