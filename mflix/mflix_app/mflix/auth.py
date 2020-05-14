# -*- coding: utf-8 -*-

"""
Authentication module.
"""

import flask_login
import requests
from flask import redirect, render_template, request, url_for

from . import AUTH_SERVICE, app, login_manager
from .models import User


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """
    Sign-up page.
    :return:
    """
    if request.method == 'GET':
        return render_template('login.html')

    name = request.form['name']
    email = request.form['email']
    pw = request.form['password']

    if len(pw) < 8:
        return render_template(
            'login.html', signuperror='Password must be at least 8 characters.'
        )
    elif pw != request.form['confirm-password']:
        return render_template(
            'login.html', signuperror='Make sure to confirm the password!'
        )

    r = requests.post(
        f'{AUTH_SERVICE}/users',
        json={
            'name': name,
            'email': email,
            'pw': pw
        }
    )
    if r.status_code != 201:
        return render_template('login.html', signuperror=r.json()['message'])

    new_user_doc = r.json()['data']
    new_user_obj = User().from_json(new_user_doc)
    flask_login.login_user(new_user_obj)
    return redirect(url_for('show_movies'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Log-in page.
    :return:
    """
    if request.method == 'GET':
        return render_template('login.html')

    email = request.form['email']
    pw = request.form['password']

    r = requests.get(
        f'{AUTH_SERVICE}/user-auth/?email={email}', json={'pw': pw}
    )
    if r.status_code != 200:
        return render_template('login.html', loginerror=r.json()['message'])

    user_doc = r.json()['data']
    user_obj = User().from_json(user_doc)
    flask_login.login_user(user_obj)
    return redirect(url_for('show_movies'))


@app.route('/profile')
@flask_login.login_required
def profile():
    """
    Profile page.
    :return:
    """
    return render_template('profile.html')


@app.route('/logout')
@flask_login.login_required
def logout():
    """
    Logout page.
    :return:
    """
    flask_login.logout_user()
    return redirect(url_for('show_movies'))


@login_manager.unauthorized_handler
def unauthorized_handler():
    """
    Flask-Login unauthorized handler.
    When "login_required", this function handles unauthorized users, and
    redirect them to appropriate place.
    :return:
    """
    return render_template('splash_screen.html')
