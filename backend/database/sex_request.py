import time

from mongoengine import *
from credentials import username, password


connect(
    db='test',
    username=username,
    password=password,
    host='mongodb://%s:%s@ds121636.mlab.com:21636/amour_auth' % (username, password)
)


class SexRequest(Document):
    meta = {
        'collection': 'sex_request'
    }

    initiator = StringField(max_length=20, required=True)
    partner = StringField(max_length=20, required=True)
    timestamp = IntField(required=True, default=time.time())
    confirmed = BooleanField(required=True, default=False)
    pending = BooleanField(required=True, default=True)

    initiator_signature = StringField(max_length=500)
    partner_signature = StringField(max_length=500)
    contract_record_id = StringField(max_length=100)
