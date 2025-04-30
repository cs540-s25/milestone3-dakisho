import React, { useState, useEffect } from 'react';

function MyRatings() {
  const [ratings, setRatings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [saveStatus, setSaveStatus] = useState(null);

  useEffect(() => {
    fetchUserRatings();
  }, []);

  const fetchUserRatings = async () => {
    try {
      setLoading(true);
      const response = await fetch('/api/ratings');
      if (!response.ok) throw new Error('Failed to fetch ratings');
      
      const data = await response.json();
      setRatings(data.ratings || []);
      setLoading(false);
    } catch (err) {
      setError('Failed to load your ratings');
      setLoading(false);
    }
  };

  const handleDeleteRating = (ratingId) => {
    setRatings(ratings.filter((rating) => rating.id !== ratingId));
  };

  const handleRatingChange = (ratingId, newScore) => {
    setRatings(ratings.map((rating) => {
      if (rating.id === ratingId) {
        return { ...rating, score: parseInt(newScore, 10) };
      }
      return rating;
    }));
  };

  const handleCommentChange = (ratingId, newComment) => {
    setRatings(ratings.map((rating) => {
      if (rating.id === ratingId) {
        return { ...rating, comment: newComment };
      }
      return rating;
    }));
  };

  const handleSaveChanges = async () => {
    try {
      const response = await fetch('/api/ratings/update', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ ratings }),
      });

      if (!response.ok) throw new Error('Failed to save changes');
      
      const data = await response.json();
      setSaveStatus({ success: true, message: data.message || 'Changes saved successfully' });
      
      // Refresh ratings from server
      fetchUserRatings();
      
      // Clear status after 3 seconds
      setTimeout(() => setSaveStatus(null), 3000);
    } catch (err) {
      setSaveStatus({ success: false, message: 'Failed to save changes' });
    }
  };

  if (loading) return <div>Loading...</div>;
  if (error) return <div className="error">{error}</div>;

  return (
    <div className="my-ratings-container">
      <h1>My Movie Ratings</h1>
      
      {saveStatus && (
        <div className={`status-message ${saveStatus.success ? 'success' : 'error'}`}>
          {saveStatus.message}
        </div>
      )}

      {ratings.length === 0 ? (
        <p>You haven't rated any movies yet.</p>
      ) : (
        <div>
          <div className="ratings-list">
            {ratings.map((rating) => (
              <div key={rating.id} className="rating-item">
                <div className="rating-header">
                  <h3>{rating.movie_title}</h3>
                  <button
                    type="button"
                    className="delete-btn"
                    onClick={() => handleDeleteRating(rating.id)}
                  >
                    Delete
                  </button>
                </div>
                <div className="rating-details">
                  <div className="form-group">
                    <label htmlFor={`rating-${rating.id}`}>
                      Rating (1-10):
                      <input
                        type="number"
                        id={`rating-${rating.id}`}
                        min="1"
                        max="10"
                        value={rating.score}
                        onChange={(e) => handleRatingChange(rating.id, e.target.value)}
                      />
                    </label>
                  </div>
                  <div className="form-group">
                    <label htmlFor={`comment-${rating.id}`}>
                      Comment:
                      <textarea
                        id={`comment-${rating.id}`}
                        value={rating.comment || ''}
                        onChange={(e) => handleCommentChange(rating.id, e.target.value)}
                        rows="3"
                      />
                    </label>
                  </div>
                </div>
              </div>
            ))}
          </div>
          <button type="button" className="save-btn" onClick={handleSaveChanges}>
            Save Changes
          </button>
        </div>
      )}
    </div>
  );
}

export default MyRatings;