# Create Test Makefile
# What This Step Does: Simplifies testing commands.

test:
	pytest

coverage:
	pytest --cov=backend

coverage-html:
	pytest --cov=backend --cov-report=html