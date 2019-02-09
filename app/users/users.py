import json
from flask import request, Blueprint, abort, current_app
from flask_restful import Api, Resource, reqparse, fields, marshal, marshal_with
from .usersDao import UsersDAO
from app.auth.auth import Auth

bp = Blueprint('users', __name__, url_prefix='/user/v1')
user_api = Api(bp)

user_fields = {
    'uid': fields.String,
    'email': fields.String,
    'uri': fields.Url('users.users')
}

auth = Auth()


class User(Resource):
    decorators = [auth.identify(resource=UsersDAO)]

    def __init__(self):
        self.db = UsersDAO()
        self.reqparse = reqparse.RequestParser()

    @marshal_with(user_fields)
    def get(self, uid):
        query = {'uid': uid}
        data = self.db.findOne(query)
        if data:
            return data
        abort(404)

    def put(self, uid):
        self.reqparse.add_argument(
            'pwd', type=str, required=True, help="is required", location='json')
        self.reqparse.add_argument(
            'email', type=str, required=True, help="is required", location='json')
        query = {"uid": uid}
        update = self.reqparse.parse_args()
        result = self.db.update(query, update)
        if result['n']:
            return {'update': uid}, 202
        return abort(404)

    def delete(self, uid):
        query = {'uid': uid}
        result = self.db.remove(query)
        if result['n']:
            return {'deleted': uid}, 202
        return abort(404)


user_api.add_resource(User, '/<string:uid>', endpoint = 'users')
