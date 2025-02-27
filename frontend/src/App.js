import React, { useState } from 'react';
import './App.css';

function App() {
  const [scanResults, setScanResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [config, setConfig] = useState({
    api: {
      base_url: '',
      endpoints: [''],
    }
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const response = await fetch('http://localhost:5000/scan', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(config),
      });
      const data = await response.json();
      setScanResults(data);
    } catch (error) {
      console.error('Error:', error);
    }
    setLoading(false);
  };

  const addEndpoint = () => {
    setConfig({
      ...config,
      api: {
        ...config.api,
        endpoints: [...config.api.endpoints, '']
      }
    });
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>SecuAPI Scanner</h1>
      </header>
      <main>
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Base URL:</label>
            <input
              type="url"
              value={config.api.base_url}
              onChange={(e) => setConfig({
                ...config,
                api: { ...config.api, base_url: e.target.value }
              })}
              required
            />
          </div>
          
          <div className="form-group">
            <label>Endpoints:</label>
            {config.api.endpoints.map((endpoint, index) => (
              <input
                key={index}
                type="text"
                value={endpoint}
                onChange={(e) => {
                  const newEndpoints = [...config.api.endpoints];
                  newEndpoints[index] = e.target.value;
                  setConfig({
                    ...config,
                    api: { ...config.api, endpoints: newEndpoints }
                  });
                }}
              />
            ))}
            <button type="button" onClick={addEndpoint}>Add Endpoint</button>
          </div>

          <button type="submit" disabled={loading}>
            {loading ? 'Scanning...' : 'Start Scan'}
          </button>
        </form>

        {scanResults && (
          <div className="results">
            <h2>Scan Results</h2>
            <pre>{JSON.stringify(scanResults, null, 2)}</pre>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
