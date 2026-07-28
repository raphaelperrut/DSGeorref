# REQ-TOOL-001 — Python 3.12 como runtime primário, com atualização controlada para 3.13 e integração futura com 3.14

- **Tipo:** `NAO_FUNCIONAL`
- **Categoria:** `TOOL`
- **Prioridade:** `P1`
- **Owner normativo:** `ADR-035`
- **Estado:** `ACCEPTED`
- **Gate:** `SPRINT-001 / PythonRuntimeGate`

## Requisito

O backend e os serviços Python devem usar **CPython 3.12.13 como runtime primário inicial, dentro da linha 3.12**. O código deve permanecer compatível com a linguagem 3.12 e não pode depender de sintaxe, biblioteca padrão ou comportamento exclusivo de Python 3.13 ou 3.14.

A adoção de Python 3.13 será uma atualização posterior, deliberada e reversível. Python 3.14 somente poderá entrar como lane de integração depois de a lane 3.13 estar estável. Nenhuma dessas versões é requisito para iniciar o produto.

## Controles obrigatórios

- `.python-version` fixa `3.12.13`; o mesmo patch deve ser usado no ambiente de desenvolvimento, CI e imagem OCI;
- `pyproject.toml` declara `requires-python = ">=3.12,<3.13"` na baseline inicial;
- Ruff usa `target-version = "py312"` e mypy usa `python_version = "3.12"`;
- a stack nativa GDAL/Rasterio/PROJ/pyproj/GEOS/Shapely/OpenCV deve passar por teste ABI na mesma imagem;
- nenhuma dependência pode ser atualizada por tag flutuante;
- a mudança para 3.13 ou 3.14 exige compatibility matrix, lock diff, testes, benchmark, SBOM, imagem assinada e rollback documentado.

## Rastreabilidade

- **Épicos:** `EPIC-001`, `EPIC-002`
- **Histórias:** `STORY-0699`
- **Evidência ou teste canônico:** `test_python_312_primary_and_upgrade_gates`
- **Profile:** `docs/03-engineering/application-profiles/AP-001-sprint-001-engineering-toolchain.md`
- **Política:** `docs/03-engineering/PYTHON_312_RUNTIME_POLICY.md`
- **Matriz:** `docs/06-delivery/TRACEABILITY_MATRIX.csv`


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-001` — Governança de Engenharia e Entrega.
- **Contexts consumidores:** `BC-001`.
- **Regra:** o requisito é implementado no modelo do owner; consumidores usam contrato publicado e não reinterpretam a invariante.
- **Resultado:** `PASS`.

## Critério de conformidade

O requisito é atendido quando o runtime 3.12, os linters, o type checker, a imagem nativa e os testes passam no commit candidato; qualquer lane 3.13/3.14 permanece isolada e não altera o runtime primário sem aprovação do gate de atualização.
