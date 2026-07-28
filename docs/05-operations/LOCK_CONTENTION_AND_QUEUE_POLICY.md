# Locks, contenção e filas — baseline 3.0

A política normativa está em `contracts/operations/lock-and-queue-policy.yaml`.

## Regras críticas

- ordem global de locks obrigatória;
- transações curtas e sem I/O externo;
- timeout de lock distinto para interativo e batch;
- leases cross-process com fencing;
- ack do broker somente após commit autoritativo;
- mensagens limitadas a 256 KiB e sem binaries, secrets ou paths absolutos;
- prefetch inicial 1 até promoção por BP-004;
- fila é observada por idade da mensagem mais antiga, não somente por quantidade;
- retry esgotado termina em quarantine, sem loop infinito.

Qualquer implementação que dependa de lock não inventariado ou fila ad hoc falha na revisão.
