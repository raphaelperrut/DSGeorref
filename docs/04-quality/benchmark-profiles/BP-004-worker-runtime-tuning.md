# BP-004 — Worker runtime tuning

- **Status:** `Required before scale promotion`
- **Owner ADR:** ADR-036

Calibrar por workload: prefetch, worker concurrency, recycle count, memory ceiling, heartbeat/lease interval, drain timeout, backoff e queue capacity. Os testes incluem redelivery, worker crash, native leak, broker interruption, poison message, cancellation e scale gate 1→10→40→300.
