# DSGeorref

O DSGeorref é um sistema e webservice Python/FastAPI voltado ao georreferenciamento de imagens antigas ou atuais que não possuem referência espacial confiável. O projeto busca transformar essas imagens em resultados verificáveis, rastreáveis e reproduzíveis, com uma arquitetura preparada para processamento individual e em lote, validação geométrica, revisão assistida e operação governada.

## Visão geral

A visão do produto combina referências raster ou tileadas, locais ou externas — incluindo MBTiles quando aplicável — com busca provável, correspondências, consenso espacial e área de interesse (AOI) explícita. A geometria resultante passa por verificação forte e fail-closed; a homografia projetiva é o modelo canônico previsto para a estimação geométrica.

O roadmap também contempla execução individual e em lote, revisão assistida, artefatos imutáveis, lineage e mecanismos de reprodução das execuções. Recursos de IA são opcionais e governados: não substituem a elegibilidade clássica, não constituem autoridade sobre a geometria e não contornam os controles ou a verificação geométrica do sistema.

Esses elementos descrevem a direção arquitetural e o produto pretendido. A baseline de engenharia está materializada no repositório, enquanto as capacidades operacionais são implementadas incrementalmente por issues e histórias autorizadas.

## Arquitetura e engenharia

O repositório reúne a baseline técnica necessária para orientar a implementação: requisitos, Domain-Driven Design, ADRs, contratos, especificações executáveis, roadmap, histórias implementáveis, TaskEnvelopes e mecanismos de assurance e gates. O runtime primário canônico é **CPython 3.12.13**.

O programa de revisão arquitetural das fases A–G está concluído conforme o [roadmap de fases](docs/06-delivery/PHASE_ROADMAP.md). Essas fases registram a construção e a revisão da baseline; não são os 12 sprints de implementação. Os pontos de entrada para a arquitetura e suas revisões são:

- [SAR — Start Here](docs/02-architecture/sar/SAR-000-START-HERE.md)
- [Roadmap de implementação](docs/06-delivery/ROADMAP.md)
- [Roadmap de fases A–G](docs/06-delivery/PHASE_ROADMAP.md)
- [Revisão dos sprints — Fase F](docs/07-assurance/PHASE-F-SPRINT-REVIEW-REPORT.md)
- [CTO Review — Fase G](docs/07-assurance/PHASE-G-CTO-REVIEW-REPORT.md)

### Estado atual

- A baseline arquitetural e o programa de revisão A–G estão concluídos.
- A implementação é conduzida de forma incremental por issues e histórias que recebem autorização formal e escopo de escrita explícito.
- A conclusão de uma issue, história ou conjunto parcial de entregas não encerra um sprint. O fechamento depende da conclusão formal do backlog, dos gates e das evidências aplicáveis ao sprint inteiro.

## Roadmap de implementação

O roadmap canônico está organizado em **12 sprints**, **110 épicos**, **761 histórias implementáveis** e **871 issues**.

Os sprints oferecem a visão temporal e macroscópica da entrega. A ordem efetiva de implementação é governada pelo DAG de dependências, pelos gates e pelos critérios de aceitação; por isso, progresso em issues individuais não implica conclusão do sprint que as contém.

## Sprints

Um checkbox marcado representa o encerramento formal do sprint inteiro, não progresso parcial. Na ausência dessa evidência canônica, o sprint permanece desmarcado.

### [ ] SPRINT-001 — Repositório, governança e fundação executável

**12 épicos · 94 histórias**

**Objetivo:** materializar a fundação de engenharia do produto: governança arquitetural, repositório, workflow e Project, contratos iniciais, monorepo, CI, migrations, checks e controles necessários ao restante da implementação.

**Resultado esperado:** uma fundação executável, reproduzível e governada sobre a qual os demais sprints possam ser implementados.

[Backlog do sprint](docs/06-delivery/sprint-backlogs/SPRINT-001-BACKLOG.md)

### [ ] SPRINT-002 — Identidade, autorização, workspace e persistência inicial

**8 épicos · 55 histórias**

**Objetivo:** estabelecer contas, sessões, identidade, autorização, papéis, workspace seguro, persistência inicial, auditoria e mecanismos fundamentais de proteção.

**Resultado esperado:** uma base segura de usuários, permissões, projetos, workspaces e armazenamento para suportar os workloads do sistema.

[Backlog do sprint](docs/06-delivery/sprint-backlogs/SPRINT-002-BACKLOG.md)

### [ ] SPRINT-003 — Jobs, runners, lote básico e CLI

**7 épicos · 49 histórias**

**Objetivo:** materializar jobs, máquina de estados, runners, execução direta e distribuída, retries, cancelamento, retomada, interfaces de acompanhamento, processamento em lote e CLI.

**Resultado esperado:** um núcleo de execução capaz de receber, executar, acompanhar e recuperar workloads individuais e em lote.

[Backlog do sprint](docs/06-delivery/sprint-backlogs/SPRINT-003-BACKLOG.md)

### [ ] SPRINT-004 — Resiliência, scheduler, replay e escala operacional

**6 épicos · 42 histórias**

**Objetivo:** fortalecer o runtime com retry técnico, checkpoints, cancelamento cooperativo, supervisão, concorrência, scheduler, observabilidade e replay.

