# Weather Aggregator Backend

Backend pentru agregarea datelor meteorologice folosind **Hexagonal Architecture (Ports & Adapters)**.

## Structura Proiectului

```
weather-aggregator/
├── domain/              # Business Logic Layer (核心層)
│   ├── model.py        # Entități de business pure
│   ├── ports.py        # Interfețe abstracte (contracte)
│   └── service.py      # Logica de business
├── adapters/           # Infrastructure Layer
│   ├── open_meteo.py   # Adapter pentru Open-Meteo API
│   └── postgres_repo.py # Adapter pentru PostgreSQL
├── api/                # Application Layer
│   └── router.py       # FastAPI endpoints
└── requirements.txt    # Dependențe Python
```

## Principii Hexagonal Architecture

### 1. **Domain Layer** (Centru)
- **Nu depinde de nimic extern**
- Conține logica de business pură
- Definește interfețe (ports) pentru comunicare cu exterior

### 2. **Adapters Layer** (Exterior)
- Implementează ports-urile definite în domain
- Gestionează detalii tehnice (HTTP, DB, etc.)
- Poate fi înlocuit fără a afecta domain-ul

### 3. **API Layer** (Entry Point)
- Primește request-uri HTTP
- Orchestrează domain service și adapters
- Transformă date între format HTTP și domain models

## Reguli Stricte

✅ **Domain layer:**
- NU importă FastAPI, httpx, psycopg2
- NU conține detalii de infrastructură
- Doar Python standard și abstractizări

✅ **Adapters:**
- Implementează interfețele din `domain/ports.py`
- Conțin toată logica de integrare externă

✅ **API:**
- Injectează dependențele
- Gestionează serializare/deserializare HTTP

## Instalare

```bash
pip install -r requirements.txt
```

## Următorii Pași

1. Implementare domain models
2. Definire ports (interfețe)
3. Implementare domain service
4. Implementare adapters
5. Implementare API endpoints
6. Testing
