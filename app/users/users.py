import json
from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify, request, Blueprint, abort, make_response
from flask_restful import Api, Resource, reqparse, fields, marshal, marshal_with
from .model import UsersDAO
# from app.auth import Auth

bp = Blueprint('users', __name__)
user_api = Api(bp)

user_fields = {
    'uid': fields.String,
    'email': fields.String,
    'uri': fields.Url('users.user')
}


def set_password(self, password):
    return generate_password_hash(password)


def check_password(self, hash, password):
    return check_password_hash(hash, password)

# @bp.route('/register', methods=['POST'])
# def register():
#     """
#     用户注册
#     :return: json
#     """
#     email = request.form.get('email')
#     username = request.form.get('username')
#     password = request.form.get('password')
#     user = UsersDAO(email=email, username=username,
#                  password=UsersDAO.set_password(UsersDAO, password))
#     result = UsersDAO.add(Users, user)
#     if user.id:
#         returnUser = {
#             'id': user.id,
#             'username': user.username,
#             'email': user.email,
#             'login_time': user.login_time
#         }


# @bp.route('/login', methods=['POST'])
# def login():
#     """
#     用户登录
#     :return: json
#     """
#     username = request.form.get('username')
#     password = request.form.get('password')
#     if (not username or not password):
#         return jsonify(common.falseReturn('', '用户名和密码不能为空'))
#     else:
#         return Auth.authenticate(Auth, username, password)


class User(Resource):
    def __init__(self):
        self.db = UsersDAO()
        self.reqparse = reqparse.RequestParser()

    @marshal_with(user_fields)
    def get(self, uid):
        query = {'uid': uid}
        data = self.db.findOne(query)
        if data:
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

    def post(self, uid):
        query = {'uid': uid}
        data = self.db.insert(query)
        print(data)


user_api.add_resource(User, '/user/v1/<string:uid>', endpoint='user')
