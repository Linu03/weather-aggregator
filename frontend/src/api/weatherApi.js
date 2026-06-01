const API_BASE = import.meta.env.VITE_API_BASE_URL ?? '';

async function parseError(response) {
  try {
    const body = await response.json();
    if (body?.detail) {
      return typeof body.detail === 'string' ? body.detail : JSON.stringify(body.detail);
    }
  } catch {
    /* ignore */
  }
  return `Request failed (${response.status})`;
}

async function request(url, options) {
  const response = await fetch(`${API_BASE}${url}`, options);
  if (!response.ok) {
    throw new Error(await parseError(response));
  }
  return response.json();
}

export function fetchWeather(city) {
  const params = new URLSearchParams({ city });
  return request(`/weather/fetch?${params}`, { method: 'POST' });
}

export function getWeatherByCity(city) {
  return request(`/weather/${encodeURIComponent(city)}`);
}

export function getLatestWeather(city) {
  return request(`/weather/${encodeURIComponent(city)}/latest`);
}
