# SPRINT-002 — Backlog implementável

- **Sprint:** `SPRINT-002`
- **Histórias:** `55`
- **Épicos:** `8`

## Histórias por épico

### EPIC-008 — contas locais, bootstrap único, sessões, tokens e adapter OIDC

| História | Issue | Task | Papel | Dependências |
|---|---|---|---|---|
| `STORY-0036` | `ISSUE-0146` | `TASK-0036` | Arquiteto | STORY-0020 |
| `STORY-0037` | `ISSUE-0147` | `TASK-0037` | Backend | STORY-0712, STORY-0713 |
| `STORY-0038` | `ISSUE-0148` | `TASK-0038` | Frontend | STORY-0036 |
| `STORY-0039` | `ISSUE-0149` | `TASK-0039` | Security | STORY-0037, STORY-0038 |
| `STORY-0040` | `ISSUE-0150` | `TASK-0040` | Reviewer | STORY-0039 |
| `STORY-0712` | `ISSUE-0822` | `TASK-0712` | Backend | STORY-0036 |
| `STORY-0713` | `ISSUE-0823` | `TASK-0713` | Backend | STORY-0036 |

### EPIC-009 — usuários e papéis da instância

| História | Issue | Task | Papel | Dependências |
|---|---|---|---|---|
| `STORY-0041` | `ISSUE-0151` | `TASK-0041` | Arquiteto | STORY-0040, STORY-0025 |
| `STORY-0042` | `ISSUE-0152` | `TASK-0042` | Backend | STORY-0714, STORY-0715 |
| `STORY-0043` | `ISSUE-0153` | `TASK-0043` | Frontend | STORY-0041 |
| `STORY-0044` | `ISSUE-0154` | `TASK-0044` | Security | STORY-0042, STORY-0043 |
| `STORY-0045` | `ISSUE-0155` | `TASK-0045` | Reviewer | STORY-0044 |
| `STORY-0714` | `ISSUE-0824` | `TASK-0714` | Backend | STORY-0041 |
| `STORY-0715` | `ISSUE-0825` | `TASK-0715` | Backend | STORY-0041 |

### EPIC-010 — autorização por projeto, operação, artefato e caminho

| História | Issue | Task | Papel | Dependências |
|---|---|---|---|---|
| `STORY-0046` | `ISSUE-0156` | `TASK-0046` | Arquiteto | STORY-0045 |
| `STORY-0047` | `ISSUE-0157` | `TASK-0047` | Backend | STORY-0716, STORY-0717 |
| `STORY-0048` | `ISSUE-0158` | `TASK-0048` | Frontend | STORY-0046 |
| `STORY-0049` | `ISSUE-0159` | `TASK-0049` | Security | STORY-0047, STORY-0048 |
| `STORY-0050` | `ISSUE-0160` | `TASK-0050` | Reviewer | STORY-0049 |
| `STORY-0716` | `ISSUE-0826` | `TASK-0716` | Backend | STORY-0046 |
| `STORY-0717` | `ISSUE-0827` | `TASK-0717` | Backend | STORY-0046 |

### EPIC-011 — limites, idempotência, audit log e controles administrativos

| História | Issue | Task | Papel | Dependências |
|---|---|---|---|---|
| `STORY-0051` | `ISSUE-0161` | `TASK-0051` | Arquiteto | STORY-0050 |
| `STORY-0052` | `ISSUE-0162` | `TASK-0052` | Backend | STORY-0051 |
| `STORY-0053` | `ISSUE-0163` | `TASK-0053` | Frontend | STORY-0051 |
| `STORY-0054` | `ISSUE-0164` | `TASK-0054` | Security | STORY-0052, STORY-0053 |
| `STORY-0055` | `ISSUE-0165` | `TASK-0055` | Reviewer | STORY-0054 |

### EPIC-012 — raízes de workspace, API de navegação segura, catálogo, hashes e lineage

