import codecs
import hashlib

from mongoengine import *
from credentials import username, password, secret_key


connect(
    db='test',
    username=username,
    password=password,
    host='mongodb://%s:%s@ds121636.mlab.com:21636/amour_auth' % (username, password)
)


class User(Document):
    meta = {
        'collection': 'locations'
    }

