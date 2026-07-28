# Baseline tecnológica fechada

- **Versão SAR:** `3.0`
- **Estado arquitetural:** `APPROVED_FOR_IMPLEMENTATION`
- **Autorização de execução:** `BLOCKED_EXTERNAL` até emissão do `ImplementationAuthorizationRecord`.
- **Princípio:** nenhuma dependência usa tag flutuante; major/minor é decisão normativa e o patch exato é congelado em lockfile ou digest OCI.

| Área | Tecnologia | Família normativa | Decisão | Pin exato |
|---|---|---|---|---|
| language-backend | CPython | `3.12.13` | runtime primário e único requisito da implementação inicial | `.python-version`, CI e digest OCI |
| language-backend-compat-313 | CPython | `3.13.x` | lane futura não bloqueante; ativação após gate da stack nativa | matriz CI e lock experimental separados |
| language-backend-compat-314 | CPython | `3.14.x` | alvo de integração posterior; não integra o CI inicial | matriz experimental após estabilização da lane 3.13 |
| dependency-management | uv | `stable pinned` | single Python workspace and lock | tool bootstrap digest |
| http-api | FastAPI | `0.140.x` | REST/OpenAPI adapter | uv.lock |
| validation | Pydantic | `2.13.x` | transport/settings/schema validation | uv.lock |
| persistence | SQLAlchemy | `2.0.x` | explicit repositories and UoW | uv.lock |
| migrations | Alembic | `1.x` | expand-migrate-contract migrations | uv.lock |
| database | PostgreSQL | `18.x` | system of record | OCI image digest |
| spatial-database | PostGIS | `3.6.x` | spatial extension | OCI image digest |
| broker | RabbitMQ | `4.3.x` | durable transport only | OCI image digest |
| workers | Celery | `5.6.x` | worker adapter over TaskEnvelope | uv.lock |
| frontend-runtime | Node.js | `24.x LTS` | frontend toolchain runtime | .tool-versions and CI image digest |
| frontend-package-manager | pnpm | `10.x` | single JS workspace and frozen lock | packageManager field and corepack digest |
| frontend-ui | React | `19.2.x` | SPA component model; no React Server Components; react/react-dom same exact patch | pnpm-lock.yaml |
| frontend-build | Vite | `8.1.x` | SPA build/dev server | pnpm-lock.yaml |
| frontend-types | TypeScript | `6.0.x` | primary strict type checker and generated OpenAPI client; conservative bridge release | pnpm-lock.yaml |
| frontend-types-compat | TypeScript | `7.0.x` | mandatory compatibility lane; promotion only after Vite, Vitest, Playwright, generated-client and editor-tooling gate | separate CI matrix and pnpm lock experiment |
| cartography | OpenLayers | `10.9.x` | browser map engine | pnpm-lock.yaml |
| native-raster | GDAL | `3.13.x` | raster I/O and COG creation | native OCI stack digest |
| crs | PROJ | `9.8.x` | CRS transforms and grids | native OCI stack digest |
| geometry | GEOS | `3.14.x stable` | geometry predicates/operations | native OCI stack digest |
| computer-vision | OpenCV | `4.x stable` | RootSIFT/FLANN/USAC_MAGSAC adapters | native OCI stack digest |
| raster-python | Rasterio | `compatible with pinned GDAL` | primary typed raster adapter | uv.lock + ABI gate |
| geometry-python | Shapely | `2.x` | domain geometry adapter | uv.lock + GEOS ABI gate |
| crs-python | pyproj | `3.x` | typed CRS adapter | uv.lock + PROJ ABI gate |
| deployment | OCI images + Compose | `Compose Specification` | official single-instance deployment | signed image digests |
| observability | OpenTelemetry | `stable APIs/SDKs` | vendor-neutral telemetry | lockfiles and collector image digest |
| api-contract | OpenAPI | `3.1.0` | normative HTTP contract | repository file digest |
| schema-contract | JSON Schema | `2020-12` | normative data/event/artifact schemas | repository file digest |
| geometric-model | projective homography + USAC_MAGSAC | `profile-versioned` | canonical final model/robust estimator | ClassicalMatchingProfile digest |
| quality-authority | Strong Geometric Verifier | `SGVProfile-versioned` | fail-closed acceptance authority | SGVProfile digest |

## Decisões conservadoras explícitas

- **Python:** 3.12 é o runtime primário e o único exigido na implementação inicial. A baseline usa `requires-python = ">=3.12,<3.13"`, Ruff `py312` e mypy 3.12. Python 3.13 será avaliado em lane futura não bloqueante após o gate GDAL/Rasterio/pyproj/Shapely/OpenCV; Python 3.14 somente será integrado depois de a lane 3.13 estar estável. A linha 3.12 recebe correções de segurança até outubro de 2028, portanto a atualização antes desse limite é um gate operacional obrigatório.
- **TypeScript:** 6.0 é o compilador primário; 7.0 é lane obrigatória, mas não primária nesta baseline por ter introduzido uma reimplementação recente do compilador. A promoção exige compatibilidade de Vite, Vitest, Playwright, cliente OpenAPI e tooling de editor.
- **React:** a aplicação é SPA cliente e não usa React Server Components. `react` e `react-dom` devem compartilhar o mesmo patch; qualquer pacote RSC é proibido no baseline. Caso esse boundary mude, o mínimo seguro conhecido da família 19.2 é 19.2.4 e uma nova revisão de segurança é obrigatória.
- **PROJ:** a imagem nativa fixa também o banco EPSG/proj-data; upgrades exigem regressão de CRS porque a linha 9.8 teve alteração e reversão de conteúdo EPSG.

## Parâmetros que não são decisões em aberto

Os itens abaixo são deliberadamente promovidos por benchmark porque escolher números sem corpus seria uma suposição inválida:

- Argon2id cost, throttling and session timeouts (BP-003)
- matching thresholds, tiles, keypoint quotas and FLANN parameters (BP-001)
- SGV thresholds and false-accept budget (BP-002)
- worker prefetch, concurrency, lease, recycle and queue capacity (BP-004)
- CPU/RAM/GPU/disk quotas by supported hardware class

Esses parâmetros possuem owner, Benchmark Profile, corpus, teste e gate. Não exigem nova escolha tecnológica, apenas evidência mensurável.

## Verificação oficial

A evidência de versão e os riscos de adoção estão registrados em `docs/03-engineering/TECHNOLOGY_VERIFICATION.md`. A verificação de 27 de julho de 2026 confirmou as famílias normativas. O patch exato será revalidado no momento de criação dos lockfiles e digests, evitando congelar antecipadamente um patch vulnerável ou superseded.
## Parecer econômico e operacional — Fase G

A baseline tecnológica foi aprovada para implementação em estágios. Não existe vendor comercial obrigatório. PostgreSQL/PostGIS, POSIX filesystem e stack geoespacial nativa são lock-ins tecnológicos intencionais; GPU permanece opcional; custo e capacidade dependem dos gates `G-CTO-02` e `G-CTO-03`.
