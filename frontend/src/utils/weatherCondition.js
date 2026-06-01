/**
 * Maps API weather descriptions to visual animation themes.
 */
export function getWeatherCondition({ description, wind_speed, fetched_at }) {
  const d = (description ?? '').toLowerCase();
  const hour = fetched_at ? new Date(fetched_at).getHours() : new Date().getHours();
  const isNight = hour >= 20 || hour < 6;
  const windy = (wind_speed ?? 0) >= 40;

  if (d.includes('thunder')) return 'stormy';
  if (d.includes('snow')) return 'snowy';
  if (d.includes('rain') || d.includes('drizzle') || d.includes('shower')) return 'rainy';
  if (d.includes('fog')) return 'foggy';
  if (windy && !d.includes('rain') && !d.includes('snow')) return 'windy';
  if (d.includes('overcast') || d.includes('cloud') || d.includes('partly')) return 'cloudy';
  if (d.includes('clear') || d.includes('mainly clear')) return isNight ? 'night' : 'sunny';

  return isNight ? 'night' : 'cloudy';
}

export function isWindyOverlay(wind_speed) {
  return (wind_speed ?? 0) >= 28;
}

export function getWeatherEmoji(condition) {
  const map = {
    sunny: '☀️',
    cloudy: '☁️',
    rainy: '🌧️',
    stormy: '⛈️',
    snowy: '❄️',
    windy: '💨',
    foggy: '🌫️',
    night: '🌙',
  };
  return map[condition] ?? '🌤️';
}
