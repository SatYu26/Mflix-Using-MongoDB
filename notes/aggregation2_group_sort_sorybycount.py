# -*- coding: utf-8 -*-

"""
MongoDB Aggregation Framework demo2.

$group, $sort and $sortByCount stages demo
"""

__author__ = 'Ziang Lu'

import pprint

from pymongo import MongoClient

from notes.config import CONN_URI

cli = MongoClient(CONN_URI)
movies_initial = cli.mflix.movies_initial

# Equivalence in SQL:
# select language, count(*) as count
# from movies_initial
# group by language
# order by count;

# pipeline = [
#     {
#         '$group': {
#             '_id': {'language': '$language'},  # Identifier expression to group by
#             'count': {'$sum': 1}  # Accumulator to apply aggregation
#         }
#     },  # stage1: 'group' stage
#     {
#         '$sort': {'count': -1}
#     }  # stage2: 'sort' stage
# ]

# The above stages can be combined into one single stage:
pipeline = [
    {
        '$sortByCount': '$language'
    }  # stage1: 'sortByCount' stage
]

for result in movies_initial.aggregate(pipeline):
    pprint.pprint(result)
