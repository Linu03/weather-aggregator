import { useMemo, useState } from 'react';
import { AnimatePresence, motion } from 'framer-motion';
import { fetchWeather, getWeatherByCity } from './api/weatherApi';
import AnimatedTemperature from './components/AnimatedTemperature';
import WeatherBackground from './components/WeatherBackground';
import WeatherIcon from './components/WeatherIcon';
import {
  getWeatherCondition,
  isWindyOverlay,
} from './utils/weatherCondition';
import { formatFetchedAt } from './utils/formatDate';
import './App.css';

const panelMotion = {
  initial: { opacity: 0, y: 16 },
  animate: { opacity: 1, y: 0 },
  exit: { opacity: 0, y: -8 },
  transition: { duration: 0.45, ease: [0.22, 1, 0.36, 1] },
};

function ReadingDetails({ reading, condition }) {
  return (
    <>
      <WeatherIcon condition={condition} />
      <dl className="reading-details">
        <div>
          <dt>City</dt>
          <dd>{reading.city}</dd>
        </div>
        <div>
          <dt>Temperature</dt>
          <AnimatedTemperature value={reading.temperature} />
        </div>
        <div>
          <dt>Wind speed</dt>
          <dd>{reading.wind_speed} km/h</dd>
        </div>
        <div>
          <dt>Description</dt>
          <dd>{reading.description}</dd>
        </div>
        <div>
          <dt>Fetched at</dt>
          <dd>{formatFetchedAt(reading.fetched_at)}</dd>
        </div>
      </dl>
    </>
  );
}

function App() {
  const [cityInput, setCityInput] = useState('');
  const [activeCity, setActiveCity] = useState('');
  const [latest, setLatest] = useState(null);
  const [readings, setReadings] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const weatherCondition = useMemo(
    () =>
      latest
        ? getWeatherCondition({
            description: latest.description,
            wind_speed: latest.wind_speed,
            fetched_at: latest.fetched_at,
          })
        : 'cloudy',
    [latest],
  );

  const showWindOverlay = latest ? isWindyOverlay(latest.wind_speed) : false;

  async function handleSubmit(event) {
    event.preventDefault();
    const city = cityInput.trim();
    if (!city) {
      setError('Please enter a city name.');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const newReading = await fetchWeather(city);
      const canonicalCity = newReading.city;
      const history = await getWeatherByCity(canonicalCity);
      setActiveCity(canonicalCity);
      setLatest(newReading);
      setReadings(history);
    } catch (err) {
      setLatest(null);
      setReadings([]);
      setActiveCity('');
      setError(err.message ?? 'Something went wrong.');
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="app-shell">
      <WeatherBackground
        condition={weatherCondition}
        showWindOverlay={showWindOverlay}
      />

      <div className="app">
        <motion.header
          initial={{ opacity: 0, y: -12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <h1>Weather Aggregator</h1>
          <p>Fetch and browse stored weather readings for a city.</p>
        </motion.header>

        <motion.form
          className="city-form glass-panel"
          onSubmit={handleSubmit}
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.08 }}
        >
          <label htmlFor="city-input">City</label>
          <div className="city-form-row">
            <input
              id="city-input"
              type="text"
              value={cityInput}
              onChange={(e) => setCityInput(e.target.value)}
              placeholder="e.g. Timisoara"
              disabled={loading}
              autoComplete="off"
            />
            <motion.button
              type="submit"
              disabled={loading}
              whileHover={{ scale: 1.03 }}
              whileTap={{ scale: 0.98 }}
              transition={{ type: 'spring', stiffness: 400, damping: 20 }}
            >
              {loading ? 'Fetching…' : 'Fetch weather'}
            </motion.button>
          </div>
        </motion.form>

        <AnimatePresence mode="wait">
          {error && (
            <motion.p
              className="message message-error glass-panel"
              role="alert"
              key="error"
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0 }}
              transition={{ duration: 0.3 }}
            >
              {error}
            </motion.p>
          )}
        </AnimatePresence>

        <AnimatePresence mode="wait">
          {latest && (
            <motion.section
              className="panel glass-panel"
              aria-labelledby="latest-heading"
              key={`latest-${weatherCondition}-${latest.fetched_at}`}
              {...panelMotion}
            >
              <h2 id="latest-heading">Latest reading</h2>
              <p className="panel-subtitle">
                Most recent fetch for {activeCity}
              </p>
              <ReadingDetails reading={latest} condition={weatherCondition} />
            </motion.section>
          )}
        </AnimatePresence>

        <AnimatePresence mode="wait">
          {activeCity && (
            <motion.section
              className="panel glass-panel"
              aria-labelledby="history-heading"
              key={`history-${activeCity}-${readings.length}`}
              {...panelMotion}
              transition={{ ...panelMotion.transition, delay: 0.06 }}
            >
              <h2 id="history-heading">All readings for {activeCity}</h2>
              {readings.length === 0 ? (
                <p className="empty-state">No stored readings yet.</p>
              ) : (
                <div className="table-wrap">
                  <table>
                    <thead>
                      <tr>
                        <th>City</th>
                        <th>Temperature</th>
                        <th>Wind speed</th>
                        <th>Description</th>
                        <th>Fetched at</th>
                      </tr>
                    </thead>
                    <tbody>
                      {readings.map((reading, index) => (
                        <motion.tr
                          key={`${reading.fetched_at}-${reading.temperature}`}
                          className="forecast-row"
                          initial={{ opacity: 0, x: -8 }}
                          animate={{ opacity: 1, x: 0 }}
                          transition={{ delay: index * 0.04, duration: 0.35 }}
                          whileHover={{
                            scale: 1.01,
                            backgroundColor: 'rgba(255, 255, 255, 0.55)',
                          }}
                        >
                          <td>{reading.city}</td>
                          <td>{reading.temperature} °C</td>
                          <td>{reading.wind_speed} km/h</td>
                          <td>{reading.description}</td>
                          <td>{formatFetchedAt(reading.fetched_at)}</td>
                        </motion.tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </motion.section>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
}

export default App;
