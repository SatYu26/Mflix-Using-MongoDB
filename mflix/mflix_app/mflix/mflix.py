# -*- coding: utf-8 -*-

"""
Flask application module.
"""

import requests
from datetime import datetime
from typing import Optional
from urllib.parse import urlencode

import bson.json_util
import flask_login
from flask import redirect, render_template, request, url_for
from flask_login import current_user

from . import MOVIE_SERVICE, app


@app.route('/')
def show_movies():
    """
    Mflix application home page.
    :return:
    """
    movies_per_page = 20

    filters = {}
    genre = request.args.get('genre')
    if genre:
        filters['genres'] = genre
    search = request.args.get('search')
    if search:
        filters['$text'] = {'$search': search}

    # For pagination
    page = request.args.get('page', type=int, default=0)

    args_copy = request.args.copy()
    args_copy['page'] = page - 1
    prev_page = urlencode(args_copy)
    args_copy['page'] = page + 1
    next_page = urlencode(args_copy)

    request_url = f'{MOVIE_SERVICE}/movies'
    if request.args:
        request_url += f'?{urlencode(request.args)}'

    r = requests.get(request_url, json=filters)
    json_data = r.json()['data']
    page_movies = bson.json_util.loads(json_data['page_movies'])  # A BSON document is serialized to a string, so we need to deserialize it back to a BSON document.
    total_num_of_movies = json_data['total_num_of_movies']

    r = requests.get(f'{MOVIE_SERVICE}/movie-genres')
    all_genres = r.json()['data']

    context = {
        'total_num_of_entries': total_num_of_movies,
        'entries_per_page': movies_per_page,
        'page': page,
        'filters': filters,
        'movies': page_movies,
        'prev_page': prev_page,
        'next_page': next_page,
        'all_genres': all_genres
    }
    return render_template('movies.html', **context)


@app.route('/movies/<id>', methods=['GET', 'POST'])
@flask_login.login_required
def show_movie(id: str):
    """
    Movie detail page.
    :param id: str
    :return:
    """
    context = {
        'movie': _get_movie(id)
    }
    if request.method == 'POST':
        context['new_comment'] = request.form['comment']
    return render_template('movie.html', **context)


def _get_movie(id: str) -> Optional[dict]:
    """
    Private helper function to get the movie with the given ID.
    :param id:
    :return: dict or None
    """
    r = requests.get(f'{MOVIE_SERVICE}/movies/{id}')
    if r.status_code == 200:
        return bson.json_util.loads(r.json()['data'])
    else:
        return None


@app.route('/movies/<id>/comments', methods=['GET', 'POST'])
@flask_login.login_required
def show_movie_comments(id: str):
    """
    Movie comments page.
    :param id: str
    :return:
    """
    if request.method == 'POST':
        comment = request.form['comment']
        requests.post(
            f'{MOVIE_SERVICE}/movies/{id}/comments',
            json={
                'movie_id': id,
                'user': current_user.to_json(),
                'text': comment,
                'date': datetime.now().isoformat()
            }
        )
        return redirect(url_for('show_movie', id=id))

    r = requests.get(f'{MOVIE_SERVICE}/movie/{id}/comments')
    if r.status_code == 200:
        comments = r.json()['data']
    else:
        comments = []

    context = {
        'movie': _get_movie(id),
        'comments': comments
    }
    return render_template('movie_comments.html', **context)


@app.route('/movies/<movie_id>/comments/<comment_id>/delete', methods=['POST'])
@flask_login.login_required
def delete_movie_comment(movie_id: str, comment_id: str):
    """
    Movie deletion page.
    :param movie_id: str
    :param comment_id: str
    :return:
    """
    requests.delete(
        f'{MOVIE_SERVICE}/movies/{movie_id}/comments/{comment_id}'
    )
    return redirect(url_for('show_movie', id=id))


@app.route('/movies/watch/<id>')
@flask_login.login_required
def watch_movie(id: str):
    """
    Movie watch page.
    :param id: str
    :return:
    """
    context = {
        'movie': _get_movie(id)
    }
    return render_template('watch_movie.html', **context)
