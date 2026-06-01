test:
	pytest

coverage:
	pytest --cov=backend

coverage-html:
	pytest --cov=backend --cov-report=html