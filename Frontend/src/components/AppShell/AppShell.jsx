import { useState } from 'react';
import Header from '../Header/Header.jsx';

export default function AppShell() {
  const [status, setStatus] = useState('');
  const [pending, setPending] = useState(false);
  async function checkBackend() {
    setPending(true);
    setStatus('Checking local backend...');
    try {
      const response = await fetch('/api/health', { signal: AbortSignal.timeout(5000) });
      if (!response.ok) throw new Error('Backend unavailable');
      const result = await response.json();
      if (result.status !== 'ok' || result.service !== 'library-lots-backend')
        throw new Error('Invalid response');
      setStatus('Backend connected.');
    } catch {
      setStatus('Unable to connect. Start the Python service and try again.');
    } finally {
      setPending(false);
    }
  }
  return (
    <div className="app-shell">
      <Header />
      <main>
        <h1>Local development connection</h1>
        <p>Check the connection between Library Lots and its local Python service.</p>
        <button type="button" onClick={checkBackend} disabled={pending}>
          {pending ? 'Checking...' : 'Check local backend'}
        </button>
        <p role="status">{status}</p>
        <p>Live Steam imports require internet access and a backend Steam Web API key.</p>
      </main>
    </div>
  );
}
