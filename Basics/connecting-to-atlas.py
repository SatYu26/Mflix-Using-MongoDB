
# coding: utf-8

# In[ ]:


from pymongo import MongoClient # this lets us connect to MongoDB
import pprint # this lets us print our MongoDB documents nicely


# In[ ]:


# the connection uri to our course cluster
client = MongoClient('mongodb+srv://analytics:analytics-password@mflix-tjjkj.mongodb.net/test?retryWrites=true&w=majority')


# In[ ]:


# the trips collection on the citibike database
trips = client.citibike.trips


# In[ ]:


# find all trips between 5 and 10 minutes in duration that start at station 216
query = {"tripduration":{"$gte":5000,"$lt":10000},"start station id":216}

# only return the bikeid, tripduration, and _id (displayed by default)
projection = {"bikeid": 1, "tripduration": 1}


# In[ ]:


# print all of the trips
for doc in trips.find(query, projection):
    pprint.pprint(doc)

