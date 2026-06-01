import { describe, it, expect } from 'vitest';
import { getWeatherCondition, getWeatherEmoji } from './weatherCondition';

describe('getWeatherCondition', () => {
  it('maps clear sky to sunny during day', () => {
    expect(
      getWeatherCondition({
        description: 'Clear sky',
        wind_speed: 10,
        fetched_at: '2024-06-01T14:00:00',
      }),
    ).toBe('sunny');
  });

  it('maps overcast to cloudy', () => {
    expect(
      getWeatherCondition({
        description: 'Overcast',
        wind_speed: 10,
        fetched_at: '2024-06-01T14:00:00',
      }),
    ).toBe('cloudy');
  });

  it('maps thunderstorm to stormy', () => {
    expect(
      getWeatherCondition({
        description: 'Thunderstorm',
        wind_speed: 10,
        fetched_at: '2024-06-01T14:00:00',
      }),
    ).toBe('stormy');
  });
});

describe('getWeatherEmoji', () => {
  it('returns emoji for condition', () => {
    expect(getWeatherEmoji('rainy')).toBe('🌧️');
  });
});
