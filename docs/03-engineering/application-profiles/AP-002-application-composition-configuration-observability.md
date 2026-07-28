# AP-002 — Application composition, configuration and observability

- **Status:** `Accepted`
- **Owner ADR:** ADR-002

## Profile

- namespace `dsgeorref` com packages criados somente quando houver responsabilidade e primeiro teste;
- composition roots finos e constructor injection;
- settings tipados em camadas, fail-closed e com visão sanitizada no doctor;
- logging estruturado com request/job/attempt/work-unit context e redaction;
- registry local de capabilities e feature flags, com owner, default seguro, expiração e audit trail.

A árvore exata do scaffold é especificada em STORY-0012 / ISSUE-0122 e pode evoluir sem decisão do Owner, respeitando dependency rules e a ADR-002.
