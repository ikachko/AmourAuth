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
        print(users)
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


api.add_resource(Users, '/users', methods=['GET', 'POST'])


if __name__ == '__main__':
    app.run(host=API_HOST, port=API_PORT)
