# Desenvolvimento local

## Baseline aprovada para a SPRINT-001

- Python 3.12 como runtime primário e único requisito da baseline inicial;
- Python 3.13 como lane futura não bloqueante após o gate da stack nativa;
- Python 3.14 como alvo de integração posterior, somente depois da estabilização em 3.13;
- `uv`, workspace `pyproject.toml` e `uv.lock`;
- FastAPI/Pydantic;
- SQLAlchemy 2 e Alembic, com SQL/PostGIS explícito quando necessário;
- Ruff e mypy progressivamente estrito;
- pytest em camadas com PostgreSQL/PostGIS e RabbitMQ reais;
- Node 24 LTS e pnpm workspace;
- TypeScript 6.0 strict como compilador primário; TypeScript 7.0 em lane obrigatória de compatibilidade; Vitest, Testing Library e Playwright;
- Make como façade estável da toolchain.

Nesta fundação documental, os verificadores continuam exigindo apenas Python compatível e `make`:

```bash
make verify
```

A SPRINT-001 criará os lockfiles, manifests, imagens e testes reais. Nenhum runtime ou package citado neste documento está implementado ainda.

## Regras

- CI é a execução canônica;
- instalações usam locks frozen;
- nenhuma tarefa padrão baixa modelos, tiles ou corpora grandes implicitamente;
- suítes GPU e corpus real são opt-in e governadas;
- diferenças host/container devem ser detectadas por testes de equivalência;
- promoção de Python ou Node atualiza locks, digests e evidence sets.
