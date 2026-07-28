# SPRINT-006 — Backlog implementável

- **Sprint:** `SPRINT-006`
- **Histórias:** `86`
- **Épicos:** `12`

## Histórias por épico

### EPIC-050 — registry de matchers clássicos/IA, escalonamento explicável, licenças, manifests e benchmark

| História | Issue | Task | Papel | Dependências |
|---|---|---|---|---|
| `STORY-0302` | `ISSUE-0412` | `TASK-0302` | Arquiteto | STORY-0121, STORY-0288, STORY-0020 |
| `STORY-0303` | `ISSUE-0413` | `TASK-0303` | Geoprocessamento | STORY-0750, STORY-0751 |
| `STORY-0304` | `ISSUE-0414` | `TASK-0304` | Geoprocessamento | STORY-0302 |
| `STORY-0305` | `ISSUE-0415` | `TASK-0305` | Geoprocessamento | STORY-0302 |
| `STORY-0306` | `ISSUE-0416` | `TASK-0306` | Geoprocessamento | STORY-0302 |
| `STORY-0307` | `ISSUE-0417` | `TASK-0307` | QA | STORY-0303, STORY-0304, STORY-0305, STORY-0306 |
| `STORY-0308` | `ISSUE-0418` | `TASK-0308` | Reviewer | STORY-0307 |
| `STORY-0750` | `ISSUE-0860` | `TASK-0750` | Geoprocessamento | STORY-0302 |
| `STORY-0751` | `ISSUE-0861` | `TASK-0751` | Geoprocessamento | STORY-0302 |

### EPIC-051 — estimadores USAC_MAGSAC/RANSAC explícitos, calibração, proveniência e testes de compatibilidade

| História | Issue | Task | Papel | Dependências |
|---|---|---|---|---|
| `STORY-0309` | `ISSUE-0419` | `TASK-0309` | Arquiteto | STORY-0121, STORY-0135, STORY-0149 |
| `STORY-0310` | `ISSUE-0420` | `TASK-0310` | Geoprocessamento | STORY-0309 |
| `STORY-0311` | `ISSUE-0421` | `TASK-0311` | Geoprocessamento | STORY-0309 |
| `STORY-0312` | `ISSUE-0422` | `TASK-0312` | Geoprocessamento | STORY-0309 |
| `STORY-0313` | `ISSUE-0423` | `TASK-0313` | Geoprocessamento | STORY-0309 |
| `STORY-0314` | `ISSUE-0424` | `TASK-0314` | QA | STORY-0310, STORY-0311, STORY-0312, STORY-0313 |
| `STORY-0315` | `ISSUE-0425` | `TASK-0315` | Reviewer | STORY-0314 |

### EPIC-052 — seleção de GCPs por cobertura/qualidade/diversidade, exportando pontos usados e descartados

| História | Issue | Task | Papel | Dependências |
|---|---|---|---|---|
| `STORY-0316` | `ISSUE-0426` | `TASK-0316` | Arquiteto | STORY-0135, STORY-0274, STORY-0315 |
| `STORY-0317` | `ISSUE-0427` | `TASK-0317` | Geoprocessamento | STORY-0316 |
| `STORY-0318` | `ISSUE-0428` | `TASK-0318` | Geoprocessamento | STORY-0316 |
| `STORY-0319` | `ISSUE-0429` | `TASK-0319` | Geoprocessamento | STORY-0316 |
| `STORY-0320` | `ISSUE-0430` | `TASK-0320` | Geoprocessamento | STORY-0316 |
| `STORY-0321` | `ISSUE-0431` | `TASK-0321` | QA | STORY-0317, STORY-0318, STORY-0319, STORY-0320 |
| `STORY-0322` | `ISSUE-0432` | `TASK-0322` | Reviewer | STORY-0321 |

### EPIC-053 — grafo de referências verificadas, componentes desconectados, invalidação e retry por componente

| História | Issue | Task | Papel | Dependências |
|---|---|---|---|---|
| `STORY-0323` | `ISSUE-0433` | `TASK-0323` | Arquiteto | STORY-0128, STORY-0135, STORY-0142, STORY-0322 |
| `STORY-0324` | `ISSUE-0434` | `TASK-0324` | Geoprocessamento | STORY-0323 |
| `STORY-0325` | `ISSUE-0435` | `TASK-0325` | Geoprocessamento | STORY-0323 |
| `STORY-0326` | `ISSUE-0436` | `TASK-0326` | Geoprocessamento | STORY-0323 |
| `STORY-0327` | `ISSUE-0437` | `TASK-0327` | Geoprocessamento | STORY-0323 |
| `STORY-0328` | `ISSUE-0438` | `TASK-0328` | QA | STORY-0324, STORY-0325, STORY-0326, STORY-0327 |
| `STORY-0329` | `ISSUE-0439` | `TASK-0329` | Reviewer | STORY-0328 |

