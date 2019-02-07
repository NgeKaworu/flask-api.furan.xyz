from flask import jsonify, request, Blueprint, abort, make_response, current_app
from werkzeug.security import check_password_hash
from .usersDao import UsersDAO
import json
import time
from app.auth.auth import Auth

from bson.objectid import ObjectId


bp = Blueprint('login', __name__)
auth = Auth()


@bp.route('/login', methods=['POST'])
def login():
    """
    用户登录
    :return: json
    """
    db = UsersDAO()
    parse = request.json.copy()
    requiredQuery = ['pwd', 'email']
    for i in requiredQuery:
        if i not in parse:
            return make_response(jsonify({
                "message": i + " 不能为空"
            }), 400)

    result = db.findOne(
        {'email': parse['email']}, {'nickname': 1, 'pwd': 1, '_id': 1})

    if result == None:
        abort(404)

    # 验证
    if check_password_hash(result['pwd'], parse['pwd']):
        login_time = time.time()
        logout_time = time.time() + 7200
        db.update({'email': parse['email']}, {
                  "login_time": login_time, "logout_time": logout_time})
        token = auth.encode_auth_token(
            result['_id']['$oid'], login_time).decode()
        return make_response(jsonify({
            "message": "succeed",
            "token": token,
            "uid": result['_id']['$oid'],
            "name": result['nickname']
        }), 200)

    return make_response(jsonify({
        "message": "用户名或密码不匹配"
    }), 400)


@bp.route('/logout/<string:uid>', methods=['GET'])
@auth.identify(resource=UsersDAO)
def logout(uid):
    """
    用户退出
    :return: json
    """
    db = UsersDAO()
    logout_time = time.time()
    db.update({'_id': ObjectId(uid)}, {"logout_time": logout_time})
    return make_response(jsonify({
        "message": "succeed"
    }), 200)
