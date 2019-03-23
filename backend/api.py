import json
from flask_restful import Resource, Api, reqparse
from flask import Flask, request

from settings import API_HOST, API_PORT
from routes import Users


app = Flask(__name__)
api = Api(app)

api.add_resource(Users, '/users', methods=['GET'])


if __name__ == '__main__':
    app.run(host=API_HOST, port=API_PORT)
