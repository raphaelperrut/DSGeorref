# Registro de correções e dependências de integração

Este registro separa **hard blockers**, que pertencem ao DAG executável, de relações de integração ou validação que não devem impedir o início de uma história.

| Relação original | Disposição | Relação corrigida | Racional |
|---|---|---|---|
| `EPIC-039 → EPIC-082` | `DIRECTION_CORRECTED` | `EPIC-082 → EPIC-039` | A implementação consumidora deve depender do contrato/capacidade provedora, não o inverso. |
| `EPIC-033 → EPIC-059` | `DIRECTION_CORRECTED` | `EPIC-059 → EPIC-033` | A implementação consumidora deve depender do contrato/capacidade provedora, não o inverso. |
| `EPIC-049 → EPIC-063` | `DIRECTION_CORRECTED` | `EPIC-063 → EPIC-049` | A implementação consumidora deve depender do contrato/capacidade provedora, não o inverso. |
| `EPIC-037 → EPIC-063` | `DIRECTION_CORRECTED` | `EPIC-063 → EPIC-037` | A implementação consumidora deve depender do contrato/capacidade provedora, não o inverso. |
| `EPIC-031 → EPIC-017` | `DIRECTION_CORRECTED` | `EPIC-017 → EPIC-031` | A implementação consumidora deve depender do contrato/capacidade provedora, não o inverso. |
| `EPIC-030 → EPIC-065` | `SOFT_INTEGRATION` | `Integração antes do gate; sem hard blocker` | A taxonomia de retry pode iniciar com invariantes de runtime; deve reconciliar a taxonomia de falhas antes do gate de integração, sem bloquear o início. |
| `EPIC-049 → EPIC-066` | `DIRECTION_CORRECTED` | `EPIC-066 → EPIC-049` | A implementação consumidora deve depender do contrato/capacidade provedora, não o inverso. |
| `EPIC-027 → EPIC-041` | `DIRECTION_CORRECTED` | `EPIC-041 → EPIC-027` | A implementação consumidora deve depender do contrato/capacidade provedora, não o inverso. |
| `EPIC-040 → EPIC-069` | `DIRECTION_CORRECTED` | `EPIC-069 → EPIC-040` | A implementação consumidora deve depender do contrato/capacidade provedora, não o inverso. |
| `EPIC-075 → EPIC-069` | `DIRECTION_CORRECTED` | `EPIC-069 → EPIC-075` | A implementação consumidora deve depender do contrato/capacidade provedora, não o inverso. |
| `EPIC-034 → EPIC-069` | `DIRECTION_CORRECTED` | `EPIC-069 → EPIC-034` | A implementação consumidora deve depender do contrato/capacidade provedora, não o inverso. |
| `EPIC-034 → EPIC-057` | `DIRECTION_CORRECTED` | `EPIC-057 → EPIC-034` | A implementação consumidora deve depender do contrato/capacidade provedora, não o inverso. |
| `EPIC-039 → EPIC-067` | `DIRECTION_CORRECTED` | `EPIC-067 → EPIC-039` | A implementação consumidora deve depender do contrato/capacidade provedora, não o inverso. |
| `EPIC-040 → EPIC-068` | `DIRECTION_CORRECTED` | `EPIC-068 → EPIC-040` | A implementação consumidora deve depender do contrato/capacidade provedora, não o inverso. |
| `EPIC-049 → EPIC-062` | `DIRECTION_CORRECTED` | `EPIC-062 → EPIC-049` | A implementação consumidora deve depender do contrato/capacidade provedora, não o inverso. |
| `EPIC-039 → EPIC-019` | `DIRECTION_CORRECTED` | `EPIC-019 → EPIC-039` | A implementação consumidora deve depender do contrato/capacidade provedora, não o inverso. |
