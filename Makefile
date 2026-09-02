.PHONY: verify python-quality frontend-quality architecture requirements ddd adrs specifications review-sprints

PYTHON ?= python
PNPM ?= pnpm
RUFF_PATHS := tools/governance/migrations-ci-secret-dependency-scan-e-telemetria-mini/sgvcal-srg-srp-parte-4/decision_controls.py tests/fnd/migrations-ci-secret-dependency-scan-e-telemetria-mini/test_sgvcal_srg_srp_part_4.py
MYPY_PATHS := tools/governance/migrations-ci-secret-dependency-scan-e-telemetria-mini/sgvcal-srg-srp-parte-4/decision_controls.py

verify: python-quality frontend-quality
	$(PYTHON) -X utf8 tools/validate_repository.py
	$(PYTHON) -X utf8 tools/run_architecture_review.py
	$(PYTHON) -X utf8 tools/run_requirements_review.py
	$(PYTHON) -X utf8 tools/run_domain_driven_design_review.py
	$(PYTHON) -X utf8 tools/run_adr_review.py
	$(PYTHON) -X utf8 tools/run_specification_review.py
	$(PYTHON) -X utf8 tools/run_sprint_review.py
	$(PYTHON) -X utf8 tools/check_python_architecture.py
	$(PYTHON) -X utf8 tools/governance/monorepo-greenfield-com-cli-api-web-minimos-e-checks-r/foundation_validation.py --foundation docs/03-engineering/contexts/engineering_governance/monorepo-greenfield-com-cli-api-web-minimos-e-checks-r/foundation-plan.json --contract contracts/contexts/engineering_governance/fnd/monorepo-greenfield-com-cli-api-web-minimos-e-checks-r/examples/monorepo-foundation.json
	$(PYTHON) -X utf8 -m pytest -q -p no:cacheprovider tests/fnd/monorepo-greenfield-com-cli-api-web-minimos-e-checks-r/test_foundation.py

python-quality:
	$(PYTHON) -m ruff check $(RUFF_PATHS)
	$(PYTHON) -m mypy $(MYPY_PATHS)

frontend-quality:
	$(PNPM) run frontend:verify

architecture:
	python tools/run_architecture_review.py
	python tools/check_python_architecture.py

requirements:
	python tools/run_requirements_review.py

ddd:
	python tools/run_domain_driven_design_review.py

adrs:
	python tools/run_adr_review.py


specifications:
	python tools/run_specification_review.py

review-sprints:
	python tools/run_sprint_review.py
