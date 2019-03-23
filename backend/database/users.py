from mongoengine import *
from credentials import username, password, secret_key
import datetime
import jwt

# connect('mongodb://%s:%s@ds121636.mlab.com:21636/amour_auth' % (username, password))

connect(
    db='test',
    username='user',
    password='12345',
    host='mongodb://%s:%s@ds121636.mlab.com:21636/amour_auth' % (username, password)
)


class User(Document):
    meta = {
        'collection': 'users'
    }

    login = StringField(max_length=20, unique=True, required=True)
    passport_id = StringField(min_length=8, max_length=8, unique=True, required=True)
    email = EmailField(unique=True)
    password = StringField(max_length=500, required=True)
    name = StringField(max_length=200, required=True)
    surname = StringField(max_length=200, required=True)

    @staticmethod
    def encode_auth_token(login):
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
                'iat': datetime.datetime.utcnow(),
                'sub': login
            }
            return jwt.encode(
                payload,
                secret_key,
                algorithm='HS256'
            )
        except Exception as e:
            return e


# if __name__ == "__main__":
#     user = User(login='bobbob', passport_id='ТТ567890', password='uiui',email='bob@example.com', name='Bob', surname='White')
#     user.save()