**Resultado esperado:** execução resiliente, diagnosticável e recuperável sob concorrência e falhas.

[Backlog do sprint](docs/06-delivery/sprint-backlogs/SPRINT-004-BACKLOG.md)

### [ ] SPRINT-005 — Primeira fatia geoespacial classic-first

**15 épicos · 120 histórias**

**Objetivo:** materializar a primeira grande fatia geoespacial, incluindo corpus versionado, busca provável, correspondências, estimação geométrica robusta e os componentes classic-first do pipeline.

**Resultado esperado:** um pipeline geoespacial funcional e verificável capaz de produzir os primeiros resultados de georreferenciamento sobre corpus controlado.

[Backlog do sprint](docs/06-delivery/sprint-backlogs/SPRINT-005-BACKLOG.md)

### [ ] SPRINT-006 — Correspondências, referências, providers e revisão assistida

**12 épicos · 86 histórias**

**Objetivo:** expandir e robustecer correspondências, referências e providers, incorporando mecanismos de seleção, validação e revisão assistida.

**Resultado esperado:** maior cobertura e robustez do georreferenciamento, com referências e correspondências controladas e revisáveis.

[Backlog do sprint](docs/06-delivery/sprint-backlogs/SPRINT-006-BACKLOG.md)

### [ ] SPRINT-007 — Contratos de coordenadas, grade e mosaico relativo

**6 épicos · 42 histórias**

**Objetivo:** formalizar e implementar contratos espaciais de coordenadas, grades e relações necessárias à composição de mosaicos relativos.

**Resultado esperado:** uma base espacial consistente para relacionar múltiplas imagens e representar sua geometria relativa.

[Backlog do sprint](docs/06-delivery/sprint-backlogs/SPRINT-007-BACKLOG.md)

### [ ] SPRINT-008 — Qualidade, reporting e materialização do mosaico relativo

**5 épicos · 35 histórias**

**Objetivo:** materializar verificação, métricas, reporting, visualização, exportação, budgets e persistência do mosaico relativo.

**Resultado esperado:** mosaicos relativos verificáveis e materializados, acompanhados de evidências de qualidade e artefatos persistentes.

[Backlog do sprint](docs/06-delivery/sprint-backlogs/SPRINT-008-BACKLOG.md)

### [ ] SPRINT-009 — Frontend cartográfico, revisão e aprendizagem

**9 épicos · 58 histórias**

**Objetivo:** materializar a experiência web e cartográfica, incluindo workspace visual, configuração, acompanhamento, revisão, qualidade, assistência guiada, correções e aprendizagem.

**Resultado esperado:** uma interface operacional para configurar, acompanhar, inspecionar, compreender e revisar o processamento geoespacial.

[Backlog do sprint](docs/06-delivery/sprint-backlogs/SPRINT-009-BACKLOG.md)

### [ ] SPRINT-010 — Resultados, lineage, schemas e reprodutibilidade

**6 épicos · 38 histórias**

**Objetivo:** consolidar persistência e exportação de resultados, diagnósticos, lineage, manifests, reprodução, cache e deduplicação, snapshots e registry de schemas.

**Resultado esperado:** resultados versionados, rastreáveis e reproduzíveis, com proveniência suficiente para auditoria e comparação entre execuções.

[Backlog do sprint](docs/06-delivery/sprint-backlogs/SPRINT-010-BACKLOG.md)

### [ ] SPRINT-011 — Operações, segurança, backup, IA governada e hardening

**14 épicos · 84 histórias**

**Objetivo:** preparar o sistema para operação sustentada por meio de observabilidade, benchmarks, budgets, backup e restore, retenção e GC, auditoria, segurança, IA governada e hardening.

**Resultado esperado:** uma plataforma operacionalmente robusta, observável, recuperável e protegida, com controles explícitos para riscos técnicos e uso de IA.

[Backlog do sprint](docs/06-delivery/sprint-backlogs/SPRINT-011-BACKLOG.md)

### [ ] SPRINT-012 — Instalação, release train e publicação

**10 épicos · 58 histórias**

**Objetivo:** fechar o ciclo de entrega com instalação, upgrade e downgrade, migrations, health e smoke tests, rollback e restore, documentação, licença, milestones e release train.

**Resultado esperado:** um produto instalável, atualizável e publicável por um processo de release reproduzível, auditável e com rollback definido.

[Backlog do sprint](docs/06-delivery/sprint-backlogs/SPRINT-012-BACKLOG.md)

## Validação

Execute `make verify` como entrada principal de validação do repositório. O target reúne os checks automatizados da baseline e dos controles de arquitetura, requisitos, DDD, ADRs, especificações, sprints e fitness functions aplicáveis.

## Navegação

- [Comece pela visão arquitetural](docs/02-architecture/sar/SAR-000-START-HERE.md)
- [Consulte o roadmap de implementação](docs/06-delivery/ROADMAP.md)
- [Diferencie as fases A–G dos sprints](docs/06-delivery/PHASE_ROADMAP.md)
- [Veja a revisão dos 12 sprints](docs/07-assurance/PHASE-F-SPRINT-REVIEW-REPORT.md)
- [Veja a due diligence técnica final](docs/07-assurance/PHASE-G-CTO-REVIEW-REPORT.md)
