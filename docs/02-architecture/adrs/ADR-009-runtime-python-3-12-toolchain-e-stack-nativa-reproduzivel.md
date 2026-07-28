# ADR-009 — Runtime Python 3.12, toolchain e stack nativa reproduzível

- **Status:** `Accepted`
- **Baseline:** `SAR v2.8 — Fase E`
- **Aprovador:** `Project Owner`
- **Owner normativo:** `ADR-009`
- **Boundary independente:** `SIM`
- **Decisões em aberto:** `Nenhuma`
- **Bounded Contexts:** `BC-001` — Governança de Engenharia e Entrega, `BC-015` — Release, Instalação e Supply Chain

## Contexto

Esta ADR isola uma decisão arquitetural de alto impacto e alto custo de reversão. Ela substitui agrupamentos amplos da baseline anterior e possui responsabilidade normativa exclusiva sobre o boundary descrito no título.

## Decisão

- O runtime primário é CPython 3.12.13 com requires-python >=3.12,<3.13, Ruff py312 e mypy 3.12.
- Locks, versões da stack nativa, SBOM, provenance e digest OCI pertencem ao mesmo release candidate.
- Tags flutuantes são proibidas; Python 3.13 e 3.14 permanecem lanes futuras sujeitas a matriz de compatibilidade e rollback.
- Mudança de runtime ou ABI exige evidência funcional, científica, de memória e de performance.

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

- **Requisitos owned:** `REQ-AI-008`, `REQ-AI-010`, `REQ-AI-013`, `REQ-AI-014`, `REQ-AI-016`, `REQ-AI-017`, `REQ-AIE-003`, `REQ-ARTLAYOUT-001`, `REQ-ARTLAYOUT-008`, `REQ-EPIC-088`, `REQ-NATIVE-009`, `REQ-RMQ-002`, `REQ-SGVCAL-005`, `REQ-TOOL-006`
- **Épicos relacionados:** `EPIC-002`, `EPIC-005`, `EPIC-014`, `EPIC-021`, `EPIC-022`, `EPIC-024`, `EPIC-026`, `EPIC-028`, `EPIC-029`, `EPIC-036`, `EPIC-039`, `EPIC-041`, `EPIC-046`, `EPIC-049`, `EPIC-050`, `EPIC-084`, `EPIC-088`, `EPIC-103`
- **Matriz canônica:** `docs/07-assurance/ADR_APPLICABILITY_MATRIX.csv`
- **Grafo de decisões:** `docs/02-architecture/ADR_DEPENDENCY_GRAPH.json`
- **Revisão:** `docs/07-assurance/PHASE-D-ADR-REVIEW-REPORT.md`
