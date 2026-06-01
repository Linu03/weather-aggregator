import { useMemo } from 'react';
import './WeatherBackground.css';

const RAIN_COUNT = 24;
const SNOW_COUNT = 28;
const STAR_COUNT = 40;
const WIND_LINES = 10;
const WIND_PARTICLES = 12;

function RainLayer() {
  const drops = useMemo(
    () =>
      Array.from({ length: RAIN_COUNT }, (_, i) => ({
        id: i,
        left: `${(i * 4.3) % 100}%`,
        duration: `${0.6 + (i % 5) * 0.15}s`,
        delay: `${(i % 7) * 0.12}s`,
      })),
    [],
  );

  return (
    <>
      {drops.map((d) => (
        <span
          key={d.id}
          className="weather-bg__raindrop"
          style={{ left: d.left, animationDuration: d.duration, animationDelay: d.delay }}
        />
      ))}
      <span className="weather-bg__splash" style={{ left: '20%' }} />
      <span className="weather-bg__splash" style={{ left: '55%', animationDelay: '0.8s' }} />
      <span className="weather-bg__splash" style={{ left: '78%', animationDelay: '1.4s' }} />
    </>
  );
}

function SnowLayer() {
  const flakes = useMemo(
    () =>
      Array.from({ length: SNOW_COUNT }, (_, i) => ({
        id: i,
        left: `${(i * 3.7) % 100}%`,
        size: `${6 + (i % 8)}px`,
        duration: `${8 + (i % 10)}s`,
        delay: `${(i % 12) * 0.4}s`,
        drift: `${-30 + (i % 60)}px`,
      })),
    [],
  );

  return (
    <>
      {flakes.map((f) => (
        <span
          key={f.id}
          className="weather-bg__snowflake"
          style={{
            left: f.left,
            '--size': f.size,
            '--duration': f.duration,
            '--delay': f.delay,
            '--drift': f.drift,
          }}
        >
          ✦
        </span>
      ))}
    </>
  );
}

function WindLayer() {
  const lines = useMemo(
    () =>
      Array.from({ length: WIND_LINES }, (_, i) => ({
        id: `l-${i}`,
        top: `${8 + (i * 7) % 75}%`,
        w: `${40 + (i % 5) * 20}px`,
        duration: `${2 + (i % 4) * 0.5}s`,
        delay: `${(i % 6) * 0.3}s`,
      })),
    [],
  );
  const particles = useMemo(
    () =>
      Array.from({ length: WIND_PARTICLES }, (_, i) => ({
        id: `p-${i}`,
        top: `${10 + (i * 6) % 80}%`,
        duration: `${3 + (i % 3)}s`,
        delay: `${(i % 8) * 0.25}s`,
        y: `${-10 + (i % 20)}px`,
      })),
    [],
  );

  return (
    <>
      {lines.map((l) => (
        <span
          key={l.id}
          className="weather-bg__wind-line"
          style={{
            top: l.top,
            '--w': l.w,
            '--duration': l.duration,
            '--delay': l.delay,
          }}
        />
      ))}
      {particles.map((p) => (
        <span
          key={p.id}
          className="weather-bg__particle"
          style={{
            top: p.top,
            '--duration': p.duration,
            '--delay': p.delay,
            '--y': p.y,
          }}
        />
      ))}
    </>
  );
}

function NightLayer() {
  const stars = useMemo(
    () =>
      Array.from({ length: STAR_COUNT }, (_, i) => ({
        id: i,
        left: `${(i * 2.9) % 98}%`,
        top: `${(i * 4.1) % 55}%`,
        duration: `${2 + (i % 4)}s`,
        delay: `${(i % 10) * 0.35}s`,
      })),
    [],
  );

  return (
    <>
      <div className="weather-bg__moon" aria-hidden />
      {stars.map((s) => (
        <span
          key={s.id}
          className="weather-bg__star"
          style={{
            left: s.left,
            top: s.top,
            '--duration': s.duration,
            '--delay': s.delay,
          }}
        />
      ))}
    </>
  );
}

export default function WeatherBackground({ condition, showWindOverlay }) {
  const theme = condition || 'cloudy';

  return (
    <div className={`weather-bg weather-bg--${theme}`} aria-hidden>
      <div className="weather-bg__gradient" />

      {theme === 'sunny' && (
        <div className="weather-bg__sun">
          <div className="weather-bg__sun-rays" />
          <div className="weather-bg__sun-core" />
        </div>
      )}

      {(theme === 'cloudy' || theme === 'stormy') && (
        <>
          <span className="weather-bg__cloud weather-bg__cloud--1" />
          <span className="weather-bg__cloud weather-bg__cloud--2" />
          <span className="weather-bg__cloud weather-bg__cloud--3" />
        </>
      )}

      {theme === 'rainy' && <RainLayer />}

      {theme === 'stormy' && (
        <>
          <div className="weather-bg__storm-cloud" />
          <div className="weather-bg__lightning" />
          <RainLayer />
        </>
      )}

      {theme === 'snowy' && <SnowLayer />}

      {(theme === 'windy' || showWindOverlay) && <WindLayer />}

      {theme === 'foggy' && (
        <>
          <span className="weather-bg__fog weather-bg__fog--1" />
          <span className="weather-bg__fog weather-bg__fog--2" />
          <span className="weather-bg__fog weather-bg__fog--3" />
        </>
      )}

      {theme === 'night' && <NightLayer />}
    </div>
  );
}