### EPIC-054 — componentes provisórios multimodais, scores versionados, preview e correção sem equivalência com prova geométrica

| História | Issue | Task | Papel | Dependências |
|---|---|---|---|---|
| `STORY-0330` | `ISSUE-0440` | `TASK-0330` | Arquiteto | STORY-0121, STORY-0061, STORY-0329 |
| `STORY-0331` | `ISSUE-0441` | `TASK-0331` | Geoprocessamento | STORY-0330 |
| `STORY-0332` | `ISSUE-0442` | `TASK-0332` | Geoprocessamento | STORY-0330 |
| `STORY-0333` | `ISSUE-0443` | `TASK-0333` | Geoprocessamento | STORY-0330 |
| `STORY-0334` | `ISSUE-0444` | `TASK-0334` | Geoprocessamento | STORY-0330 |
| `STORY-0335` | `ISSUE-0445` | `TASK-0335` | QA | STORY-0331, STORY-0332, STORY-0333, STORY-0334 |
| `STORY-0336` | `ISSUE-0446` | `TASK-0336` | Reviewer | STORY-0335 |

### EPIC-055 — recuperação progressiva de vizinhos com candidate budget, telemetria de recall e retry ampliado explícito

| História | Issue | Task | Papel | Dependências |
|---|---|---|---|---|
| `STORY-0337` | `ISSUE-0447` | `TASK-0337` | Arquiteto | STORY-0288, STORY-0308, STORY-0336, STORY-0109 |
| `STORY-0338` | `ISSUE-0448` | `TASK-0338` | Geoprocessamento | STORY-0337 |
| `STORY-0339` | `ISSUE-0449` | `TASK-0339` | Geoprocessamento | STORY-0337 |
| `STORY-0340` | `ISSUE-0450` | `TASK-0340` | Geoprocessamento | STORY-0337 |
| `STORY-0341` | `ISSUE-0451` | `TASK-0341` | Geoprocessamento | STORY-0337 |
| `STORY-0342` | `ISSUE-0452` | `TASK-0342` | QA | STORY-0338, STORY-0339, STORY-0340, STORY-0341 |
| `STORY-0343` | `ISSUE-0453` | `TASK-0343` | Reviewer | STORY-0342 |

### EPIC-056 — máquina de estados de arestas, evidência direta, lineage e SGV independente da imagem dependente

| História | Issue | Task | Papel | Dependências |
|---|---|---|---|---|
| `STORY-0344` | `ISSUE-0454` | `TASK-0344` | Arquiteto | STORY-0135, STORY-0142, STORY-0322, STORY-0329 |
| `STORY-0345` | `ISSUE-0455` | `TASK-0345` | Geoprocessamento | STORY-0344 |
| `STORY-0346` | `ISSUE-0456` | `TASK-0346` | Geoprocessamento | STORY-0344 |
| `STORY-0347` | `ISSUE-0457` | `TASK-0347` | Geoprocessamento | STORY-0344 |
| `STORY-0348` | `ISSUE-0458` | `TASK-0348` | Geoprocessamento | STORY-0344 |
| `STORY-0349` | `ISSUE-0459` | `TASK-0349` | QA | STORY-0345, STORY-0346, STORY-0347, STORY-0348 |
| `STORY-0350` | `ISSUE-0460` | `TASK-0350` | Reviewer | STORY-0349 |

### EPIC-057 — resultados por componente, sucesso parcial explícito, retry por subconjunto e UX de componentes não resolvidos

| História | Issue | Task | Papel | Dependências |
|---|---|---|---|---|
| `STORY-0351` | `ISSUE-0461` | `TASK-0351` | Arquiteto | STORY-0329, STORY-0350, STORY-0184 |
| `STORY-0352` | `ISSUE-0462` | `TASK-0352` | Geoprocessamento | STORY-0351 |
| `STORY-0353` | `ISSUE-0463` | `TASK-0353` | Geoprocessamento | STORY-0351 |
| `STORY-0354` | `ISSUE-0464` | `TASK-0354` | Geoprocessamento | STORY-0351 |
| `STORY-0355` | `ISSUE-0465` | `TASK-0355` | Geoprocessamento | STORY-0351 |
| `STORY-0356` | `ISSUE-0466` | `TASK-0356` | QA | STORY-0352, STORY-0353, STORY-0354, STORY-0355 |
| `STORY-0357` | `ISSUE-0467` | `TASK-0357` | Reviewer | STORY-0356 |

