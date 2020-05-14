# -*- coding: utf-8 -*-

"""
MongoDB Aggregation Framework demo5.

$cond and $addFields stages demo
"""

__author__ = 'Ziang Lu'

from pymongo import MongoClient

from notes.config import CONN_URI

cli = MongoClient(CONN_URI)
movies_initial = cli.mflix.movies_initial

pipeline = [
    {
        '$limit': 100
    },  # stage1: 'limit' stage
    # $addFields stage adds new fields.
    # Since "lastupdated" field contains too many trailing 0s in the string
    # representation of the timestamp, we need to trim them off, to be able to
    # parse out a date from it.
    {
        '$addFields': {
            'lastupdated': {
                '$arrayElemAt': [  # Take the element at the given index in the given array
                    {'$split': ['$lastupdated', '.']},
                    0
                ]
            }  # Note that since "lastupdated" field already exists, its value will be replaced
        }
    },  # stage2: 'addFields' stage
    {
        '$project': {
            'title': 1,
            'poster': 1,
            'genres': {'$split': ['$genre', ', ']},
            'plot': 1,
            'fullPlot': '$fullplot',
            'directors': {'$split': ['$director', ', ']},
            'actors': {'$split': ['$cast', ',']},
            'writers': {'$split': ['$writer', ',']},
            'year': 1,
            'released': {  # Reshape "released" field based on some condition
                '$cond': {
                    'if': {'$ne': ['$released', '']},
                    'then': {
                        '$dateFromString': {
                            'dateString': '$released'
                        }
                    },
                    'else': ''
                }  # Conditional expression
            },
            'languages': {'$split': ['$language', ',']},
            'countries': {'$split': ['$country', ',']},
            'runtime': 1,
            'imdb': {
                'id': '$imdbID',
                'rating': '$imdbRating',
                'votes': '$imdbVotes'
            },
            'rated': '$rating',
            'awards': 1,
            'lastUpdated': {  # Reshape "lastupdated" field based on some condition
                '$cond': {
                    'if': {'$ne': ['$lastupdated', '']},
                    'then': {
                        '$dateFromString': {
                            'dateString': '$lastupdated',
                            'timezone': 'America/New_York'
                        }
                    },
                    'else': ''
                }
            }
        }
    },  # stage3: 'project' stage
    {
        '$out': 'movies_processed'
    }  # stage4: 'out' stage
]

movies_initial.aggregate(pipeline)
