#!/bin/bash

source ./env.sh

mongorestore --gzip --uri "$MFLIX_DB_URI" data/dump
