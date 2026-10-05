# AP-003 — Web security runtime profile

- **Status:** `Accepted`
- **Owner ADR:** ADR-028
- **Calibration:** BP-003

## Profile operacional

Define schemas de sessão, stores, cookies, headers, audit events, recovery material e controles de exposição que implementam a ADR-028. Valores numéricos de Argon2id, throttling, cooldown, idle/absolute timeout e limites de concorrência são promovidos somente após BP-003 e permanecem versionados.

Nenhum parâmetro pode reduzir os pisos de segurança, permitir enumeração de contas ou contornar autorização/CSRF.

## Replay key — decisão explícita do Project Owner, ISSUE-0149

A `replay_key` de `IdentityTransactions`, usada no fingerprint HMAC-SHA-256, deve
conter no mínimo **32 bytes (256 bits)** de material secreto. Quando gerada pelo
sistema, deve usar CSPRNG, como `secrets` do Python. Comprimento abaixo do piso é
configuração insegura e bloqueia a inicialização fail-closed; não se estima a
entropia de uma chave individual em runtime.

Este parâmetro operacional reversível aplica-se ao controle de secrets de
REQ-EPIC-076 / ADR-032 no consumidor de identidade existente. A decisão do
Project Owner fixa o piso, sem derivá-lo do tamanho usado pelo gerador existente.
