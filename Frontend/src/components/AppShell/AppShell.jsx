import { useRef, useState } from 'react';
import Header from '../Header/Header.jsx';

const messages = {
  invalid_input: 'Enter a 17-digit SteamID64 or a Steam Community profile URL.',
  not_found: 'Steam could not find this profile. Check the ID or profile name and try again.',
  hidden:
    'Game details are hidden or unavailable. Check the profile’s game detail visibility and try again.',
  rate_limited: 'Steam requests are temporarily limited. Wait and try again.',
  configuration: 'The backend Steam API key is not configured. Configure it locally and try again.',
  unavailable: 'Steam or the local backend is unavailable. Check the connection and try again.',
};

export default function AppShell() {
  const [profile, setProfile] = useState('');
  const [pending, setPending] = useState(false);
  const [error, setError] = useState('');
  const [library, setLibrary] = useState(null);
  const request = useRef(null);
  async function load(event) {
    event.preventDefault();
    if (request.current) return;
    if (!profile.trim()) {
      setError(messages.invalid_input);
      return;
    }
    const controller = new AbortController();
    request.current = controller;
    setPending(true);
    setError('');
    setLibrary(null);
    try {
      const response = await fetch('/api/library/import', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ profile }),
        signal: controller.signal,
      });
      const result = await response.json();
      if (request.current !== controller) return;
      if (!response.ok) throw new Error(messages[result.detail] || messages.unavailable);
      setLibrary(result);
    } catch (err) {
      if (request.current === controller)
        setError(
          Object.values(messages).includes(err.message) ? err.message : messages.unavailable,
        );
    } finally {
      if (request.current === controller) {
        request.current = null;
        setPending(false);
      }
    }
  }
  function cancel() {
    request.current?.abort();
    request.current = null;
    setPending(false);
    setError('Load canceled. You can try again.');
  }
  return (
    <div className="app-shell">
      <Header />
      <main>
        <h1>Load library</h1>
        <p>Load public Steam game details with a SteamID64 or Steam Community profile URL.</p>
        <p>Live imports require internet and a locally configured backend Steam Web API key.</p>
        <form onSubmit={load}>
          <label htmlFor="profile">SteamID64 or Steam profile URL</label>
          <input
            id="profile"
            value={profile}
            onChange={(event) => {
              if (request.current) {
                request.current.abort();
                request.current = null;
                setPending(false);
              }
              setLibrary(null);
              setError('');
              setProfile(event.target.value);
            }}
            aria-describedby="profile-help profile-error"
            maxLength={256}
          />
          <p id="profile-help">Your profile and game details must be visible to Steam.</p>
          <p id="profile-error" role="alert">
            {error}
          </p>
          <button type="submit" disabled={pending}>
            {pending ? 'Loading…' : library ? 'Refresh' : 'Load library'}
          </button>
          {pending && (
            <button type="button" onClick={cancel}>
              Cancel
            </button>
          )}
        </form>
        <p role="status">{pending ? 'Loading profile and public game details…' : ''}</p>
        {library && (
          <section aria-labelledby="library-title">
            <h2 id="library-title">Library: {library.name}</h2>
            <p>
              Imported {library.imported_at}. Source:{' '}
              <a href="https://steamcommunity.com/">Steam</a>.
            </p>
            {library.partial && <p>Some game details were unavailable; this import is partial.</p>}
            {library.games.length === 0 ? (
              <p>
                {library.partial
                  ? 'No usable game rows were returned.'
                  : 'No games were returned in this visible library.'}
              </p>
            ) : (
              <ul>
                {library.games.map((game) => (
                  <li key={game.appid}>{game.name || `App ${game.appid}`}</li>
                ))}
              </ul>
            )}
          </section>
        )}
        <p>
          Steam data is provided as is, with all faults and as available. Valve and its suppliers
          disclaim warranties and liability to the extent permitted by law.
        </p>
      </main>
    </div>
  );
}
