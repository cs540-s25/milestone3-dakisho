import React, {
  useState,
  useEffect,
} from 'react';
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from 'react-router-dom';
import Login from './components/Login';
import Signup from './components/Signup';
import Movie from './components/Movie';
import MyRatings from './components/MyRatings';
import Navbar from './components/Navbar';

// Define ProtectedRoute component outside of App
// Changed to function declaration to satisfy react/function-component-definition
function ProtectedRoute({ children, isAuthenticated }) {
  if (!isAuthenticated) {
    return <Navigate to="/login" />;
  }
  return children;
}

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState(null);

  useEffect(() => {
    // Check if user is logged in
    fetch('/api/check-auth')
      .then((response) => {
        if (response.ok) {
          return response.json();
        }
        throw new Error('Not authenticated');
      })
      .then((data) => {
        setIsAuthenticated(true);
        setUser(data.user);
      })
      .catch(() => {
        setIsAuthenticated(false);
        setUser(null);
      });
  }, []);

  return (
    <Router>
      <div className="app">
        {isAuthenticated && <Navbar setIsAuthenticated={setIsAuthenticated} />}
        <Routes>
          <Route path="/login" element={<Login setIsAuthenticated={setIsAuthenticated} setUser={setUser} />} />
          <Route path="/signup" element={<Signup />} />
          <Route
            path="/"
            element={(
              <ProtectedRoute isAuthenticated={isAuthenticated}>
                <Movie user={user} />
              </ProtectedRoute>
            )}
          />
          <Route
            path="/my-ratings"
            element={(
              <ProtectedRoute isAuthenticated={isAuthenticated}>
                <MyRatings user={user} />
              </ProtectedRoute>
            )}
          />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
