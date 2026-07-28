# AP-005 — Managed filesystem operational profile

- **Status:** `Accepted`
- **Owner ADR:** ADR-018

## Profile inicial

- roots funcionais: originals, staging, published, cache e quarantine;
- SHA-256 é digest normativo; digest auxiliar somente se comprovado;
- scrubbing por risco e reconciliação PostgreSQL/manifest/filesystem;
- names/Unicode/path budget e owner/modes/ACLs são definidos nas issues STORY-0058 / ISSUE-0168 e STORY-0060 / ISSUE-0170;
- qualquer filesystem não local exige capability probe e evidence antes de ser habilitado.
