.PHONY: test test-backend test-frontend install-backend install-frontend

# Run all test suites (pytest + behave + frontend). Requires Docker for integration/service/behave.
test: test-backend test-frontend
	@echo All tests passed.

test-backend:
	python -m pytest
	behave

test-frontend:
	cd frontend && npm ci && npm run test && npm run build

install-backend:
	pip install -r backend/requirements.txt

install-frontend:
	cd frontend && npm ci
