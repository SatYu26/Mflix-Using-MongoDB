# -*- coding: utf-8 -*-

"""
Module containing MongoDB Atlas configurations.
"""

from urllib.parse import quote_plus

USER = quote_plus('zianglu')
PASSWORD = quote_plus('Zest2016!')
DB = 'mflix'

CONN_URI = f'mongodb+srv://{USER}:{PASSWORD}@cluster0-hanbs.mongodb.net/{DB}?authSource=admin&readPreference=primary&ssl=true'
