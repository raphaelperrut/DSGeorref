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

Use CPython 3.12.13, Node 24.20.0 e pnpm 10.26.1. Instale `requirements-validation.txt`, rode `pnpm install --frozen-lockfile` e instale o Chromium da versão de Playwright do workspace. Execute a partir da raiz:

```bash
make verify OPENAPI_BASE_SHA=origin/main
```

Para o walking skeleton, configure `FOUNDATION_INTEGRATION=1`, `FOUNDATION_DATABASE_URL` e `FOUNDATION_BROKER_URL` com serviços descartáveis. Use os pins e as variáveis de [.github/workflows/ci.yml](../../.github/workflows/ci.yml) como referência. O mesmo workflow define a execução de identidade e migrations em um banco separado e o uso do SHA exato da base no PR.

## Regras

- CI é a execução canônica;
- instalações usam locks frozen;
- nenhuma tarefa padrão baixa modelos, tiles ou corpora grandes implicitamente;
- suítes GPU e corpus real são opt-in e governadas;
- diferenças host/container devem ser detectadas por testes de equivalência;
- promoção de Python ou Node atualiza locks, digests e evidence sets.
