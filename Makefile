.PHONY: verify python-quality frontend-quality technical-tests integration-tests

PYTHON ?= python
PNPM ?= pnpm
PYTEST := $(PYTHON) -X utf8 -m pytest -q -p no:cacheprovider --import-mode=importlib
FOUNDATION_VALIDATORS := tools/quality/contexts/engineering_governance
LICENSING := tools/governance/license-citation-cff-contribuicao-dco-cla-e-gate-de-pu/foundation_validation.py
RUFF_PATHS := tools/governance/migrations-ci-secret-dependency-scan-e-telemetria-mini/sgvcal-srg-srp-parte-4/decision_controls.py tests/fnd/migrations-ci-secret-dependency-scan-e-telemetria-mini/test_sgvcal_srg_srp_part_4.py
MYPY_PATHS := tools/governance/migrations-ci-secret-dependency-scan-e-telemetria-mini/sgvcal-srg-srp-parte-4/decision_controls.py

verify: python-quality frontend-quality technical-tests integration-tests

python-quality:
	$(PYTHON) -m ruff check $(RUFF_PATHS)
	$(PYTHON) -m mypy $(MYPY_PATHS)
	$(PYTHON) -X utf8 tools/check_python_architecture.py

technical-tests:
	$(PYTHON) -X utf8 $(FOUNDATION_VALIDATORS)/migrations-ci-secret-dependency-scan-e-telemetria-mini/validator.py --technical
	$(PYTHON) -X utf8 $(FOUNDATION_VALIDATORS)/openapi-cliente-typescript-e-contratos-cli-jobs-evento/validator.py --technical
	$(PYTHON) -X utf8 $(LICENSING) --technical
	$(PYTEST) tests/fnd/license-citation-cff-contribuicao-dco-cla-e-gate-de-pu/test_foundation.py -k 'not test_epic_007_fundacao'
	$(PYTHON) -X utf8 -m pytest -q -p no:cacheprovider tests/integration/walking_skeleton/test_runtime.py::test_process_cleanup_escalates_after_graceful_shutdown_timeout
	$(PYTEST) tests/fnd/monorepo-greenfield-com-cli-api-web-minimos-e-checks-r/test_foundation_contract.py::test_cli_api_semantic_contract \
		tests/fnd/monorepo-greenfield-com-cli-api-web-minimos-e-checks-r/test_foundation_contract.py::test_foundation_contract_rejects_silent_fallback_and_duplicate_authority \
		tests/fnd/walking-skeleton-frontendapipostgresqlrabbitmq-celeryw/test_contract.py::test_executable_foundation_gate_clean_room_end_to_end \
		tests/fnd/walking-skeleton-frontendapipostgresqlrabbitmq-celeryw/test_contract.py::test_walking_skeleton_fail_closed_paths \
		tests/fnd/openapi-cliente-typescript-e-contratos-cli-jobs-evento/test_runtime_schema_contract.py \
		tests/fnd/migrations-ci-secret-dependency-scan-e-telemetria-mini/test_sgvcal_conformance.py \
		tests/fnd/catalogo-de-conhecimento-tecnico-e-decomposicao-das-ca/test_foundation.py::test_corpus_license_hash_split_and_access_integrity \
		tests/fnd/catalogo-de-conhecimento-tecnico-e-decomposicao-das-ca/test_foundation.py::test_reference_capability_inventory_no_code_import \
		tests/fnd/catalogo-de-conhecimento-tecnico-e-decomposicao-das-ca/test_foundation.py::test_foundation_rejects_contract_drift_and_corpus_tampering \
		tests/fnd/catalogo-de-conhecimento-tecnico-e-decomposicao-das-ca/test_foundation.py::test_foundation_rejects_missing_catalog_without_fallback \
		-k 'not test_contract_package_is_registered_and_envelope_is_contained'
	$(PYTEST) tests/infra/native_stack/test_native_stack.py

integration-tests:
	$(PYTHON) -X utf8 -m pytest -q -p no:cacheprovider tests/integration/walking_skeleton/test_runtime.py::test_walking_skeleton_end_to_end_and_vertical_slice_definition_of_done

frontend-quality:
	$(PNPM) --dir src/frontend openapi:check
	$(PNPM) --dir src/frontend openapi:diff $(OPENAPI_BASE_SHA)
	$(PNPM) run frontend:typecheck
	$(PNPM) run frontend:test:unit
	$(PNPM) run frontend:test:browser
	$(PNPM) run frontend:build
	$(PNPM) --dir src/frontend test:smoke
