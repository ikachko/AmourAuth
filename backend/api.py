import json
from flask_restful import Resource, Api, reqparse
from flask import Flask, Response
from settings import API_HOST, API_PORT
from pymongo import MongoClient
from credentials import username, password


app = Flask(__name__)
api = Api(app)


client = MongoClient('mongodb://%s:%s@ds121636.mlab.com:21636/amour_auth' % (username, password))
db = client['amour_auth']


class Users(Resource):
    def get(self):
        return Response(
            response='',
            status=200,
            mimetype='application/json'
)


api.add_resource(Users, '/users', methods=['GET'])


if __name__ == '__main__':
    app.run(host=API_HOST, port=API_PORT)
