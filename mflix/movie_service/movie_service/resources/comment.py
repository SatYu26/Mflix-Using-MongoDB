# -*- coding: utf-8 -*-

"""
Comment-related resources module.
"""

from bson.errors import InvalidId
from bson.objectid import ObjectId
from flask import request
from flask_restful import Resource
from marshmallow import ValidationError
from pymongo import DESCENDING

from .. import db
from ..models import comment_schema, comments_schema

MOVIE_COMMENT_CACHE_LIMIT = 10


class MovieComments(Resource):
    """
    Resource for a collection of movie comments.
    """

    def get(self, id: str):
        """
        Returns the comments of the given movie, from most-recent to
        least-recent.
        :param id: str
        :return:
        """
        try:
            comments = db.comments.find({'movie_id': ObjectId(id)})\
                .sort('date', direction=DESCENDING)
        except InvalidId:
            return {
                'message': 'Invalid movie ID'
            }, 400

        return {
            'status': 'success',
            'data': comments_schema.dump(comments)
        }

    def post(self, id: str):
        """
        Adds a comment to the given movie.
        :param id: str
        :return:
        """
        try:
            movie_id = ObjectId(id)
            movie = db.movies.find_one({'_id': movie_id})
        except InvalidId:
            return {
                'message': 'Invalid movie ID'
            }, 400
        if not movie:
            return {
                'message': 'Movie not found',
            }, 404

        try:
            new_comment = comment_schema.load(request.json)
        except ValidationError as e:
            return {
                'message': e.messages
            }, 400

        # 1. Add a new comment to "comments" collection
        new_comment['movie_id'] = movie_id
        db.comments.insert_one(new_comment)
        # 2. At the same time, update the corresponding movie in "movies"
        #    collection
        movie_update = {
            # 2.1 Increment the comment count on the movie
            '$inc': {
                'num_mflix_comments': 1
            },
            # 2.2 Update the cached comments on the movie
            '$push': {
                'comments': {
                    '$each': [new_comment],
                    '$sort': {'date': -1},
                    '$slice': MOVIE_COMMENT_CACHE_LIMIT
                }
            }
        }
        db.movies.update_one({'_id': movie_id}, update=movie_update)
        return {
            'status': 'success',
            'data': new_comment
        }, 201


class MovieComment(Resource):
    """
    Resource for a single movie comment.
    """

    def delete(self, movie_id: str, comment_id: str):
        """
        Deletes the given comment from the given movie.
        :param movie_id: str
        :param comment_id: str
        :return:
        """
        # 1. Delete the comment from "comments" collection
        comment_id = ObjectId(comment_id)
        db.comments.delete_one({'_id': comment_id})

        # 2. At the same time, update the corresponding movie in "movies"
        #    collection

        # 2.1 Decrement the comment count on the movie
        movie_id = ObjectId(movie_id)
        movie_update = {
            '$inc': {
                'num_mflix_comments': -1
            }
        }
        db.movies.update_one({'_id': movie_id}, update=movie_update)

        # Check whether the comment is cached on the movie
        movie = db.movies.find_one({'comments._id': comment_id})
        if movie:
            # 2.2 If so, update the cached comments on the movie
            updated_comments = db.comments.find({'movie_id': movie_id}) \
                .sort('date', direction=DESCENDING)\
                .limit(MOVIE_COMMENT_CACHE_LIMIT)
            movie_update = {
                '$set': {
                    'comments': list(updated_comments)
                }
            }
            db.movies.update_one({'_id': movie_id}, update=movie_update)

        return '', 204
