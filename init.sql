-- Inițializare bază de date pentru Weather Aggregator
-- Acest script rulează automat la primul start al containerului PostgreSQL

-- Creare tabelă weather_reading
CREATE TABLE weather_reading (
    id SERIAL PRIMARY KEY,
    city VARCHAR(100) NOT NULL,
    temperature FLOAT NOT NULL,
    wind_speed FLOAT NOT NULL,
    description VARCHAR(100) NOT NULL,
    fetched_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Index pentru căutări rapide după oraș
CREATE INDEX idx_weather_reading_city ON weather_reading(city);

-- Index pentru sortare după fetched_at
CREATE INDEX idx_weather_reading_fetched_at ON weather_reading(fetched_at DESC);

-- Index compus pentru query-uri frecvente (city + fetched_at)
CREATE INDEX idx_weather_reading_city_fetched ON weather_reading(city, fetched_at DESC);

-- Comentarii pentru documentație
COMMENT ON TABLE weather_reading IS 'Stochează citirile meteorologice agregate de la furnizori';
COMMENT ON COLUMN weather_reading.city IS 'Numele orașului pentru care s-a făcut citirea';
COMMENT ON COLUMN weather_reading.temperature IS 'Temperatura în grade Celsius';
COMMENT ON COLUMN weather_reading.wind_speed IS 'Viteza vântului în km/h';
COMMENT ON COLUMN weather_reading.description IS 'Descrierea condițiilor meteo';
COMMENT ON COLUMN weather_reading.fetched_at IS 'Timestamp când au fost preluate datele de la API';