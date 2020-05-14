# -*- coding: utf-8 -*-

"""
MongoDB Aggregation Framework demo4.

$project stage demo
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
    # $project stage can be used to do data transformation, e.g., cleaning up
    # the raw (messy) data, and maybe reshaping the data to what we desire.
    {
        '$project': {
            'title': 1,  # Keep it as it is
            'poster': 1,
            'genres': {'$split': ['$genre', ', ']},  # Split the "genre" field from a string literal to an array
            'plot': 1,
            'fullPlot': '$fullplot',  # Effectively renaming operation
            'directors': {'$split': ['$director', ', ']},
            'actors': {'$split': ['$cast', ', ']},
            'writers': {'$split': ['$writer', ', ']},
            'year': 1,
            'released': 1,
            'languages': {'$split': ['$language', ', ']},
            'countries': {'$split': ['$country', ', ']},
            'runtime': 1,
            'imdb': {
                'id': '$imdbID',
                'rating': '$imdbRating',
                'votes': '$imdbVotes'
            },  # Reshape some fields into one single field (one single embedded document)
            'rated': '$rating',
            'awards': 1,
            'lastUpdated': '$lastupdated'
        }
    },  # stage2: 'project' stage
    {
        '$out': 'movies_processed'
    }  # stage3: 'out' stage
]

# Since we already dump out the result to "movies_processed" collection, we can
# simply execute the pipeline and no longer need to iterate over the results.
movies_initial.aggregate(pipeline)
