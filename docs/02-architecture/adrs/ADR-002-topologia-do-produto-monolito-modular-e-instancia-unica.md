# ADR-002 — Topologia do produto: monólito modular e instância única

- **Status:** `Accepted`
- **Baseline:** `SAR v2.8 — Fase E`
- **Aprovador:** `Project Owner`
- **Owner normativo:** `ADR-002`
- **Boundary independente:** `SIM`
- **Decisões em aberto:** `Nenhuma`
- **Bounded Contexts:** `BC-001` — Governança de Engenharia e Entrega

## Contexto

Esta ADR isola uma decisão arquitetural de alto impacto e alto custo de reversão. Ela substitui agrupamentos amplos da baseline anterior e possui responsabilidade normativa exclusiva sobre o boundary descrito no título.

## Decisão

- O DSGeorref é greenfield, single-instance e unificado, implementado como monólito modular.
- Processos separados existem somente para HTTP, frontend, CLI, workers e tarefas operacionais que exigem isolamento.
- Microservices, multitenancy, billing e planos comerciais não pertencem à baseline.
- O domínio e os application services são compartilhados por todas as superfícies.

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

`ADR-001`

## Gate de mudança

Mudança que altere a autoridade, tecnologia estrutural, formato público, trust boundary, modelo de consistência ou direção de dependências deste boundary exige ADR substituta. Ajustes compatíveis e reversíveis seguem profiles, contratos e issues.

## Verificação de conformidade

- validators devem confirmar referência a IDs existentes e sequência contínua;
- histórias e TaskEnvelopes devem listar esta ADR quando modificarem o boundary;
- contratos, migrations, testes e evidence aplicáveis devem ser versionados no mesmo commit candidato;
- nenhuma decisão aberta pode ser completada por inferência do implementador.

## Rastreabilidade SAR

- **Requisitos owned:** `REQ-EPIC-001`, `REQ-EPIC-037`, `REQ-EPIC-038`, `REQ-EPIC-041`, `REQ-EPIC-042`, `REQ-EPIC-062`, `REQ-EPIC-070`, `REQ-RUNTIME-001`, `REQ-RUNTIME-002`, `REQ-RUNTIME-007`, `REQ-SGVCAL-007`
- **Épicos relacionados:** `EPIC-002`, `EPIC-004`, `EPIC-005`, `EPIC-007`, `EPIC-011`, `EPIC-014`, `EPIC-018`, `EPIC-022`, `EPIC-028`, `EPIC-030`, `EPIC-034`, `EPIC-036`, `EPIC-037`, `EPIC-041`, `EPIC-042`, `EPIC-049`, `EPIC-062`, `EPIC-080`, `EPIC-086`, `EPIC-092`
- **Matriz canônica:** `docs/07-assurance/ADR_APPLICABILITY_MATRIX.csv`
- **Grafo de decisões:** `docs/02-architecture/ADR_DEPENDENCY_GRAPH.json`
- **Revisão:** `docs/07-assurance/PHASE-D-ADR-REVIEW-REPORT.md`
