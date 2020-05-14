# -*- coding: utf-8 -*-

"""
Movie-related models module.
"""

from marshmallow import EXCLUDE, fields, pre_load

from . import ma


class CommentSchema(ma.Schema):
    """
    Comment schema.
    """

    _id = fields.Str(required=True)
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    text = fields.Str(required=True)
    date = fields.DateTime(required=True)

    @pre_load
    def refactor_input(self, data: dict, **kwargs) -> dict:
        """
        Before deserialization, refactor the input JSON data to match the fields
        defined in this schema.
        :param data: dict
        :param kwargs: dict
        :return: dict
        """
        movie_id = data['movie_id']
        del data['movie_id']
        user = data['user']
        del data['user']

        date = data['date'].fromisoformat()
        data['_id'] = f"{movie_id}-{user['name']}-{date.timestamp()}"
        data['name'] = user['name']
        data['email'] = user['email']
        return data

    class Meta:
        unknown = EXCLUDE


comment_schema = CommentSchema()
comments_schema = CommentSchema(many=True)
