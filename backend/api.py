import codecs
import json
from flask_restful import Resource, Api, reqparse, request
from flask import Flask, Response
from settings import API_HOST, API_PORT
from pymongo import MongoClient
from credentials import username, password

from database.users import User

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
                password=user_data['password'],
                email=user_data['email'],
                name=user_data['name'],
                surname=user_data['surname'])
            user.save()
        except Exception as e:
            return Response(
                response=json.dumps({'error': e}),
                status=400,
                mimetype='application/json'
            )

        return Response(
            response=json.dumps({'created': True}),
            status=200,
            mimetype='application/json'
        )


class Login(Resource):
    """
    User Login Resource
    """
    def post(self):
        # get the post data
        user_data = json.loads(codecs.decode(request.data))

        try:
            print(user_data)
            user = json.loads(User.objects(login=user_data['login']).to_json())[0]

            print(user)
            if not user:
                raise Exception('No such user')
            if user['password'] != user_data['password']:
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
                response=json.dumps({'error': 'e'}),
                status=400,
                mimetype='application/json'
            )


api.add_resource(Users, '/users', methods=['GET', 'POST'])
api.add_resource(Login, '/login', methods=['POST'])


if __name__ == '__main__':
    app.run(host=API_HOST, port=API_PORT)
