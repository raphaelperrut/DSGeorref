# SPRINT-003 — Backlog implementável

- **Sprint:** `SPRINT-003`
- **Histórias:** `49`
- **Épicos:** `7`

## Histórias por épico

### EPIC-014 — modelo de job e máquina de estados no PostgreSQL

| História | Issue | Task | Papel | Dependências |
|---|---|---|---|---|
| `STORY-0068` | `ISSUE-0178` | `TASK-0068` | Arquiteto | STORY-0020, STORY-0025 |
| `STORY-0069` | `ISSUE-0179` | `TASK-0069` | Backend | STORY-0721, STORY-0722 |
| `STORY-0070` | `ISSUE-0180` | `TASK-0070` | Backend | STORY-0068 |
| `STORY-0071` | `ISSUE-0181` | `TASK-0071` | Backend | STORY-0068 |
| `STORY-0072` | `ISSUE-0182` | `TASK-0072` | DevOps | STORY-0068 |
| `STORY-0073` | `ISSUE-0183` | `TASK-0073` | QA | STORY-0069, STORY-0070, STORY-0071, STORY-0072 |
| `STORY-0074` | `ISSUE-0184` | `TASK-0074` | Reviewer | STORY-0073 |
| `STORY-0721` | `ISSUE-0831` | `TASK-0721` | Backend | STORY-0068 |
| `STORY-0722` | `ISSUE-0832` | `TASK-0722` | Backend | STORY-0068 |

### EPIC-015 — runner direto e Celery/RabbitMQ sobre o mesmo núcleo

| História | Issue | Task | Papel | Dependências |
|---|---|---|---|---|
| `STORY-0075` | `ISSUE-0185` | `TASK-0075` | Arquiteto | STORY-0074 |
| `STORY-0076` | `ISSUE-0186` | `TASK-0076` | Backend | STORY-0075 |
| `STORY-0077` | `ISSUE-0187` | `TASK-0077` | Backend | STORY-0075 |
| `STORY-0078` | `ISSUE-0188` | `TASK-0078` | Backend | STORY-0075 |
| `STORY-0079` | `ISSUE-0189` | `TASK-0079` | DevOps | STORY-0075 |
| `STORY-0080` | `ISSUE-0190` | `TASK-0080` | QA | STORY-0076, STORY-0077, STORY-0078, STORY-0079 |
| `STORY-0081` | `ISSUE-0191` | `TASK-0081` | Reviewer | STORY-0080 |

### EPIC-016 — retries, redelivery, cancelamento, retomada e idempotência

| História | Issue | Task | Papel | Dependências |
|---|---|---|---|---|
| `STORY-0082` | `ISSUE-0192` | `TASK-0082` | Arquiteto | STORY-0081 |
| `STORY-0083` | `ISSUE-0193` | `TASK-0083` | Backend | STORY-0082 |
| `STORY-0084` | `ISSUE-0194` | `TASK-0084` | Backend | STORY-0082 |
| `STORY-0085` | `ISSUE-0195` | `TASK-0085` | Backend | STORY-0082 |
| `STORY-0086` | `ISSUE-0196` | `TASK-0086` | DevOps | STORY-0082 |
| `STORY-0087` | `ISSUE-0197` | `TASK-0087` | QA | STORY-0083, STORY-0084, STORY-0085, STORY-0086 |
| `STORY-0088` | `ISSUE-0198` | `TASK-0088` | Reviewer | STORY-0087 |

### EPIC-017 — REST, SSE e polling de reconciliação com contratos versionados

| História | Issue | Task | Papel | Dependências |
|---|---|---|---|---|
| `STORY-0089` | `ISSUE-0199` | `TASK-0089` | Arquiteto | STORY-0074 |
| `STORY-0090` | `ISSUE-0200` | `TASK-0090` | Backend | STORY-0089 |
| `STORY-0091` | `ISSUE-0201` | `TASK-0091` | Backend | STORY-0089 |
| `STORY-0092` | `ISSUE-0202` | `TASK-0092` | Backend | STORY-0089 |
| `STORY-0093` | `ISSUE-0203` | `TASK-0093` | DevOps | STORY-0089 |
| `STORY-0094` | `ISSUE-0204` | `TASK-0094` | QA | STORY-0090, STORY-0091, STORY-0092, STORY-0093 |
| `STORY-0095` | `ISSUE-0205` | `TASK-0095` | Reviewer | STORY-0094 |

### EPIC-018 — batch hierárquico, chunking, backpressure, checkpoints e retomada para lotes usuais de 40–300 imagens

| História | Issue | Task | Papel | Dependências |
|---|---|---|---|---|
| `STORY-0096` | `ISSUE-0206` | `TASK-0096` | Arquiteto | STORY-0081, STORY-0088, STORY-0061 |
| `STORY-0097` | `ISSUE-0207` | `TASK-0097` | Backend | STORY-0096 |
| `STORY-0098` | `ISSUE-0208` | `TASK-0098` | Backend | STORY-0096 |
| `STORY-0099` | `ISSUE-0209` | `TASK-0099` | Backend | STORY-0096 |
| `STORY-0100` | `ISSUE-0210` | `TASK-0100` | DevOps | STORY-0096 |
| `STORY-0101` | `ISSUE-0211` | `TASK-0101` | QA | STORY-0097, STORY-0098, STORY-0099, STORY-0100 |
| `STORY-0102` | `ISSUE-0212` | `TASK-0102` | Reviewer | STORY-0101 |

### EPIC-019 — Resource Governor, admission control e orçamento adaptativo de RAM/CPU/GPU/disco

| História | Issue | Task | Papel | Dependências |
|---|---|---|---|---|
| `STORY-0103` | `ISSUE-0213` | `TASK-0103` | Arquiteto | STORY-0102 |
| `STORY-0104` | `ISSUE-0214` | `TASK-0104` | Backend | STORY-0103 |
| `STORY-0105` | `ISSUE-0215` | `TASK-0105` | Backend | STORY-0103 |
| `STORY-0106` | `ISSUE-0216` | `TASK-0106` | Backend | STORY-0103 |
| `STORY-0107` | `ISSUE-0217` | `TASK-0107` | DevOps | STORY-0103 |
| `STORY-0108` | `ISSUE-0218` | `TASK-0108` | QA | STORY-0104, STORY-0105, STORY-0106, STORY-0107 |
| `STORY-0109` | `ISSUE-0219` | `TASK-0109` | Reviewer | STORY-0108 |

### EPIC-020 — CLI estável para projetos, ingestão, jobs e resultados

| História | Issue | Task | Papel | Dependências |
|---|---|---|---|---|
| `STORY-0110` | `ISSUE-0220` | `TASK-0110` | Arquiteto | STORY-0081, STORY-0061 |
| `STORY-0111` | `ISSUE-0221` | `TASK-0111` | Backend | STORY-0110 |
| `STORY-0112` | `ISSUE-0222` | `TASK-0112` | Backend | STORY-0110 |
| `STORY-0113` | `ISSUE-0223` | `TASK-0113` | QA | STORY-0111, STORY-0112 |
| `STORY-0114` | `ISSUE-0224` | `TASK-0114` | Reviewer | STORY-0113 |
