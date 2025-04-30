import React, { useState, useEffect } from 'react';

function Movie() {
  const [movie, setMovie] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [userRating, setUserRating] = useState('');
  const [userComment, setUserComment] = useState('');
  const [allRatings, setAllRatings] = useState([]);

  useEffect(() => {
    fetchMovie();
  }, []);

  const fetchMovie = async () => {
    try {
      setLoading(true);
      const response = await fetch('/api/movie/random');
      if (!response.ok) throw new Error('Failed to fetch movie');
      
      const data = await response.json();
      setMovie(data.movie);
      setAllRatings(data.ratings || []);
      
      // Check if current user has rated this movie
      const userRatingData = data.user_rating;
      if (userRatingData) {
        setUserRating(userRatingData.score.toString());
        setUserComment(userRatingData.comment || '');
      } else {
        setUserRating('');
        setUserComment('');
      }
      
      setLoading(false);
    } catch (err) {
      setError('Failed to load movie data');
      setLoading(false);
    }
  };

  const handleSubmitRating = async (e) => {
    e.preventDefault();
    try {
      const score = parseInt(userRating, 10);
      if (score < 1 || score > 10 || Number.isNaN(score)) {
        setError('Rating must be a number between 1 and 10');
        return;
      }

      const response = await fetch('/api/movie/rate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          movie_id: movie.id,
          movie_title: movie.title,
          score,
          comment: userComment,
        }),
      });

      if (!response.ok) throw new Error('Failed to submit rating');
      
      // Refresh movie data
      fetchMovie();
      setError(null);
    } catch (err) {
      setError('Failed to submit rating');
    }
  };

  if (loading) return <div>Loading...</div>;
  if (error) return <div className="error">{error}</div>;
  if (!movie) return <div>No movie data available</div>;

  return (
    <div className="movie-container">
      <div className="movie-details">
        <h1>{movie.title}</h1>
        <p className="tagline">{movie.tagline}</p>
        <p>Genres: {movie.genres}</p>
        
        {movie.poster_url && (
          <img 
            src={movie.poster_url} 
            alt={`${movie.title} poster`} 
            className="movie-poster" 
          />
        )}
        
        {movie.wiki_url && (
          <p>
            <a href={movie.wiki_url} target="_blank" rel="noopener noreferrer">
              Read more on Wikipedia
            </a>
          </p>
        )}
      </div>

      <div className="rating-form">
        <h2>Rate this movie</h2>
        <form onSubmit={handleSubmitRating}>
          <div className="form-group">
            <label htmlFor="rating">
              Rating (1-10):
              <input
                type="number"
                id="rating"
                min="1"
                max="10"
                value={userRating}
                onChange={(e) => setUserRating(e.target.value)}
                required
              />
            </label>
          </div>
          <div className="form-group">
            <label htmlFor="comment">
              Comment:
              <textarea
                id="comment"
                value={userComment}
                onChange={(e) => setUserComment(e.target.value)}
                rows="4"
              />
            </label>
          </div>
          <button type="submit">Submit Rating</button>
        </form>
      </div>

      <div className="all-ratings">
        <h2>All Ratings</h2>
        {allRatings.length === 0 ? (
          <p>No ratings yet</p>
        ) : (
          <ul>
            {allRatings.map((rating) => (
              <li key={rating.id}>
                <strong>{rating.user_username}</strong>: {rating.score}/10
                {rating.comment && <p>{rating.comment}</p>}
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}

export default Movie;