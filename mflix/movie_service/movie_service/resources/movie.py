# -*- coding: utf-8 -*-

"""
Movie-related resources module.
"""

from datetime import datetime

import bson.json_util
from bson.errors import InvalidId
from bson.objectid import ObjectId
from flask import request
from flask_restful import Resource
from pymongo import DESCENDING

from .. import db


class MovieList(Resource):
    """
    Resource for a collection of movies.
    """

    def get(self):
        """
        Returns all the movies in the specified page.
        :return:
        """
        filters = request.get_json()
        if filters is None:
            filters = {}

        page = request.args.get('page', type=int, default=0)
        per_page = request.args.get('per_page', type=int, default=10)

        if '$text' in filters:
            # TODO: Figure this out
            score_meta_doc = {'$meta': 'textScore'}
            movies = db.movies\
                .find(filters, projection={'score': score_meta_doc})\
                .sort([('score', score_meta_doc)])
        else:
            movies = db.movies.find(filters)\
                .sort('tomatoes.viewers.numReviews', direction=DESCENDING)

        total_num_of_movies = movies.count()

        # Only return the movie list on the given page
        page_movies = list(movies.skip(page * per_page).limit(per_page))
        return {
            'status': 'success',
            'data': {
                'page_movies': bson.json_util.dumps(page_movies),  # In order to serialize a BSON document, we need to first encode it to a string.
                'total_num_of_movies': total_num_of_movies
            }
        }


class MovieItem(Resource):
    """
    Resource for a single movie.
    """

    def get(self, id: str):
        """
        Returns the movie with the given ID.
        :param id: str
        :return:
        """
        try:
            movie = db.movies.find_one({'_id': ObjectId(id)})
        except InvalidId:
            return {
                'message': 'Invalid movie ID'
            }, 400
        if not movie:
            return {
                'message': 'Movie not found',
            }, 404

        return {
            'status': 'success',
            'data': bson.json_util.dumps(movie)
        }


class MovieGenreList(Resource):
    """
    Resource for a collection of movie genres.
    """

    def get(self):
        """
        Returns all the movie genres.
        :return:
        """
        pipeline = [
            {
                '$unwind': '$genres'
            },
            {
                '$project': {
                    '_id': 0,
                    'genres': 1
                }
            },
            # TODO: Figure out this "group"
            {
                '$group': {
                    '_id': None,
                    'genres': {
                        '$addToSet': '$genres'
                    }
                }
            }
        ]
        # After the pipeline, there is only one document, containing only one
        # field "genres", which is array containing all the different genres.
        return {
            'status': 'success',
            'data': list(db.movies.aggregate(pipeline))[0]['genres']
        }
