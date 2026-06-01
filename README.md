# Weather Aggregator

A monorepo that fetches weather from [Open-Meteo](https://open-meteo.com/), stores readings in PostgreSQL, and exposes them through a FastAPI API and a React UI.

## Overview

### Backend

The API is built with **FastAPI** using **hexagonal architecture (ports and adapters)**:

- **domain/** — business rules, `WeatherReading` model, abstract ports, and `WeatherService` (fetch, store, list by city, latest).
- **adapters/** — `OpenMeteoAdapter` (geocoding + current weather) and `PostgresWeatherRepo` (persistence).
- **api/** — HTTP layer: maps requests/responses and wires dependencies.

Endpoints:

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/weather/fetch?city=` | Fetch from Open-Meteo and save a reading |
| `GET` | `/weather/{city}` | All stored readings for a city (newest first) |
| `GET` | `/weather/{city}/latest` | Latest reading for a city |

PostgreSQL is provided via **Docker Compose** (`docker-compose.yml`, `init.sql`).

### Frontend

A **React** (Vite) single-page app in `frontend/`:

- Enter a city and **fetch** weather (calls the backend).
- View the **latest reading** and a **table of all stored readings** for that city.
- Weather-themed background animations driven by the current condition (Framer Motion + CSS).

The dev server proxies `/weather` to `http://localhost:8000`.

### Testing

A full test pyramid under `tests/` and `frontend/`:

| Layer | Tool | What it covers |
|-------|------|----------------|
| Unit | pytest | `WeatherService` with mocked ports |
| Integration | pytest + Testcontainers | `PostgresWeatherRepo` against real Postgres |
| Service | pytest + Testcontainers | FastAPI routes via `TestClient` (Open-Meteo mocked with respx) |
| Contract | pact-python | Consumer + provider verification for Open-Meteo |
| BDD | Behave | API scenarios in Gherkin |
| Frontend | Vitest + React Testing Library | UI flows and weather-condition helpers |

**Single command (all suites):** `make test`, `.\scripts\test-all.ps1`, or `bash scripts/test-all.sh`  
**All backend Python tests:** `pytest` from the repo root (see `pytest.ini`).

### CI

**GitHub Actions** (`.github/workflows/ci.yml`) runs on push/PR to `master` in three parallel jobs:

1. **Frontend** — `npm ci`, `npm test`, `npm run build`
2. **Backend (unit & pact)** — `pytest` for unit and Pact suites
3. **Backend (integration, service, behave)** — integration, service tests, and `behave` (requires Docker on the runner)

---

## Prerequisites

- Python 3.11+
- Node.js 18+
- Docker (for integration, service, and Behave tests, and for local Postgres)

---

## Running the application

### 1. Start PostgreSQL

From the repository root:

```bash
docker compose up -d
```

### 2. Configure environment

Copy `backend/.env.example` to `backend/.env` (or keep a `.env` file at the repo root — both are loaded).

Default values match `docker-compose.yml`:

```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=weather_db
DB_USER=weather_user
DB_PASSWORD=weather_pass
```

### 3. Start the API

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

- API: http://localhost:8000  
- Swagger UI: http://localhost:8000/docs  

### 4. Start the frontend

In a second terminal:

```bash
cd frontend
npm install
npm run dev
```

- UI: http://localhost:5173  

---

## Running tests

Install backend dependencies once from the repo root:

```bash
pip install -r backend/requirements.txt
```

### All tests (single command)

Requires Docker for backend integration, service, and Behave suites.

```bash
make test
```

Windows (PowerShell):

```powershell
.\scripts\test-all.ps1
```

Linux/macOS (shell):

```bash
bash scripts/test-all.sh
```

Runs: `pytest` → `behave` → `npm ci` + `npm test` + `npm run build` in `frontend/`.

### Each test suite separately

Run from the **repository root** unless noted.

| Suite | Command | Docker required |
|-------|---------|-----------------|
| **All backend (pytest)** | `pytest` | Only for integration & service |
| Unit | `pytest tests/unit/ -v` | No |
| Pact consumer | `pytest tests/pact/consumer/ -v` | No |
| Pact provider | `pytest tests/pact/provider/ -v` | No (run consumer first or use committed pact file) |
| Integration | `pytest tests/integration/ -v` | Yes |
| Service | `pytest tests/service/ -v` | Yes |
| BDD (Behave) | `behave` | Yes |
| Frontend | `cd frontend && npm ci && npm run test` | No |
| Frontend build | `cd frontend && npm run build` | No |

---

## Architectural decisions and tradeoffs

### Hexagonal architecture

The **domain** does not import FastAPI, httpx, or psycopg2. External systems are hidden behind ports (`WeatherApiPort`, `WeatherRepositoryPort`), so adapters can be swapped or tested in isolation. The API layer only orchestrates HTTP and dependency injection.

### Canonical city names

Geocoding returns a canonical name (e.g. `Timișoara`). That name is stored and used for lookups. Queries use `LOWER(city)` for **case-insensitive** matching. **Diacritics are not normalized** — searching `timisoara` may not match `Timișoara` unless Open-Meteo returns a spelling that aligns; this keeps the implementation simple and avoids extra normalization logic.

### Open-Meteo as the only external weather source

The backend never calls third-party APIs from the frontend; the UI talks only to our API. Contract tests (Pact) document the expected Open-Meteo request/response shape.

### Test infrastructure

- **Testcontainers** spins up Postgres for integration and service tests so CI and local runs do not depend on a manually started DB (aside from Docker being available).
- **respx** mocks httpx for service tests (the `responses` library does not patch httpx reliably).
- **Pact** consumer tests must run before provider verification when regenerating contracts; the committed pact file in `tests/pact/pacts/` allows provider tests to run standalone in CI.

### Dependency pinning

`httpx==0.23.1` is pinned because `pact-python==1.7.0` requires that version. Upgrading httpx would require moving to a newer Pact client.

### Monorepo layout

- `backend/` — Python application  
- `frontend/` — React app  
- `tests/` — shared backend test suites (pytest + Behave)  
- Root `pytest.ini` / `behave.ini` — single configuration entry points  

### CI vs local “run all”

Locally, `make test` (or the scripts) runs all suites **sequentially** in one command. **CI** runs the same suites in **parallel jobs** for faster feedback; behavior is equivalent.

---

## Project structure

```
weather-aggregator/
├── backend/
│   ├── main.py
│   ├── api/
│   ├── domain/
│   └── adapters/
├── frontend/
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── service/
│   ├── pact/
│   └── features/
├── scripts/
├── .github/workflows/
├── docker-compose.yml
├── init.sql
├── pytest.ini
└── behave.ini
```
