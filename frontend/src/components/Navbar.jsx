import React from 'react';
import { Link, useNavigate } from 'react-router-dom';

function Navbar({ setIsAuthenticated }) {
  const navigate = useNavigate();

  const handleLogout = async () => {
    try {
      await fetch('/api/logout');
      setIsAuthenticated(false);
      navigate('/login');
    } catch (error) {
      // Handle error
    }
  };

  return (
    <nav className="navbar">
      <ul>
        <li>
          <Link to="/">Home</Link>
        </li>
        <li>
          <Link to="/my-ratings">My Ratings</Link>
        </li>
        <li>
          <button type="button" onClick={handleLogout}>Logout</button>
        </li>
      </ul>
    </nav>
  );
}

export default Navbar;