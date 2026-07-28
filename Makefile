.PHONY: verify architecture requirements ddd adrs specifications review-sprints

verify:
	python tools/validate_repository.py
	python tools/run_architecture_review.py
	python tools/run_requirements_review.py
	python tools/run_domain_driven_design_review.py
	python tools/run_adr_review.py
	python tools/run_specification_review.py
	python tools/run_sprint_review.py
	python tools/check_python_architecture.py

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
