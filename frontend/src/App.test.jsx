import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';

vi.mock('framer-motion', async () => {
  const actual = await vi.importActual('framer-motion');
  return {
    ...actual,
    AnimatePresence: ({ children }) => children,
  };
});
import { render, screen, waitFor, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import App from './App';

const sampleReading = {
  city: 'Timisoara',
  temperature: 22.4,
  wind_speed: 10.5,
  description: 'Overcast',
  fetched_at: '2024-06-01T12:00:00',
};

describe('App', () => {
  beforeEach(() => {
    vi.stubGlobal('fetch', vi.fn());
  });

  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it('fetches weather and shows latest reading and history table', async () => {
    const user = userEvent.setup();

    fetch
      .mockResolvedValueOnce({
        ok: true,
        json: async () => sampleReading,
      })
      .mockResolvedValueOnce({
        ok: true,
        json: async () => [sampleReading],
      });

    render(<App />);

    await user.type(screen.getByLabelText(/city/i), 'Timisoara');
    await user.click(screen.getByRole('button', { name: /fetch weather/i }));

    await waitFor(() => {
      expect(screen.getByRole('heading', { name: /latest reading/i })).toBeInTheDocument();
    });

    const latestSection = screen
      .getByRole('heading', { name: /latest reading/i })
      .closest('section');
    expect(within(latestSection).getByText('22.4 °C')).toBeInTheDocument();
    expect(within(latestSection).getByText('Overcast')).toBeInTheDocument();
    expect(screen.getByRole('heading', { name: /all readings for timisoara/i })).toBeInTheDocument();

    await waitFor(() => {
      expect(screen.getByRole('cell', { name: /22\.4/i })).toBeInTheDocument();
    });
  });

  it('shows an error when fetch fails', async () => {
    const user = userEvent.setup();

    fetch.mockResolvedValueOnce({
      ok: false,
      status: 404,
      json: async () => ({ detail: 'City not found: Nowhere' }),
    });

    render(<App />);

    await user.type(screen.getByLabelText(/city/i), 'Nowhere');
    await user.click(screen.getByRole('button', { name: /fetch weather/i }));

    await waitFor(() => {
      expect(screen.getByRole('alert')).toHaveTextContent('City not found: Nowhere');
    });
  });
});
