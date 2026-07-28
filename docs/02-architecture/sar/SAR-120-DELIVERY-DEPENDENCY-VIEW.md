# SAR-120 — Dependências e entrega

O grafo de histórias é o mecanismo normativo de paralelização. Aresta `A blocks B` significa que B somente inicia após o artifact/contrato de A estar integrado.

- Grafo: `docs/06-delivery/STORY_DEPENDENCY_GRAPH.json`.
- Índice: `docs/06-delivery/STORY_INDEX.csv`.
- Ondas topológicas: `docs/06-delivery/STORY_DEPENDENCY_GRAPH.md`.
- Audit: `docs/07-assurance/DEPENDENCY_AUDIT.md`.

Contratos e migrations são serializados; implementações especialistas abrem lanes disjuntas somente após contract freeze. QA e Reviewer atuam sobre o mesmo commit candidato e não aprovam o próprio trabalho.
