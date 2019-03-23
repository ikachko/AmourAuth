# mongodb://<dbuser>:<dbpassword>@ds121636.mlab.com:21636/amour_auth

from pymongo import MongoClient
from credentials import username, password


client = MongoClient('mongodb://%s:%s@ds121636.mlab.com:21636/amour_auth' % (username, password))

db = client['amour_auth']
collection = db['test_collection']

print(collection)
print(collection.find_one())

