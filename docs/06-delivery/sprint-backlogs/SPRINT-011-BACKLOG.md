# SPRINT-011 — Backlog implementável

- **Sprint:** `SPRINT-011`
- **Histórias:** `84`
- **Épicos:** `14`

## Histórias por épico

### EPIC-039 — instrumentação OpenTelemetry, correlation IDs, métricas, dashboards e alertas para API, RabbitMQ e workers

| História | Issue | Task | Papel | Dependências |
|---|---|---|---|---|
| `STORY-0232` | `ISSUE-0342` | `TASK-0232` | DevOps | STORY-0025, STORY-0081, STORY-0109, STORY-0424, STORY-0515 |
| `STORY-0233` | `ISSUE-0343` | `TASK-0233` | DevOps | STORY-0745, STORY-0746 |
| `STORY-0234` | `ISSUE-0344` | `TASK-0234` | DevOps | STORY-0232 |
| `STORY-0235` | `ISSUE-0345` | `TASK-0235` | QA | STORY-0232 |
| `STORY-0236` | `ISSUE-0346` | `TASK-0236` | Security | STORY-0233, STORY-0234, STORY-0235 |
| `STORY-0237` | `ISSUE-0347` | `TASK-0237` | Reviewer | STORY-0236 |
| `STORY-0745` | `ISSUE-0855` | `TASK-0745` | DevOps | STORY-0232 |
| `STORY-0746` | `ISSUE-0856` | `TASK-0746` | DevOps | STORY-0232 |

### EPIC-040 — benchmark, limites e orçamento de recursos

| História | Issue | Task | Papel | Dependências |
|---|---|---|---|---|
| `STORY-0238` | `ISSUE-0348` | `TASK-0238` | DevOps | STORY-0142, STORY-0237, STORY-0431, STORY-0438 |
| `STORY-0239` | `ISSUE-0349` | `TASK-0239` | DevOps | STORY-0238 |
| `STORY-0240` | `ISSUE-0350` | `TASK-0240` | DevOps | STORY-0238 |
| `STORY-0241` | `ISSUE-0351` | `TASK-0241` | QA | STORY-0238 |
| `STORY-0242` | `ISSUE-0352` | `TASK-0242` | Security | STORY-0239, STORY-0240, STORY-0241 |
| `STORY-0243` | `ISSUE-0353` | `TASK-0243` | Reviewer | STORY-0242 |

### EPIC-071 — BackupSet coordenado, manifests, checksums, watermark e policies de inclusão

| História | Issue | Task | Papel | Dependências |
|---|---|---|---|---|
| `STORY-0445` | `ISSUE-0555` | `TASK-0445` | Arquiteto | STORY-0061, STORY-0301 |
| `STORY-0446` | `ISSUE-0556` | `TASK-0446` | Backend | STORY-0445 |
| `STORY-0447` | `ISSUE-0557` | `TASK-0447` | Backend | STORY-0445 |
| `STORY-0448` | `ISSUE-0558` | `TASK-0448` | Backend | STORY-0445 |
| `STORY-0449` | `ISSUE-0559` | `TASK-0449` | Security | STORY-0446, STORY-0447, STORY-0448 |
| `STORY-0450` | `ISSUE-0560` | `TASK-0450` | Reviewer | STORY-0449 |

### EPIC-072 — restore drills isolados, evidências, RPO/RTO e runbook executável

| História | Issue | Task | Papel | Dependências |
|---|---|---|---|---|
| `STORY-0451` | `ISSUE-0561` | `TASK-0451` | DevOps | STORY-0450, STORY-0237 |
| `STORY-0452` | `ISSUE-0562` | `TASK-0452` | DevOps | STORY-0451 |
| `STORY-0453` | `ISSUE-0563` | `TASK-0453` | DevOps | STORY-0451 |
| `STORY-0454` | `ISSUE-0564` | `TASK-0454` | QA | STORY-0451 |
| `STORY-0455` | `ISSUE-0565` | `TASK-0455` | Security | STORY-0452, STORY-0453, STORY-0454 |
| `STORY-0456` | `ISSUE-0566` | `TASK-0456` | Reviewer | STORY-0455 |

### EPIC-073 — RetentionPolicy por classe/estado/dependência, holds e preview de impacto

