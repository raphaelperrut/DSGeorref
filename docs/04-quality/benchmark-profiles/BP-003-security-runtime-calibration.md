# BP-003 — Security runtime calibration

- **Status:** `Required before production-like readiness`
- **Owner ADR:** ADR-028

Calibrar Argon2id, limites de concorrência, atraso progressivo, janelas, cooldowns, session idle/absolute timeout e thresholds de lockout sob hardware mínimo suportado e threat tests. A promoção deve demonstrar resistência a brute force e ausência de DoS operacional por consumo de memória/CPU.
