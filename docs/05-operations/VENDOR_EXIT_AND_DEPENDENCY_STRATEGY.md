# Dependências e estratégia de saída — baseline 3.0

## Parecer

Não existe dependência obrigatória de cloud ou fornecedor comercial. Existe lock-in tecnológico intencional em PostgreSQL/PostGIS, filesystem POSIX e stack GDAL/PROJ/GEOS/OpenCV. O custo de saída é aceito porque essas tecnologias sustentam o core geoespacial e possuem formatos de exportação abertos.

## Controles

- todas as dependências têm pin, owner e fallback no registro externo;
- contracts e adapters protegem FastAPI, Celery, OpenLayers, OIDC, providers e OpenTelemetry;
- COG, GeoTIFF, GeoPackage, GeoJSON, OpenAPI e JSON Schema preservam portabilidade;
- substituição de PostGIS, POSIX artifacts ou stack nativa é mudança material e exige ADR;
- GPU, OIDC, providers e backend de observabilidade permanecem opcionais.

O inventário canônico está em `contracts/operations/external-dependency-register.csv` e `contracts/operations/vendor-exit-matrix.csv`.
