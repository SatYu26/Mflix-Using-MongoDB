from pymongo import MongoClient # this lets us connect to MongoDB
import pymongo
import pprint
from IPython.display import clear_output

client = MongoClient("mongodb+srv://analytics:analytics-password@mflix-tjjkj.mongodb.net/test?retryWrites=true&w=majority")

"""pipeline = [
    {
        '$group': {
            '_id':{'language':'$language'},
            'count':{'$sum':1}
            }
    },
        {
        '$sort':{'count':-1} #-1 sort in descending order else 1 #sorted on count
            }
            ]
            """

"""
pipeline = [
    {
        '$match': {'language':'Korean','English'}
        }
        ]
"""
#gives most frequent used combination of lanuages
pipeline = [
    {
        '$sortByCount': '$language'

            },
    {
        '$facet':{
            'top language combinations': [{'$limit':100}],
            'unusual combination shared by':[{
                '$skip':100
            },
                {
                    '$bucketAuto':{
                        'groupBy':"$count",
                        'buckets':5,
                        'output':{
                            'language combinations':{'$sum':1}
                        }
                    }
                }
            ]
        }
    }


]
clear_output()
pprint.pprint(list(client.mflix.movies_initial.aggregate(pipeline)))