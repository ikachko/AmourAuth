import codecs
import time
import json
from flask_restful import Resource, Api, reqparse, request
from flask import Flask, Response
from settings import API_HOST, API_PORT
from pymongo import MongoClient
from credentials import username, password

from database.users import User
from database.locations import OnlineTime

app = Flask(__name__)
api = Api(app)


class Users(Resource):
    def get(self):
        users = User.objects()
        return Response(
            response=users.to_json(),
            status=200,
            mimetype='application/json'
        )

    def post(self):
        user_data = json.loads(codecs.decode(request.data))
        try:
            user = User(
                login=user_data['login'],
                passport_id=user_data['passport_id'],
                password=User.hash_password(user_data['password']),
                email=user_data['email'],
                name=user_data['name'],
                surname=user_data['surname'],
                passport_pic_url=user_data['passport_pic_url']
            )

            user.save()
        except Exception as e:
            return Response(
                response=json.dumps({'error': str(e)}),
                status=400,
                mimetype='application/json'
            )

        return Response(
            response=json.dumps({'created': True}),
            status=200,
            mimetype='application/json'
        )


class Login(Resource):
    def post(self):
        # get the post data
        user_data = json.loads(codecs.decode(request.data))

        try:
            print(user_data)
            user = json.loads(User.objects(login=user_data['login']).to_json())[0]

            if not user:
                raise Exception('No such user')
            if user['password'] != User.hash_password(user_data['password']):
                raise Exception('Wrong password')
            auth_token = User.encode_auth_token(user['login'])
            if auth_token:
                return Response(
                    response=json.dumps(
                        {
                            'status': 'success',
                            'message': 'Successfully logged in.',
                            'auth_token': auth_token.decode()
                        }
                    ),
                    status=200,
                    mimetype='application/json'
                )
        except Exception as e:
            print(e)
            return Response(
                response=json.dumps({'error': str(e)}),
                status=400,
                mimetype='application/json'
            )


def get_login_from_jwt(request):
    auth_header = request.headers.get('Authorization')
    if auth_header:
        auth_token = auth_header.split(" ")[1]
    else:
        auth_token = ''
    return User.decode_auth_token(auth_token)


class Self(Resource):
    def get(self):
        try:
            resp = get_login_from_jwt(request)
            user = User.objects(login=resp)
            if not user:
                raise Exception("No such user")
            responseObj = user.to_json()

            return Response(
                response=responseObj,
                status=200,
                mimetype='application/json'
            )
        except Exception as e:
            print(e)
            return Response(
                response=json.dumps({'error': str(e)}),
                status=400,
                mimetype='application/json'
            )


class Online(Resource):
    def get(self):
        try:
            resp = get_login_from_jwt(request)
            user = User.objects(login=resp)
            if not user:
                raise Exception("No such user")

            users = OnlineTime.objects.filter(timestamp__gte=time.time() - 120).filter(login__ne=resp)
            responseObj = users.to_json()

            if len(OnlineTime.objects(login=resp)) != 0:
                OnlineTime.objects(login=resp).update_one(set__timestamp=time.time())
            else:
                online = OnlineTime(
                    login=resp,
                    timestamp=time.time(),
                )
                online.save()

            return Response(
                response=responseObj,
                status=200,
                mimetype='application/json'
            )
        except Exception as e:
            print(e)
            return Response(
                response=json.dumps({'error': str(e)}),
                status=400,
                mimetype='application/json'
            )


api.add_resource(Users, '/users', methods=['GET', 'POST'])
api.add_resource(Login, '/login', methods=['POST'])
api.add_resource(Self, '/self', methods=['GET'])
api.add_resource(Online, '/online', methods=['GET'])


if __name__ == '__main__':
    app.run(host=API_HOST, port=API_PORT)

# alise
# Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1NTM0NzA3NjYsImlhdCI6MTU1MzM4NDM2Niwic3ViIjoiYWxpc2UifQ.UBKPTaFXE8sdEdc5LJE1pd7X6Udjh2P5stTyJGIPaDg

# bob
# Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1NTM0NzA3OTksImlhdCI6MTU1MzM4NDM5OSwic3ViIjoiYm9iIn0.b5T52P5SEJSf-kBT6nT_OGb9CffWJNQlZ2O6qTi9ya4