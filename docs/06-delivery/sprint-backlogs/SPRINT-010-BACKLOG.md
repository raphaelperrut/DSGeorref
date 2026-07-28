# SPRINT-010 — Backlog implementável

- **Sprint:** `SPRINT-010`
- **Histórias:** `38`
- **Épicos:** `6`

## Histórias por épico

### EPIC-037 — persistência e exportação escalável de resultados por imagem/lote, geometrias, manifestos e checksums

| História | Issue | Task | Papel | Dependências |
|---|---|---|---|---|
| `STORY-0220` | `ISSUE-0330` | `TASK-0220` | Arquiteto | STORY-0061, STORY-0156, STORY-0184, STORY-0397 |
| `STORY-0221` | `ISSUE-0331` | `TASK-0221` | Backend | STORY-0743, STORY-0744 |
| `STORY-0222` | `ISSUE-0332` | `TASK-0222` | Backend | STORY-0220 |
| `STORY-0223` | `ISSUE-0333` | `TASK-0223` | Frontend | STORY-0220 |
| `STORY-0224` | `ISSUE-0334` | `TASK-0224` | QA | STORY-0221, STORY-0222, STORY-0223 |
| `STORY-0225` | `ISSUE-0335` | `TASK-0225` | Reviewer | STORY-0224 |
| `STORY-0743` | `ISSUE-0853` | `TASK-0743` | Backend | STORY-0220 |
| `STORY-0744` | `ISSUE-0854` | `TASK-0744` | Backend | STORY-0220 |

### EPIC-038 — métricas, heatmap amostrado e diagnóstico denso do Image Deformation Profile

| História | Issue | Task | Papel | Dependências |
|---|---|---|---|---|
| `STORY-0226` | `ISSUE-0336` | `TASK-0226` | Arquiteto | STORY-0142, STORY-0225 |
| `STORY-0227` | `ISSUE-0337` | `TASK-0227` | Backend | STORY-0226 |
| `STORY-0228` | `ISSUE-0338` | `TASK-0228` | Backend | STORY-0226 |
| `STORY-0229` | `ISSUE-0339` | `TASK-0229` | Frontend | STORY-0226 |
| `STORY-0230` | `ISSUE-0340` | `TASK-0230` | QA | STORY-0227, STORY-0228, STORY-0229 |
| `STORY-0231` | `ISSUE-0341` | `TASK-0231` | Reviewer | STORY-0230 |

### EPIC-049 — lineage normalizado, manifestos e bundle de reprodução sob demanda

| História | Issue | Task | Papel | Dependências |
|---|---|---|---|---|
| `STORY-0296` | `ISSUE-0406` | `TASK-0296` | Arquiteto | STORY-0020, STORY-0061, STORY-0281, STORY-0390, STORY-0397, STORY-0417 |
| `STORY-0297` | `ISSUE-0407` | `TASK-0297` | Backend | STORY-0296 |
| `STORY-0298` | `ISSUE-0408` | `TASK-0298` | Backend | STORY-0296 |
| `STORY-0299` | `ISSUE-0409` | `TASK-0299` | Backend | STORY-0296 |
| `STORY-0300` | `ISSUE-0410` | `TASK-0300` | Security | STORY-0297, STORY-0298, STORY-0299 |
| `STORY-0301` | `ISSUE-0411` | `TASK-0301` | Reviewer | STORY-0300 |

### EPIC-061 — cache endereçado por conteúdo, deduplicação, quotas, retention, licença, GC e proteção de lineage

| História | Issue | Task | Papel | Dependências |
|---|---|---|---|---|
| `STORY-0379` | `ISSUE-0489` | `TASK-0379` | Arquiteto | STORY-0061, STORY-0301, STORY-0364 |
| `STORY-0380` | `ISSUE-0490` | `TASK-0380` | Backend | STORY-0379 |
| `STORY-0381` | `ISSUE-0491` | `TASK-0381` | Backend | STORY-0379 |
| `STORY-0382` | `ISSUE-0492` | `TASK-0382` | Backend | STORY-0379 |
| `STORY-0383` | `ISSUE-0493` | `TASK-0383` | Security | STORY-0380, STORY-0381, STORY-0382 |
| `STORY-0384` | `ISSUE-0494` | `TASK-0384` | Reviewer | STORY-0383 |

### EPIC-070 — snapshots imutáveis, regra de resultado vigente e comparação entre ciclos

| História | Issue | Task | Papel | Dependências |
|---|---|---|---|---|
| `STORY-0439` | `ISSUE-0549` | `TASK-0439` | Arquiteto | STORY-0225, STORY-0301, STORY-0390 |
| `STORY-0440` | `ISSUE-0550` | `TASK-0440` | Backend | STORY-0439 |
| `STORY-0441` | `ISSUE-0551` | `TASK-0441` | Backend | STORY-0439 |
| `STORY-0442` | `ISSUE-0552` | `TASK-0442` | Frontend | STORY-0439 |
| `STORY-0443` | `ISSUE-0553` | `TASK-0443` | QA | STORY-0440, STORY-0441, STORY-0442 |
| `STORY-0444` | `ISSUE-0554` | `TASK-0444` | Reviewer | STORY-0443 |

### EPIC-105 — Registry de schemas e compatibilidade de artifacts

| História | Issue | Task | Papel | Dependências |
|---|---|---|---|---|
| `STORY-0654` | `ISSUE-0764` | `TASK-0654` | Arquiteto | — |
| `STORY-0655` | `ISSUE-0765` | `TASK-0655` | Backend | STORY-0654 |
| `STORY-0656` | `ISSUE-0766` | `TASK-0656` | Backend | STORY-0654 |
| `STORY-0657` | `ISSUE-0767` | `TASK-0657` | Backend | STORY-0654 |
| `STORY-0658` | `ISSUE-0768` | `TASK-0658` | Security | STORY-0655, STORY-0656, STORY-0657 |
| `STORY-0659` | `ISSUE-0769` | `TASK-0659` | Reviewer | STORY-0658 |
