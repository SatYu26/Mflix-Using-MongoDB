# -*- coding: utf-8 -*-

"""
Flask models module.
"""

import requests
from typing import Optional

from flask_login import UserMixin

from . import AUTH_SERVICE, login_manager


class User(UserMixin):
    """
    Self-defined User class, which represents a user of the application.
    """

    def from_json(self, user_doc: dict):
        """
        Populates this User object from the given user document.
        :param user_doc: dict
        :return: User
        """
        self.id = user_doc['email']
        self.name = user_doc['name']
        self.first_name = user_doc['name'].split(', ')[0]
        self.email = user_doc['email']
        return self

    def to_json(self) -> dict:
        """
        Converts this User object to a user document.
        :return: dict
        """
        return {
            'name': self.name,
            'email': self.email
        }


@login_manager.user_loader
def user_loader(email: str) -> Optional[User]:
    """
    Flask-Login user loader for reloading the logged-in user from the session.
    :param email: str
    :return: User or None
    """
    user_doc = _get_user(email)
    if user_doc:
        return User().from_json(user_doc)


def _get_user(email: str) -> Optional[dict]:
    """
    Private helper function to return the user with the given email.
    :param email: str
    :return: dict or None
    """
    r = requests.get(f'{AUTH_SERVICE}/users/?email={email}')
    if r.status_code == 200:
        return r.json()['data']
