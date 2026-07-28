# Verificação oficial da baseline tecnológica

- **Data de verificação:** 27/07/2026
- **Regra:** usar somente fontes oficiais dos projetos; o patch exato será revalidado quando lockfiles e imagens forem criados.
- **Resultado:** Python 3.12 é compatível com a stack Python principal selecionada. A série está em fase de correções de segurança, o que torna obrigatório o plano de atualização antes de outubro de 2028.

| Tecnologia | Evidência oficial | Decisão SAR |
|---|---|---|
| CPython | Python Developer's Guide registra 3.12 em `security` até 2028-10 | 3.12 primário; 3.13/3.14 somente por gate posterior |
| FastAPI | PyPI declara Python `>=3.10` e classifica 3.12 | compatível com 3.12 |
| Pydantic | PyPI declara Python `>=3.9` e classifica 3.12 | compatível com 3.12 |
| SQLAlchemy | PyPI classifica Python 3.12 | compatível com 3.12 |
| Celery | documentação/PyPI da linha 5.x inclui Python 3.12 | compatível com 3.12 |
| Rasterio | documentação oficial da linha 1.5 exige Python `>=3.12` | 3.12 é o piso compatível da stack raster atual |
| Shapely | PyPI declara Python `>=3.10` e classifica 3.12 | compatível com 3.12 |
| pyproj | PyPI declara Python `>=3.11` e classifica 3.12 | compatível com 3.12 |

## Fontes oficiais

- https://devguide.python.org/versions/
- https://www.python.org/downloads/release/python-31212/
- https://pypi.org/project/fastapi/
- https://pypi.org/project/pydantic/
- https://pypi.org/project/SQLAlchemy/
- https://pypi.org/project/celery/
- https://rasterio.readthedocs.io/en/latest/
- https://pypi.org/project/shapely/
- https://pypi.org/project/pyproj/

## Risco e ação

Python 3.12 não recebe correções regulares de bugs. O produto pode iniciar nessa série por compatibilidade e estabilidade do ecossistema, mas o release train deve manter o `PythonRuntimeGate` e concluir a atualização antes do fim do suporte de segurança.
