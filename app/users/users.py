import json
from flask import jsonify, request, Blueprint, abort, make_response
from flask_restful import Api, Resource, reqparse, fields, marshal, marshal_with
from .usersDao import UsersDAO
# from app.auth import Auth

bp = Blueprint('users', __name__, url_prefix='/user/v1')
user_api = Api(bp)

user_fields = {
    'uid': fields.String,
    'email': fields.String,
    'uri': fields.Url('users.user')
}

class User(Resource):
    def __init__(self):
        self.db = UsersDAO()
        self.reqparse = reqparse.RequestParser()

    @marshal_with(user_fields)
    def get(self, uid):
        query = {'uid': uid}
        data = self.db.findOne(query)
        if data != 'null':
            return json.loads(data)
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
            return make_response(jsonify({'update': uid}), 202)
        return abort(404)

    def delete(self, uid):
        query = {'uid': uid}
        result = self.db.remove(query)
        if result['n']:
            return make_response(jsonify({'deleted': uid}), 202)
        return abort(404)


user_api.add_resource(User, '/<string:uid>', endpoint='user')
