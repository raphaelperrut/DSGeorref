# AP-003 — Web security runtime profile

- **Status:** `Accepted`
- **Owner ADR:** ADR-028
- **Calibration:** BP-003

## Profile operacional

Define schemas de sessão, stores, cookies, headers, audit events, recovery material e controles de exposição que implementam a ADR-028. Valores numéricos de Argon2id, throttling, cooldown, idle/absolute timeout e limites de concorrência são promovidos somente após BP-003 e permanecem versionados.

Nenhum parâmetro pode reduzir os pisos de segurança, permitir enumeração de contas ou contornar autorização/CSRF.
