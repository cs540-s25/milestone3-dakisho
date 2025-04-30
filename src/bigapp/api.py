import random
from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user, login_user, logout_user

from .models import db, User, Rating
from .tmdb import fetch_movie_data
from .wiki import fetch_wikipedia_link

api = Blueprint('api', __name__, url_prefix='/api')

MOVIE_IDS = [
    550,  # Fight Club
    300668,
    329865,
    335984,
    157336,
    675353,
]

@api.route('/check-auth')
def check_auth():
    if current_user.is_authenticated:
        return jsonify({
            'authenticated': True,
            'user': {
                'id': current_user.id,
                'username': current_user.username
            }
        })
    return jsonify({'authenticated': False}), 401

@api.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    
    user = User.query.filter_by(username=username).first()
    
    if not user:
        return jsonify({'message': 'Invalid username'}), 401
    
    login_user(user)
    return jsonify({
        'message': 'Login successful',
        'user': {
            'id': user.id,
            'username': user.username
        }
    })

@api.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    
    user = User.query.filter_by(username=username).first()
    
    if user:
        return jsonify({'message': 'Username already exists'}), 400
    
    new_user = User(username=username)
    
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({'message': 'Signup successful'})

@api.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logout successful'})

@api.route('/movie/random')
@login_required
def random_movie():
    random_movie_id = random.choice(MOVIE_IDS)
    tmdb_info = fetch_movie_data(random_movie_id)
    wiki_link = None

    if tmdb_info:
        wiki_link = fetch_wikipedia_link(tmdb_info['title'])

    # Fallback data if TMDB or Wikipedia calls fail
    if not tmdb_info:
        tmdb_info = {
            'title': 'Fallback Movie',
            'tagline': 'No data found - using fallback.',
            'genres': ['Mystery', 'Thriller'],
            'poster_url': 'https://placehold.co/300x450.png?text=No+Image',
        }
        wiki_link = 'https://en.wikipedia.org/wiki/Fallback_Page'
        random_movie_id = 0  # Fallback ID

    # Get all ratings for this movie
    ratings = Rating.query.filter_by(movie_id=random_movie_id).all()
    ratings_data = []
    
    for rating in ratings:
        user = User.query.get(rating.user_id)
        ratings_data.append({
            'id': rating.id,
            'score': rating.score,
            'comment': rating.comment,
            'user_id': rating.user_id,
            'user_username': user.username if user else 'Unknown User',
            'timestamp': rating.timestamp.isoformat() if rating.timestamp else None
        })

    # Get current user's rating if it exists
    user_rating = Rating.query.filter_by(
        user_id=current_user.id, movie_id=random_movie_id
    ).first()
    
    user_rating_data = None
    if user_rating:
        user_rating_data = {
            'id': user_rating.id,
            'score': user_rating.score,
            'comment': user_rating.comment
        }

    return jsonify({
        'movie': {
            'id': random_movie_id,
            'title': tmdb_info['title'],
            'tagline': tmdb_info['tagline'],
            'genres': tmdb_info['genres'],
            'poster_url': tmdb_info['poster_url'],
            'wiki_url': wiki_link
        },
        'ratings': ratings_data,
        'user_rating': user_rating_data
    })

@api.route('/movie/rate', methods=['POST'])
@login_required
def rate_movie():
    data = request.get_json()
    movie_id = data.get('movie_id')
    score = data.get('score')
    comment = data.get('comment')
    movie_title = data.get('movie_title')

    if not movie_id or not score:
        return jsonify({'message': 'Rating information incomplete'}), 400

    try:
        score = int(score)
        if score < 1 or score > 10:
            return jsonify({'message': 'Rating must be between 1 and 10'}), 400
    except ValueError:
        return jsonify({'message': 'Rating must be a number'}), 400

    # Check if user already rated this movie
    existing_rating = Rating.query.filter_by(
        user_id=current_user.id, movie_id=movie_id
    ).first()

    if existing_rating:
        # Update existing rating
        existing_rating.score = score
        existing_rating.comment = comment
    else:
        # Create new rating
        new_rating = Rating(
            score=score,
            comment=comment,
            movie_id=movie_id,
            movie_title=movie_title,
            user_id=current_user.id,
        )
        db.session.add(new_rating)

    db.session.commit()
    return jsonify({'message': 'Rating submitted successfully'})

@api.route('/ratings')
@login_required
def get_user_ratings():
    ratings = Rating.query.filter_by(user_id=current_user.id).all()
    
    ratings_data = []
    for rating in ratings:
        ratings_data.append({
            'id': rating.id,
            'score': rating.score,
            'comment': rating.comment,
            'movie_id': rating.movie_id,
            'movie_title': rating.movie_title,
            'timestamp': rating.timestamp.isoformat() if rating.timestamp else None
        })
    
    return jsonify({'ratings': ratings_data})

@api.route('/ratings/update', methods=['POST'])
@login_required
def update_ratings():
    data = request.get_json()
    updated_ratings = data.get('ratings', [])
    
    # Get all of user's ratings from DB
    user_ratings = Rating.query.filter_by(user_id=current_user.id).all()
    
    # Create map of rating IDs for easy access
    rating_map = {rating.id: rating for rating in user_ratings}
    
    # Get IDs from request
    updated_ids = {rating['id'] for rating in updated_ratings}
    
    # Determine which ratings to delete (ratings that are in DB but not in request)
    for rating in user_ratings:
        if rating.id not in updated_ids:
            db.session.delete(rating)
    
    # Update ratings that are in the request
    for updated_rating in updated_ratings:
        rating_id = updated_rating.get('id')
        if rating_id in rating_map:
            rating = rating_map[rating_id]
            try:
                score = int(updated_rating.get('score'))
                if 1 <= score <= 10:
                    rating.score = score
                rating.comment = updated_rating.get('comment', '')
            except (ValueError, TypeError):
                # Skip invalid scores
                continue
    
    db.session.commit()
    return jsonify({'message': 'Changes saved successfully'})