# Weather Aggregator

Monorepo: API FastAPI (hexagonal architecture), React UI, PostgreSQL.

## Project structure

```
weather-aggregator/
├── backend/           # Python API
│   ├── main.py
│   ├── api/
│   ├── domain/
│   ├── adapters/
│   └── requirements.txt
├── frontend/          # React (Vite)
├── tests/             # pytest, pact, behave
├── docker-compose.yml
├── init.sql
├── pytest.ini
└── behave.ini
```

## Prerequisites

- Python 3.11+
- Node.js 18+
- Docker (integration, service, and behave tests)

## Backend

```bash
docker compose up -d
cd backend
pip install -r requirements.txt
# Copy backend/.env.example to backend/.env (or keep .env at repo root)
uvicorn main:app --reload --port 8000
```

API docs: http://localhost:8000/docs

## Frontend

```bash
cd frontend
npm install
npm run dev
```

UI: http://localhost:5173 (proxies `/weather` to the API)

```bash
npm run test
```

## Tests (from repo root)

```bash
pip install -r backend/requirements.txt
pytest tests/unit/ -v
pytest tests/pact/consumer/ -v
pytest tests/pact/provider/ -v
pytest tests/integration/ -v
pytest tests/service/ -v
behave
```

## Hexagonal architecture

- **domain/** — business logic, ports, no FastAPI/DB/HTTP imports
- **adapters/** — Open-Meteo, PostgreSQL
- **api/** — FastAPI routes and HTTP mapping
