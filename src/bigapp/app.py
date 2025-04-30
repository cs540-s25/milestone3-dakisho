import random

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from .models import db, Rating
from .tmdb import fetch_movie_data
from .wiki import fetch_wikipedia_link

main = Blueprint('main', __name__)

MOVIE_IDS = [
    550,  # Fight Club
    300668,
    329865,
    335984,
    157336,
    675353,
]


@main.route('/')
@login_required
def index():
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

    # Get ratings for this movie
    ratings = Rating.query.filter_by(movie_id=random_movie_id).all()

    return render_template(
        'index.html',
        movie_id=random_movie_id,
        movie_title=tmdb_info['title'],
        movie_tagline=tmdb_info['tagline'],
        movie_genres=', '.join(tmdb_info['genres']),
        poster_url=tmdb_info['poster_url'],
        wiki_url=wiki_link,
        ratings=ratings,
    )


@main.route('/rate', methods=['POST'])
@login_required
def rate_movie():
    movie_id = int(request.form.get('movie_id'))
    score = request.form.get('score')
    comment = request.form.get('comment')
    movie_title = request.form.get('movie_title')

    if not movie_id or not score:
        flash('Rating information incomplete')
        return redirect(url_for('main.index'))

    try:
        score = int(score)
        if score < 1 or score > 10:
            flash('Rating must be between 1 and 10')
            return redirect(url_for('main.index'))
    except ValueError:
        flash('Rating must be a number')
        return redirect(url_for('main.index'))

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
    return redirect(url_for('main.index'))
