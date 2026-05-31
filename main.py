from fastapi import FastAPI
from api.router import router
from dotenv import load_dotenv

# Încarcă variabilele de environment din .env
load_dotenv()

# Creează aplicația FastAPI
app = FastAPI(
    title="Weather Aggregator API",
    description="API pentru agregarea datelor meteorologice de la Open-Meteo",
    version="1.0.0"
)

# Include router-ul cu endpoint-urile
app.include_router(router)


@app.get("/", tags=["root"])
def read_root():
    return {
        "message": "Weather Aggregator API is running",
        "version": "1.0.0",
        "endpoints": {
            "POST /weather/fetch": "Preia și salvează date meteo pentru un oraș",
            "GET /weather/history/{city}": "Istoric complet pentru un oraș",
            "GET /weather/latest/{city}": "Ultima citire pentru un oraș"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
