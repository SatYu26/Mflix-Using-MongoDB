# -*- coding: utf-8 -*-

"""
MongoDB Aggregation Framework demo1.

$match stage demo
"""

__author__ = 'Ziang Lu'

import pprint

from pymongo import MongoClient

from notes.config import CONN_URI

cli = MongoClient(CONN_URI)
movies_initial = cli.mflix.movies_initial

pipeline = [
    {
        '$match': {'language': 'Mandarin, English'}
    }  # stage1: 'match' stage
]
# Note that we can totally use movies_initial.find() method to filter, since
# this is a very simply case where we only have one stage in the pipeline

for result in movies_initial.aggregate(pipeline):
    pprint.pprint(result)
