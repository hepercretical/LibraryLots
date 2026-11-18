import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { expect, test, vi } from 'vitest';
import AppShell from './AppShell.jsx';

test('checks health using the keyboard and disables duplicate requests', async () => {
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
  await user.tab();
  await user.tab();
  await user.keyboard('{Enter}');
  expect(screen.getByRole('button')).toBeDisabled();
  finish({ ok: true, json: async () => ({ status: 'ok', service: 'library-lots-backend' }) });
  expect(await screen.findByText('Backend connected.')).toBeVisible();
  expect(screen.getByRole('button')).toBeEnabled();
  expect(fetch).toHaveBeenCalledTimes(1);
});
test.each([
  ['network failure', () => Promise.reject(new Error('offline'))],
  ['HTTP failure', async () => ({ ok: false })],
  ['invalid payload', async () => ({ ok: true, json: async () => ({ status: 'ok' }) })],
])('recovers from %s', async (_, response) => {
  vi.stubGlobal('fetch', vi.fn(response));
  const user = userEvent.setup();
  render(<AppShell />);
  await user.click(screen.getByRole('button'));
  expect(await screen.findByText(/Unable to connect/)).toBeVisible();
  fetch.mockResolvedValue({
    ok: true,
    json: async () => ({ status: 'ok', service: 'library-lots-backend' }),
  });
  await user.click(screen.getByRole('button'));
  expect(await screen.findByText('Backend connected.')).toBeVisible();
});
