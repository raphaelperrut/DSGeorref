# AP-001 — Toolchain de engenharia da SPRINT-001

- **Status:** `Accepted`
- **Owner ADR:** `ADR-002` para boundaries de aplicação; `ADR-041` para compatibilidade da stack nativa
- **Runtime primário:** `CPython 3.12.13`

## Baseline vigente

- Python 3.12 como runtime primário e único requisito da implementação inicial;
- `requires-python = ">=3.12,<3.13"`, `.python-version` na série 3.12, Ruff `py312` e mypy 3.12;
- Python 3.13 como lane futura não bloqueante, ativada somente após o gate ABI da stack nativa e suíte integral;
- Python 3.14 como alvo de integração posterior, somente depois de a lane 3.13 estar estável;
- `uv`, `pyproject.toml`, workspace e lock único;
- Ruff e mypy strict; pytest em camadas com PostGIS e RabbitMQ reais quando o tier exigir;
- Node 24 LTS e pnpm 10 workspace com lock congelado;
- TypeScript 6.0 strict primário e TypeScript 7.0 em lane de compatibilidade;
- Make como façade estável para local e CI;
- fitness functions de arquitetura obrigatórias para dependências, ciclos, duplicação e tamanho de módulos.

## Gate PythonRuntimeGate

A promoção de 3.12 para 3.13, ou a ativação de 3.14, exige:

1. lockfile e imagem OCI separados;
2. compatibilidade de FastAPI, Pydantic, SQLAlchemy, Alembic, Celery e OpenTelemetry;
3. gate ABI de GDAL, Rasterio, PROJ, pyproj, GEOS, Shapely e OpenCV;
4. testes unitários, integração, contrato, E2E, científicos e fault injection;
5. comparação de desempenho e memória sem regressão não aceita;
6. SBOM, licenças, assinatura e rollback para 3.12;
7. aprovação do Arquiteto e Reviewer no mesmo commit candidato.

## Regra de evolução

Versões, package managers e ferramentas mudam por PR de toolchain com compatibility matrix, lock diff, SBOM, CI e rollback. Nova ADR somente é necessária se a alteração quebrar a boundary da ADR-002 ou da ADR-041.

A tabela normativa está em `docs/03-engineering/TECHNOLOGY_BASELINE.md`; a política detalhada está em `docs/03-engineering/PYTHON_312_RUNTIME_POLICY.md`.
