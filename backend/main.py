from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.router import router

BACKEND_DIR = Path(__file__).resolve().parent
REPO_ROOT = BACKEND_DIR.parent

load_dotenv(BACKEND_DIR / ".env")
load_dotenv(REPO_ROOT / ".env")

app = FastAPI(
    title="Weather Aggregator API",
    description="API pentru agregarea datelor meteorologice de la Open-Meteo",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/", tags=["root"])
def read_root():
    return {
        "message": "Weather Aggregator API is running",
        "version": "1.0.0",
        "endpoints": {
            "POST /weather/fetch": "Preia și salvează date meteo pentru un oraș",
            "GET /weather/{city}": "Istoric complet pentru un oraș",
            "GET /weather/{city}/latest": "Ultima citire pentru un oraș",
        },
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
