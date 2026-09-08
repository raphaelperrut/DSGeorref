# Evidence — STORY-0534 / ISSUE-0644

## Candidate scope

- contrato versionado, schema Draft 2020-12 e exemplo executável do walking skeleton;
- design review com boundaries, autoridade, compatibilidade, migration/rollback e falhas;
- ownership dos três artifacts contratuais;
- testes focados dos ACs e paths fail-closed;
- ajuste do `TASK-0534` somente para permitir teste, evidência e registry obrigatórios.

Nenhum arquivo de runtime, OpenAPI compartilhado, schema de domínio, migration ou regra de
produto foi alterado.

## Acceptance evidence

| Critério | Evidência |
|---|---|
| `AC-ISSUE-0644-01` | `walking-skeleton.schema.json`, exemplo e `test_executable_foundation_gate_clean_room_end_to_end` |
| `AC-ISSUE-0644-02` | manifesto mapeia `REQ-EPIC-001` e `REQ-SPRINT-001-004` aos testes canônicos |
| `AC-ISSUE-0644-03` | seis outcomes fail-closed e mutações negativas em `test_walking_skeleton_fail_closed_paths` |
| `AC-ISSUE-0644-04` | schemas/estados versionados, SemVer, authority, migration/rollback e ownership validados por `test_epic_086_contrato` |

## Validation result

- `py -3.12 -X utf8 -m pytest -q -p no:cacheprovider tests/fnd/walking-skeleton-frontendapipostgresqlrabbitmq-celeryw/test_contract.py`
  — PASS, 3 testes.
- `py -3.12 -X utf8 -m pytest -q -p no:cacheprovider tests/fnd/governanca-de-decisoes-arquiteturais-e-manutencao-da-b/test_contract.py::test_sprint_zero_baseline_decision_04`
  — PASS, 1 teste.
- `py -3.12 -m ruff check tests/fnd/walking-skeleton-frontendapipostgresqlrabbitmq-celeryw/test_contract.py`
  — PASS.
- `py -3.12 -X utf8 tools/validate_repository.py` — PASS.
- `py -3.12 -X utf8 tools/check_python_architecture.py` — PASS.
- `make PYTHON="py -3.12" verify` — o gate local obrigatório passou por frontend,
  browser e validadores de arquitetura, requisitos, DDD, ADRs e specifications; sua
  etapa de integração preexistente exige PostgreSQL/RabbitMQ e
  `FOUNDATION_INTEGRATION=1`, indisponíveis neste host sem Docker. O workflow hospedado
  `.github/workflows/ci.yml` fornece os serviços pinados e é o gate equivalente do SHA
  publicado no PR.

## Handoff

- Runtime é deliberadamente `DOWNSTREAM_STORIES_ONLY`; esta Story congela o contrato e
  não declara que o serviço está materializado.
- Não há migration nesta mudança; qualquer persistência downstream exige migration e
  rollback conforme o contrato.
- Risco arquitetural residual: nenhum identificado dentro do diff.
- Aprovação independente permanece pendente e deve referenciar o mesmo SHA do PR; este
  documento não constitui autoaprovação.
