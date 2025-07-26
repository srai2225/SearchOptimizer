import React, { useState } from 'react';
import './App.css';

function App() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [error, setError] = useState('');

  const handleSearch = async () => {
    try {
      const response = await fetch('http://127.0.0.1:8000/semantic-search', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query })  // ✅ Fixed key
      });

      if (!response.ok) {
        throw new Error('Search request failed');
      }

      const data = await response.json();
      setResults(data);
      setError('');
    } catch (err) {
      setError(err.message);
      setResults([]);
    }
  };

  return (
    <div className="app-container">
      <nav className="navbar">
        <div className="logo">Flipkart Grid</div>
        <div className="search-bar">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search for products..."
          />
          <button onClick={handleSearch}>Search</button>
        </div>
      </nav>

      {error && <p className="error">{error}</p>}

      <div className="grid-container">
        {results.map((item, index) => (
          <div key={index} className="product-card">
            <h3>{item.title}</h3>
            <p>{item.description}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;