| História | Issue | Task | Papel | Dependências |
|---|---|---|---|---|
| `STORY-0056` | `ISSUE-0166` | `TASK-0056` | Arquiteto | STORY-0025, STORY-0050 |
| `STORY-0057` | `ISSUE-0167` | `TASK-0057` | Backend | STORY-0718, STORY-0719, STORY-0720 |
| `STORY-0058` | `ISSUE-0168` | `TASK-0058` | Backend | STORY-0056 |
| `STORY-0059` | `ISSUE-0169` | `TASK-0059` | Backend | STORY-0056 |
| `STORY-0060` | `ISSUE-0170` | `TASK-0060` | Security | STORY-0057, STORY-0058, STORY-0059 |
| `STORY-0061` | `ISSUE-0171` | `TASK-0061` | Reviewer | STORY-0060 |
| `STORY-0718` | `ISSUE-0828` | `TASK-0718` | Backend | STORY-0056 |
| `STORY-0719` | `ISSUE-0829` | `TASK-0719` | Backend | STORY-0056 |
| `STORY-0720` | `ISSUE-0830` | `TASK-0720` | Backend | STORY-0056 |

### EPIC-013 — backup/restore consistente entre banco e arquivos

| História | Issue | Task | Papel | Dependências |
|---|---|---|---|---|
| `STORY-0062` | `ISSUE-0172` | `TASK-0062` | Arquiteto | STORY-0061 |
| `STORY-0063` | `ISSUE-0173` | `TASK-0063` | Backend | STORY-0062 |
| `STORY-0064` | `ISSUE-0174` | `TASK-0064` | Backend | STORY-0062 |
| `STORY-0065` | `ISSUE-0175` | `TASK-0065` | Backend | STORY-0062 |
| `STORY-0066` | `ISSUE-0176` | `TASK-0066` | Security | STORY-0063, STORY-0064, STORY-0065 |
| `STORY-0067` | `ISSUE-0177` | `TASK-0067` | Reviewer | STORY-0066 |

### EPIC-041 — threat model validado, scanning e testes ofensivos

| História | Issue | Task | Papel | Dependências |
|---|---|---|---|---|
| `STORY-0244` | `ISSUE-0354` | `TASK-0244` | Security | STORY-0061 |
| `STORY-0245` | `ISSUE-0355` | `TASK-0245` | Arquiteto | STORY-0747, STORY-0748, STORY-0749 |
| `STORY-0246` | `ISSUE-0356` | `TASK-0246` | Backend | STORY-0244 |
| `STORY-0247` | `ISSUE-0357` | `TASK-0247` | Security | STORY-0244 |
| `STORY-0248` | `ISSUE-0358` | `TASK-0248` | DevOps | STORY-0245, STORY-0246, STORY-0247 |
| `STORY-0249` | `ISSUE-0359` | `TASK-0249` | Reviewer | STORY-0248 |
| `STORY-0747` | `ISSUE-0857` | `TASK-0747` | Arquiteto | STORY-0244 |
| `STORY-0748` | `ISSUE-0858` | `TASK-0748` | Arquiteto | STORY-0244 |
| `STORY-0749` | `ISSUE-0859` | `TASK-0749` | Arquiteto | STORY-0244 |

### EPIC-082 — preflight de hardware e ExecutionProfiles CPU/GPU/híbrido integrados ao Resource Governor

| História | Issue | Task | Papel | Dependências |
|---|---|---|---|---|
| `STORY-0511` | `ISSUE-0621` | `TASK-0511` | Arquiteto | STORY-0050 |
| `STORY-0512` | `ISSUE-0622` | `TASK-0512` | Backend | STORY-0511 |
| `STORY-0513` | `ISSUE-0623` | `TASK-0513` | Frontend | STORY-0511 |
| `STORY-0514` | `ISSUE-0624` | `TASK-0514` | Security | STORY-0512, STORY-0513 |
| `STORY-0515` | `ISSUE-0625` | `TASK-0515` | Reviewer | STORY-0514 |
