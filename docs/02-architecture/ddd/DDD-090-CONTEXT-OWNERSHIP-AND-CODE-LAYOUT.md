# Ownership de contexts e layout de código

O monólito é modular por **bounded context primeiro**, depois por camada interna. Uma pasta global `domain/`, `application/` ou `adapters/` é proibida para novo código.

```text
src/backend/dsgeorref/
├── contexts/
│   ├── identity_access/{domain,application,adapters,contracts}/
│   ├── project_workspace/{domain,application,adapters,contracts}/
│   ├── processing_plan/{domain,application,adapters,contracts}/
│   ├── job_orchestration/{domain,application,adapters,contracts}/
│   ├── review_correction/{domain,application,adapters,contracts}/
│   ├── results_reporting/{domain,application,adapters,contracts}/
│   ├── artifact_provenance/{domain,application,adapters,contracts}/
│   ├── operations_audit/{domain,application,adapters,contracts}/
│   └── release_installation/{domain,application,adapters,contracts}/
├── bootstrap/
└── shared/technical/

src/geo/dsgeorref_geo/contexts/
├── reference_discovery/{domain,application,algorithms,adapters,contracts}/
├── georeferencing/{domain,application,algorithms,adapters,contracts}/
├── geometric_quality/{domain,application,algorithms,adapters,contracts}/
└── relative_mosaic/{domain,application,algorithms,adapters,contracts}/

src/ai/dsgeorref_ai/contexts/ai_recovery/{domain,application,runners,adapters,contracts}/
src/frontend/src/contexts/operator_experience/{features,entities,adapters}/
```

## Limites

- import entre contexts somente por package `contracts` ou port de aplicação explicitamente exportado;
- ORM models e repositories ficam internos ao contexto;
- cada migration declara owner context;
- tabelas usam schema PostgreSQL ou prefixo de ownership estável;
- arquivos Python seguem os limites do `PYTHON_CODE_ARCHITECTURE_STANDARD.md`;
- packages orientados por épico, issue, sprint ou agente são proibidos.
