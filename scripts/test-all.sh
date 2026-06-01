#!/usr/bin/env bash
# Run all project tests from repo root. Requires Docker for integration, service, and behave.
set -euo pipefail
cd "$(dirname "$0")/.."

echo "==> Backend (pytest)"
python -m pytest

echo "==> Backend (behave)"
behave

echo "==> Frontend (vitest + build)"
(
  cd frontend
  npm ci
  npm run test
  npm run build
)

echo "All tests passed."
