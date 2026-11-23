import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { expect, test, vi } from 'vitest';
import AppShell from './AppShell.jsx';

test('validates and loads a library, disabling duplicate requests', async () => {
  let finish;
  vi.stubGlobal(
    'fetch',
    vi.fn(
      () =>
        new Promise((resolve) => {
          finish = resolve;
        }),
    ),
  );
  const user = userEvent.setup();
  render(<AppShell />);
  await user.click(screen.getByRole('button', { name: 'Load library' }));
  expect(screen.getByRole('alert')).toHaveTextContent('17-digit');
  await user.type(screen.getByLabelText(/SteamID64 or Steam profile URL/), '76561198000000000');
  await user.click(screen.getByRole('button', { name: 'Load library' }));
  expect(screen.getByRole('button', { name: 'Loading…' })).toBeDisabled();
  finish({ ok: true, json: async () => ({ name: 'Example', imported_at: 'now', games: [] }) });
  expect(await screen.findByText(/No games were returned/)).toBeVisible();
  expect(fetch).toHaveBeenCalledTimes(1);
});
test('reports hidden details and allows retry', async () => {
  vi.stubGlobal(
    'fetch',
    vi.fn().mockResolvedValue({ ok: false, json: async () => ({ detail: 'hidden' }) }),
  );
  const user = userEvent.setup();
  render(<AppShell />);
  await user.type(screen.getByLabelText(/SteamID64 or Steam profile URL/), '76561198000000000');
  await user.click(screen.getByRole('button', { name: 'Load library' }));
  expect(await screen.findByText(/Game details are hidden/)).toBeVisible();
  expect(screen.getByRole('button', { name: 'Load library' })).toBeEnabled();
});

test('switching profiles discards an old response', async () => {
  let finish;
  vi.stubGlobal(
    'fetch',
    vi
      .fn()
      .mockImplementationOnce(
        () =>
          new Promise((resolve) => {
            finish = resolve;
          }),
      )
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({ name: 'New', imported_at: 'now', games: [] }),
      }),
  );
  const user = userEvent.setup();
  render(<AppShell />);
  const input = screen.getByLabelText(/SteamID64 or Steam profile URL/);
  await user.type(input, '76561198000000000');
  await user.click(screen.getByRole('button', { name: 'Load library' }));
  await user.clear(input);
  await user.type(input, '76561198000000001');
  await user.click(screen.getByRole('button', { name: 'Load library' }));
  expect(await screen.findByText('Library: New')).toBeVisible();
  finish({ ok: true, json: async () => ({ name: 'Old', games: [] }) });
  expect(screen.queryByText('Library: Old')).not.toBeInTheDocument();
});