| História | Issue | Task | Papel | Dependências |
|---|---|---|---|---|
| `STORY-0457` | `ISSUE-0567` | `TASK-0457` | Arquiteto | STORY-0301, STORY-0384 |
| `STORY-0458` | `ISSUE-0568` | `TASK-0458` | Backend | STORY-0457 |
| `STORY-0459` | `ISSUE-0569` | `TASK-0459` | Backend | STORY-0457 |
| `STORY-0460` | `ISSUE-0570` | `TASK-0460` | Backend | STORY-0457 |
| `STORY-0461` | `ISSUE-0571` | `TASK-0461` | Security | STORY-0458, STORY-0459, STORY-0460 |
| `STORY-0462` | `ISSUE-0572` | `TASK-0462` | Reviewer | STORY-0461 |

### EPIC-074 — GC reference-aware, tombstone, quarentena, período de graça e reconciliação

| História | Issue | Task | Papel | Dependências |
|---|---|---|---|---|
| `STORY-0463` | `ISSUE-0573` | `TASK-0463` | Arquiteto | STORY-0462, STORY-0301 |
| `STORY-0464` | `ISSUE-0574` | `TASK-0464` | Backend | STORY-0463 |
| `STORY-0465` | `ISSUE-0575` | `TASK-0465` | Backend | STORY-0463 |
| `STORY-0466` | `ISSUE-0576` | `TASK-0466` | Backend | STORY-0463 |
| `STORY-0467` | `ISSUE-0577` | `TASK-0467` | Security | STORY-0464, STORY-0465, STORY-0466 |
| `STORY-0468` | `ISSUE-0578` | `TASK-0468` | Reviewer | STORY-0467 |

### EPIC-075 — canal append-only de auditoria, particionamento, digests, consulta e exportação assinada opcional

| História | Issue | Task | Papel | Dependências |
|---|---|---|---|---|
| `STORY-0469` | `ISSUE-0579` | `TASK-0469` | DevOps | STORY-0055, STORY-0301, STORY-0438 |
| `STORY-0470` | `ISSUE-0580` | `TASK-0470` | DevOps | STORY-0469 |
| `STORY-0471` | `ISSUE-0581` | `TASK-0471` | DevOps | STORY-0469 |
| `STORY-0472` | `ISSUE-0582` | `TASK-0472` | QA | STORY-0469 |
| `STORY-0473` | `ISSUE-0583` | `TASK-0473` | Security | STORY-0470, STORY-0471, STORY-0472 |
| `STORY-0474` | `ISSUE-0584` | `TASK-0474` | Reviewer | STORY-0473 |

### EPIC-076 — catálogo de campos, redaction centralizada, testes de vazamento e bundles de suporte sanitizados

| História | Issue | Task | Papel | Dependências |
|---|---|---|---|---|
| `STORY-0475` | `ISSUE-0585` | `TASK-0475` | Security | STORY-0025, STORY-0237, STORY-0474 |
| `STORY-0476` | `ISSUE-0586` | `TASK-0476` | Arquiteto | STORY-0475 |
| `STORY-0477` | `ISSUE-0587` | `TASK-0477` | Backend | STORY-0475 |
| `STORY-0478` | `ISSUE-0588` | `TASK-0478` | Security | STORY-0475 |
| `STORY-0479` | `ISSUE-0589` | `TASK-0479` | DevOps | STORY-0476, STORY-0477, STORY-0478 |
| `STORY-0480` | `ISSUE-0590` | `TASK-0480` | Reviewer | STORY-0479 |

### EPIC-077 — budgets de cardinalidade, sampling, retenção por sinal e dashboards de perda/overhead

| História | Issue | Task | Papel | Dependências |
|---|---|---|---|---|
| `STORY-0481` | `ISSUE-0591` | `TASK-0481` | DevOps | STORY-0237, STORY-0462 |
| `STORY-0482` | `ISSUE-0592` | `TASK-0482` | DevOps | STORY-0481 |
| `STORY-0483` | `ISSUE-0593` | `TASK-0483` | DevOps | STORY-0481 |
| `STORY-0484` | `ISSUE-0594` | `TASK-0484` | QA | STORY-0481 |
| `STORY-0485` | `ISSUE-0595` | `TASK-0485` | Security | STORY-0482, STORY-0483, STORY-0484 |
| `STORY-0486` | `ISSUE-0596` | `TASK-0486` | Reviewer | STORY-0485 |

