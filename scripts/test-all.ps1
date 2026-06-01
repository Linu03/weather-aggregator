# Run all project tests from repo root. Requires Docker for integration, service, and behave.
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

Write-Host "==> Backend (pytest)" -ForegroundColor Cyan
python -m pytest
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "==> Backend (behave)" -ForegroundColor Cyan
behave
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "==> Frontend (vitest + build)" -ForegroundColor Cyan
Push-Location frontend
npm ci
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
npm run test
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
npm run build
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Pop-Location

Write-Host "All tests passed." -ForegroundColor Green
