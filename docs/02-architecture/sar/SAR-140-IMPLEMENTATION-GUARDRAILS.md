# SAR-140 — Guardrails de implementação

## Runtime

Python 3.12 é o runtime primário. Python 3.13 e 3.14 não são dependências da implementação inicial e entram somente pelos gates do AP-001.

## Anti-alucinação

Um agente somente implementa elementos existentes nas fontes normativas. Ausência de requisito, schema, endpoint, estado, tabela, evento ou owner é condição de parada. O agente não preenche lacuna arquitetural por inferência silenciosa.

## Modularidade

- código organizado por bounded context e responsabilidade, nunca por issue ou épico;
- domínio e application services são únicos e reutilizados por API, CLI e worker;
- adapters não reimplementam regras;
- imports circulares são bloqueados;
- módulos genéricos sem owner são proibidos;
- limites de tamanho e complexidade são machine-readable em `contracts/architecture/python-module-boundaries.yaml`.

## Gates

- `make verify`: consistência SAR, schemas, DAG e links;
- `make architecture`: fitness functions de Python;
- contract freeze antes de paralelização;
- QA e Reviewer independentes no mesmo commit candidato;
- exceção exige Design Review e não pode ser autoaprovada pelo implementador.


## Decisões de fechamento da Fase A

- ADR-007: packages e write scopes estáveis;
- ADR-008: no máximo 10 requisitos por história;
- ADR-010: contratos específicos congelados;
- ADR-009: CPython 3.12.13 e lock nativo reproduzível.
