import os

import requests


def fetch_movie_data(movie_id: int) -> dict:
    """
    Fetch movie details from TMDB, including title, tagline, genres, and poster URL.
    Returns None if there's an error or if TMDB_API_KEY is not set.
    """
    api_key = os.environ.get('TMDB_API_KEY')
    if not api_key:
        return None

    base_url = 'https://api.themoviedb.org/3'
    movie_url = f'{base_url}/movie/{movie_id}'
    config_url = f'{base_url}/configuration'

    try:
        # Fetch configuration details to build the full poster path
        config_resp = requests.get(config_url, params={'api_key': api_key})
        config_resp.raise_for_status()
        config_data = config_resp.json()
        images_data = config_data.get('images', {})
        base_image_url = images_data.get('secure_base_url', 'https://image.tmdb.org/t/p/')
        poster_sizes = images_data.get('poster_sizes', [])
        poster_size = 'w500'
        if 'w342' in poster_sizes:
            poster_size = 'w342'

        # Fetch the movie details
        movie_resp = requests.get(movie_url, params={'api_key': api_key})
        movie_resp.raise_for_status()
        movie_data = movie_resp.json()

        title = movie_data.get('title', 'Unknown Title')
        tagline = movie_data.get('tagline', '')
        genres = (
            [g['name'] for g in movie_data.get('genres', [])] if movie_data.get('genres') else []
        )
        poster_path = movie_data.get('poster_path')
        if poster_path:
            poster_url = f'{base_image_url}{poster_size}{poster_path}'
        else:
            poster_url = 'https://via.placeholder.com/300x450.png?text=No+Image'

        return {'title': title, 'tagline': tagline, 'genres': genres, 'poster_url': poster_url}
    except requests.RequestException:
        return None