### EPIC-078 — contrato de secrets, setup, permissões, rotação, recuperação e adapters opcionais de vault

| História | Issue | Task | Papel | Dependências |
|---|---|---|---|---|
| `STORY-0487` | `ISSUE-0597` | `TASK-0487` | Security | STORY-0025, STORY-0040 |
| `STORY-0488` | `ISSUE-0598` | `TASK-0488` | Arquiteto | STORY-0487 |
| `STORY-0489` | `ISSUE-0599` | `TASK-0489` | Backend | STORY-0487 |
| `STORY-0490` | `ISSUE-0600` | `TASK-0490` | Security | STORY-0487 |
| `STORY-0491` | `ISSUE-0601` | `TASK-0491` | DevOps | STORY-0488, STORY-0489, STORY-0490 |
| `STORY-0492` | `ISSUE-0602` | `TASK-0492` | Reviewer | STORY-0491 |

### EPIC-079 — ingress único, TLS, redes privadas, limites e testes de exposição de portas

| História | Issue | Task | Papel | Dependências |
|---|---|---|---|---|
| `STORY-0493` | `ISSUE-0603` | `TASK-0493` | DevOps | STORY-0015, STORY-0040, STORY-0492 |
| `STORY-0494` | `ISSUE-0604` | `TASK-0494` | DevOps | STORY-0493 |
| `STORY-0495` | `ISSUE-0605` | `TASK-0495` | DevOps | STORY-0493 |
| `STORY-0496` | `ISSUE-0606` | `TASK-0496` | QA | STORY-0493 |
| `STORY-0497` | `ISSUE-0607` | `TASK-0497` | Security | STORY-0494, STORY-0495, STORY-0496 |
| `STORY-0498` | `ISSUE-0608` | `TASK-0498` | Reviewer | STORY-0497 |

### EPIC-080 — lockfiles, pins por digest/SHA, scanners, SBOM, assinatura OCI, attestations e verificador de release

| História | Issue | Task | Papel | Dependências |
|---|---|---|---|---|
| `STORY-0499` | `ISSUE-0609` | `TASK-0499` | Security | STORY-0010, STORY-0025 |
| `STORY-0500` | `ISSUE-0610` | `TASK-0500` | Arquiteto | STORY-0499 |
| `STORY-0501` | `ISSUE-0611` | `TASK-0501` | Backend | STORY-0499 |
| `STORY-0502` | `ISSUE-0612` | `TASK-0502` | Security | STORY-0499 |
| `STORY-0503` | `ISSUE-0613` | `TASK-0503` | DevOps | STORY-0500, STORY-0501, STORY-0502 |
| `STORY-0504` | `ISSUE-0614` | `TASK-0504` | Reviewer | STORY-0503 |

### EPIC-083 — modos offline/restricted/connected, egress enforcement, mirrors e testes air-gapped

| História | Issue | Task | Papel | Dependências |
|---|---|---|---|---|
| `STORY-0516` | `ISSUE-0626` | `TASK-0516` | DevOps | STORY-0498, STORY-0364, STORY-0504 |
| `STORY-0517` | `ISSUE-0627` | `TASK-0517` | DevOps | STORY-0516 |
| `STORY-0518` | `ISSUE-0628` | `TASK-0518` | DevOps | STORY-0516 |
| `STORY-0519` | `ISSUE-0629` | `TASK-0519` | QA | STORY-0516 |
| `STORY-0520` | `ISSUE-0630` | `TASK-0520` | Security | STORY-0517, STORY-0518, STORY-0519 |
| `STORY-0521` | `ISSUE-0631` | `TASK-0521` | Reviewer | STORY-0520 |

### EPIC-088 — namespace experimental/labs, registry separado, ModelPacks isolados e bloqueio técnico de ArtifactSet aceito

| História | Issue | Task | Papel | Dependências |
|---|---|---|---|---|
| `STORY-0545` | `ISSUE-0655` | `TASK-0545` | IA | STORY-0308, STORY-0504, STORY-0281 |
| `STORY-0546` | `ISSUE-0656` | `TASK-0546` | IA | STORY-0545 |
| `STORY-0547` | `ISSUE-0657` | `TASK-0547` | QA | STORY-0546 |
| `STORY-0548` | `ISSUE-0658` | `TASK-0548` | Reviewer | STORY-0547 |
