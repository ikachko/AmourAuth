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


class OnlineTime(Document):
    meta = {
        'collection': 'online_time'
    }

    login = StringField(max_length=20, required=True, unique=True)
    timestamp = IntField(required=True)

