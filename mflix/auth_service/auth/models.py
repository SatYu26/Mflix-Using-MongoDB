# -*- coding: utf-8 -*-

"""
Authentication-related models module.
"""

from marshmallow import EXCLUDE, fields

from . import ma


class UserSchema(ma.Schema):
    """
    User schema.
    """

    _id = fields.Str(dump_only=True)
    username = fields.Str(required=True)
    email = fields.Email(required=True)
    pw = fields.Str(required=True, load_only=True)

    class Meta:
        unknown = EXCLUDE


user_schema = UserSchema()