### EPIC-058 — gateway por capacidades, adapters STAC/API oficial, testes de contrato, allowlist, SSRF/egress e estados de licença/disponibilidade

| História | Issue | Task | Papel | Dependências |
|---|---|---|---|---|
| `STORY-0358` | `ISSUE-0468` | `TASK-0358` | Arquiteto | STORY-0163, STORY-0020, STORY-0249 |
| `STORY-0359` | `ISSUE-0469` | `TASK-0359` | Geoprocessamento | STORY-0358 |
| `STORY-0360` | `ISSUE-0470` | `TASK-0360` | Geoprocessamento | STORY-0358 |
| `STORY-0361` | `ISSUE-0471` | `TASK-0361` | Geoprocessamento | STORY-0358 |
| `STORY-0362` | `ISSUE-0472` | `TASK-0362` | Geoprocessamento | STORY-0358 |
| `STORY-0363` | `ISSUE-0473` | `TASK-0363` | QA | STORY-0359, STORY-0360, STORY-0361, STORY-0362 |
| `STORY-0364` | `ISSUE-0474` | `TASK-0364` | Reviewer | STORY-0363 |

### EPIC-059 — busca espaciotemporal guiada, ranking explicável, incerteza e expansão limitada por orçamento

| História | Issue | Task | Papel | Dependências |
|---|---|---|---|---|
| `STORY-0365` | `ISSUE-0475` | `TASK-0365` | Arquiteto | STORY-0364, STORY-0128 |
| `STORY-0366` | `ISSUE-0476` | `TASK-0366` | Geoprocessamento | STORY-0365 |
| `STORY-0367` | `ISSUE-0477` | `TASK-0367` | Geoprocessamento | STORY-0365 |
| `STORY-0368` | `ISSUE-0478` | `TASK-0368` | Geoprocessamento | STORY-0365 |
| `STORY-0369` | `ISSUE-0479` | `TASK-0369` | Geoprocessamento | STORY-0365 |
| `STORY-0370` | `ISSUE-0480` | `TASK-0370` | QA | STORY-0366, STORY-0367, STORY-0368, STORY-0369 |
| `STORY-0371` | `ISSUE-0481` | `TASK-0371` | Reviewer | STORY-0370 |

### EPIC-060 — policy de aquisição no ProcessingPlan, preview, consentimento e bloqueio fail-closed de ativos pagos/ambíguos

| História | Issue | Task | Papel | Dependências |
|---|---|---|---|---|
| `STORY-0372` | `ISSUE-0482` | `TASK-0372` | Arquiteto | STORY-0364, STORY-0371, STORY-0177 |
| `STORY-0373` | `ISSUE-0483` | `TASK-0373` | Geoprocessamento | STORY-0372 |
| `STORY-0374` | `ISSUE-0484` | `TASK-0374` | Geoprocessamento | STORY-0372 |
| `STORY-0375` | `ISSUE-0485` | `TASK-0375` | Geoprocessamento | STORY-0372 |
| `STORY-0376` | `ISSUE-0486` | `TASK-0376` | Geoprocessamento | STORY-0372 |
| `STORY-0377` | `ISSUE-0487` | `TASK-0377` | QA | STORY-0373, STORY-0374, STORY-0375, STORY-0376 |
| `STORY-0378` | `ISSUE-0488` | `TASK-0378` | Reviewer | STORY-0377 |

### EPIC-063 — modelo tipado/versionado de GCPs, lifecycle, proveniência e round-trip dos exports

| História | Issue | Task | Papel | Dependências |
|---|---|---|---|---|
| `STORY-0391` | `ISSUE-0501` | `TASK-0391` | Arquiteto | STORY-0322, STORY-0061 |
| `STORY-0392` | `ISSUE-0502` | `TASK-0392` | Geoprocessamento | STORY-0391 |
| `STORY-0393` | `ISSUE-0503` | `TASK-0393` | Geoprocessamento | STORY-0391 |
| `STORY-0394` | `ISSUE-0504` | `TASK-0394` | Geoprocessamento | STORY-0391 |
| `STORY-0395` | `ISSUE-0505` | `TASK-0395` | Geoprocessamento | STORY-0391 |
| `STORY-0396` | `ISSUE-0506` | `TASK-0396` | QA | STORY-0392, STORY-0393, STORY-0394, STORY-0395 |
| `STORY-0397` | `ISSUE-0507` | `TASK-0397` | Reviewer | STORY-0396 |
