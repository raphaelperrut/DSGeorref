# AP-006 — Native geospatial runtime profile

- **Status:** `Accepted`
- **Owner ADRs:** ADR-041 e ADR-044

## Profile inicial

- COG escrito pelo driver GDAL e validado por caminho independente;
- GDAL, PROJ, GEOS, OpenCV, grids e bindings promovidos como unidade OCI/ABI com digests e smoke corpus;
- drivers e VSI allowlisted; network VSI desabilitado por padrão;
- dataset handles não são compartilhados entre work units;
- limites de cache, threads e subprocessos são configurados e testados na issue STORY-0585 / ISSUE-0695.
