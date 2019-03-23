from flask import Response
from flask_restful import Resource


class Users(Resource):
    def get(self):
        return Response(
            response='',
            status=200,
            mimetype='application/json'
)
