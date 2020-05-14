import os

from flask import Flask
from flask_marshmallow import Marshmallow
from flask_restful import Api
from pymongo import MongoClient

USER = os.environ['USER']
PASSWORD = os.environ['PASSWORD']
DB_NAME = 'mflix'
MFLIX_DB_URI = f"mongodb+srv://{USER}:{PASSWORD}@cluster0-hanbs.mongodb.net/{DB_NAME}?retryWrites=true&w=majority"

try:
    db = MongoClient(MFLIX_DB_URI)[DB_NAME]
except KeyError:
    raise Exception("You haven't configured your MFLIX_DB_URI!")

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['FLASK_SECRET_KEY']

ma = Marshmallow(app)

api = Api(app)

from .resources.comment import MovieComment, MovieComments
from .resources.movie import MovieGenreList, MovieItem, MovieList

api.add_resource(MovieList, '/movies')
api.add_resource(MovieItem, '/movie/<id>')
api.add_resource(MovieComments, '/movie/<id>/comments')
api.add_resource(MovieComment, '/movie/<movie_id>/comments/<comment_id>')
api.add_resource(MovieGenreList, '/movie-genres')
