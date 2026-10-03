# Protocolo de integração

1. Congelar e integrar a revisão contratual.
2. Regenerar clientes e bindings de schema.
3. Executar lanes sobre o mesmo digest de contrato.
4. Integrar domínio e migrations antes dos adapters.
5. Executar suites de integração e E2E em ambiente limpo.
6. Produzir evidência imutável de QA.
7. Executar final review no commit candidato exato.
8. Autoridade humana integra somente o commit revisado.

Rebase ou mudança de código após QA invalida evidências de QA e final review.

## Entrega parcial compartilhada — ADR-006 / SAR-120

Registry e TaskEnvelope 1.7.0 distinguem delivery gates de predecessores Story→Story.
Entrega parcial não conclui owner Story. O owner produz AcceptanceManifest com hashes
de outputs/checks; QA e Reviewer aprovam o mesmo candidate e snapshot do envelope,
incluindo `acceptance_manifest_sha256`, pelo DAA existente. Não modificar trust DAA.
Autoridade humana integra o candidate revisado e registra IntegrationReceipt com
referências/digests de manifest, snapshot, evidências DAA e registro HUMAN_MERGE.
O consumer base deve conter o integration commit na baseline exigida. Branch, PR ou
cherry-pick isolado não satisfazem gate; definição alterada invalida satisfação.
Evidências ficam em `evidence/delivery-gates/<gate_id>/<candidate_sha>/` e são lidas
do Git; satisfação é calculada fail-closed, jamais escrita como booleano de aprovação.
Executar o modo `--ready-task <TASK-ID> --consumer-base <SHA>` antes de abrir o consumer.
