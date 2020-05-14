# -*- coding: utf-8 -*-

"""
Authentication-related resources module.
"""

from flask import request
from flask_restful import Resource
from marshmallow import ValidationError
from pymongo.errors import DuplicateKeyError

from .. import bcrypt, db
from ..models import user_schema


class UserList(Resource):
    """
    Resource for a collection of users.
    """

    def get(self):
        """
        Returns the user with a specified email.
        :return:
        """
        email = request.args.get('email')
        if not email:
            return {
                'message': 'Email argument not provided'
            }, 400

        user = db.users.find_one({'email': email})
        if not user:
            return {
                'message': 'User not found'
            }, 404

        return {
            'status': 'success',
            'data': user_schema.dump(user)
        }

    def post(self):
        """
        Adds a user with the given name, email and hashed password.
        :return:
        """
        try:
            user_data = user_schema.load(request.json)
        except ValidationError as e:
            return {
                'message': e.messages
            }, 400

        user_data['pw'] = bcrypt.generate_password_hash(user_data['pw'])\
            .decode('utf-8')
        try:
            db.users.insert_one(user_data)
        except DuplicateKeyError:
            return {
                'message': 'A user with the given email already exists'
            }, 400

        return {
            'status': 'success',
            'data': user_schema.dump(user_data)
        }, 201


class UserAuth(Resource):
    """
    Resource for user authentication.
    """

    def get(self):
        """
        Handles user authentication.
        :return:
        """
        email = request.args.get('email')
        if not email:
            return {
                'message': 'Email argument not provided'
            }, 400

        user = db.users.find_one({'email': email})
        if not user:
            return {
                'message': 'Make sure your email is correct'
            }, 404

        if not bcrypt.check_password_hash(user['pw'], request.json['pw']):
            return {
                'message': 'Make sure your password is correct'
            }, 401
        return {
            'status': 'success',
            'data': user_schema.dump(user)
        }
