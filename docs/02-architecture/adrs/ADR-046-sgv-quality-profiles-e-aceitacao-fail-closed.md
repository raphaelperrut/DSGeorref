# ADR-046 — SGV, Quality Profiles e aceitação fail-closed

- **Status:** `Accepted`
- **Baseline:** `SAR v2.8 — Fase E`
- **Aprovador:** `Project Owner`
- **Owner normativo:** `ADR-046`
- **Boundary independente:** `SIM`
- **Decisões em aberto:** `Nenhuma`
- **Bounded Contexts:** `BC-007` — Verificação Geométrica e Qualidade, `BC-012` — Resultados, Diagnósticos e Exportação

## Contexto

Esta ADR isola uma decisão arquitetural de alto impacto e alto custo de reversão. Ela substitui agrupamentos amplos da baseline anterior e possui responsabilidade normativa exclusiva sobre o boundary descrito no título.

## Decisão

- Todo resultado final passa por Strong Geometric Verifier independente da estratégia produtora.
- Métrica crítica ausente, inválida ou inconsistente bloqueia aceitação automática.
- SGVProfile e QualityProfile são imutáveis, versionados e promovidos por evidência.
- Hard gates não admitem override; zona cinzenta produz reviewable, nunca accepted.

## Invariantes

- nenhuma implementação pode criar uma segunda autoridade para este boundary;
- parâmetros quantitativos permanecem em Application Profiles ou Benchmark Profiles;
- detalhes locais e reversíveis pertencem a issues, contratos ou código;
- contradição entre esta ADR e outro artifact interrompe a execução até reconciliação pelo Arquiteto.

## Alternativas consideradas

- manter a decisão agregada em uma ADR ampla: rejeitado por ocultar drivers, trade-offs e owners independentes;
- delegar a escolha à implementação: rejeitado por permitir divergência entre agentes e superfícies;
- transformar parâmetros reversíveis em ADR: rejeitado; profiles e benchmarks continuam sendo os owners desses valores.

## Racional da seleção

A opção selecionada reduz ambiguidade, limita o espaço de inferência dos agentes, permite auditoria independente e mantém um único owner normativo para uma decisão material.

## Consequências e trade-offs

- aumenta o número de ADRs e a disciplina de rastreabilidade;
- reduz o tamanho de cada contexto decisório e o risco de implementações redundantes;
- mudanças futuras precisam identificar exatamente qual boundary será substituído;
- integração entre decisões ocorre somente pelas dependências declaradas abaixo.

## Dependências arquiteturais

`ADR-041`, `ADR-044`, `ADR-045`

## Gate de mudança

Mudança que altere a autoridade, tecnologia estrutural, formato público, trust boundary, modelo de consistência ou direção de dependências deste boundary exige ADR substituta. Ajustes compatíveis e reversíveis seguem profiles, contratos e issues.

## Verificação de conformidade

- validators devem confirmar referência a IDs existentes e sequência contínua;
- histórias e TaskEnvelopes devem listar esta ADR quando modificarem o boundary;
- contratos, migrations, testes e evidence aplicáveis devem ser versionados no mesmo commit candidato;
- nenhuma decisão aberta pode ser completada por inferência do implementador.

## Rastreabilidade SAR

- **Requisitos owned:** `REQ-AIE-007`, `REQ-BEX-003`, `REQ-EPIC-035`, `REQ-FS1-007`, `REQ-QUAL-001`, `REQ-QUAL-002`, `REQ-QUAL-003`, `REQ-QUAL-004`, `REQ-QUAL-005`, `REQ-SGVCAL-001`, `REQ-SGVCAL-002`, `REQ-SGVCAL-003`, `REQ-SGVCAL-004`, `REQ-SGVCAL-006`, `REQ-SGVCAL-008`, `REQ-SGVCAL-009`, `REQ-SGVCAL-010`
- **Épicos relacionados:** `EPIC-004`, `EPIC-005`, `EPIC-014`, `EPIC-018`, `EPIC-019`, `EPIC-020`, `EPIC-021`, `EPIC-022`, `EPIC-023`, `EPIC-024`, `EPIC-025`, `EPIC-026`, `EPIC-028`, `EPIC-031`, `EPIC-034`, `EPIC-035`, `EPIC-037`, `EPIC-038`, `EPIC-039`, `EPIC-041`, `EPIC-050`, `EPIC-065`, `EPIC-066`, `EPIC-067`, `EPIC-068`, `EPIC-069`
- **Matriz canônica:** `docs/07-assurance/ADR_APPLICABILITY_MATRIX.csv`
- **Grafo de decisões:** `docs/02-architecture/ADR_DEPENDENCY_GRAPH.json`
- **Revisão:** `docs/07-assurance/PHASE-D-ADR-REVIEW-REPORT.md`
