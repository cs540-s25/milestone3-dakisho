import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';

function Login({ setIsAuthenticated, setUser }) {
  const [username, setUsername] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('/api/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username }),
      });

      const data = await response.json();

      if (response.ok) {
        setIsAuthenticated(true);
        setUser(data.user);
        navigate('/');
      } else {
        setError(data.message || 'Login failed');
      }
    } catch (err) {
      setError('An error occurred. Please try again.');
    }
  };

  return (
    <div className="auth-container">
      <h2>Login</h2>
      {error && <p className="error">{error}</p>}
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="username">
            Username
            <input
              type="text"
              id="username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
          </label>
        </div>
        <button type="submit">Login</button>
      </form>
      <p>
        Don&apos;t have an account?
        {' '}
        <Link to="/signup">Sign Up</Link>
      </p>
    </div>
  );
}

export default Login;