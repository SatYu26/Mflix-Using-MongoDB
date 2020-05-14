# -*- coding: utf-8 -*-

"""
This module achieves the same operations as Aggregation Framework pipeline using
PyMongo scripting.

Note that one key difference is that here we are UPDATING the documents
IN-PLACE, where with Aggregation Framework, we are dumping out the result to
another collection
"""

__author__ = 'Ziang Lu'

from datetime import datetime

from pymongo import MongoClient, UpdateOne

from notes.config import CONN_URI

BATCH_SIZE = 1000  # Batch size for batch updating

cli = MongoClient(CONN_URI)
movies = cli.mflix.movies

SINGLE_PLURAL_MAPPING = {
    'genre': 'genres',
    'director': 'directors',
    'cast': 'actors',
    'writer': 'writers',
    'language': 'languages',
    'country': 'countries'
}
RENAMING = {
    'fullplot': 'fullPlot',
    'rating': 'rated'
}
IMDB_RENAMING = {
    'imdbID': 'id',
    'imdbRating': 'rating',
    'imdbVotes': 'votes'
}

batch_updates = []
for movie in movies.find({}):
    # Construct the fields to update (set and unset, respectively)
    fields_to_set = {}
    fields_to_unset = {}

    # Delete all the fields with empty values
    for field, val in movie.copy().items():
        if val in ['', ['']]:
            fields_to_unset[field] = ''
            # Delete the field in the current movie, for the convenience of
            # subsequent processing
            del movie[field]
            # Note that the deletions haven't been sent to the server

    # Split some fields from string literals to arrays
    for single_field, plural_field in SINGLE_PLURAL_MAPPING.items():
        if single_field in movie:
            # Set the new field, and remove the original field
            fields_to_set[plural_field] = movie[single_field].split(', ')
            fields_to_unset[single_field] = ''

    # Rename some fields
    for original_field, new_field in RENAMING.items():
        if original_field in movie:
            # Set the new named field, and remove the original named field
            fields_to_set[new_field] = movie[original_field]
            fields_to_unset[original_field] = ''

    # For some date-related fields, parse out the dates from their string
    # representations
    if 'released' in movie:
        fields_to_set['released'] = datetime.strptime(
            movie['released'], '%Y-%m-%d'
        )
    if 'lastupdated' in movie:
        # Note that we also do a rename here
        fields_to_set['lastUpdated'] = datetime.strptime(
            movie['lastupdated'].split('.')[0], '%Y-%m-%d %H:%M:%S'
        )
        fields_to_unset['lastupdated'] = ''

    # Reshape the IMDB-related fields into one single field (one single embedded
    # document)
    imdb_info = {}
    for original_field, new_field in IMDB_RENAMING.items():
        if original_field in movie:
            imdb_info[new_field] = movie[original_field]
            fields_to_unset[original_field] = ''
    fields_to_set['imdb'] = imdb_info

    update = {}
    if fields_to_set:
        update['$set'] = fields_to_set
    if fields_to_unset:
        update['$unset'] = fields_to_unset

    # Instead of updating one document at a time:
    # movies.update_one({'_id': movie['_id']}, update=update)
    # We will add the current update to a batch of updates, and when the current
    # batch size reaches the batch size limit, at once send the batch updates to
    # the server.
    batch_updates.append(UpdateOne({'_id': movie['_id']}, update=update))
    if len(batch_updates) == BATCH_SIZE:
        movies.bulk_write(batch_updates)
        print(f'Finished updating a batch of {BATCH_SIZE} documents')
        batch_updates = []
# Take care of the last batch of updates
if batch_updates:
    movies.bulk_write(batch_updates)
    print(f'Finished updating a last batch of {len(batch_updates)} documents')

print('Finshed all the updates.')
