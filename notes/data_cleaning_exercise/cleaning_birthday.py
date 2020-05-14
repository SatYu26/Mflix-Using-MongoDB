# -*- coding: utf-8 -*-

"""
This module converts any string value for "birthday" field to BSON dates.
"""

__author__ = 'Ziang Lu'

import dateparser
from pymongo import MongoClient, UpdateOne

from notes.config import CONN_URI

BATCH_SIZE = 1000  # Batch size for batch updating

cli = MongoClient(CONN_URI)
people_raw = cli.cleansing['people-raw']

batch_updates = []
for person in people_raw.find({'birthday': {'$type': 'string'}}):
    update = {'$set': {'birthday': dateparser.parse(person['birthday'])}}
    # Instead of updating one document at a time, we will add the current update
    # to a batch of updates, and when the current batch size reaches the batch
    # size limit, send the batch updates to the server at once.
    batch_updates.append(UpdateOne({'_id': person['_id']}, update=update))
    if len(batch_updates) == BATCH_SIZE:
        people_raw.bulk_write(batch_updates)
        print(f'Finished updating a batch of {BATCH_SIZE} documents')
        batch_updates = []
# Take care of the last batch of updates
if batch_updates:
    people_raw.bulk_write(batch_updates)
    print(f'Finished updating a last batch of {len(batch_updates)} documents')

print('Finshed all the updates.')
