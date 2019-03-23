from mongoengine import *
from credentials import username, password

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


# if __name__ == "__main__":
#     user = User(login='bobbob', passport_id='ТТ567890', password='uiui',email='bob@example.com', name='Bob', surname='White')
#     user.save()

