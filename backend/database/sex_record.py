from mongoengine import *
from credentials import username, password


connect(
    db='test',
    username=username,
    password=password,
    host='mongodb://%s:%s@ds121636.mlab.com:21636/amour_auth' % (username, password)
)


class SexRecord(Document):
    meta = {
        'collection': 'sex_records'
    }

    initiator = StringField(max_length=20, required=True, unique=True)
    partner = StringField(max_length=20, required=True, unique=True)
    timestamp = IntField(required=True)

    initiator_signature = StringField(max_length=500, required=True)
    partner_signature = StringField(max_length=500, required=True)
    # something about how contract stores it?

