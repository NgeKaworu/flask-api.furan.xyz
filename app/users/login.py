from flask import request, Blueprint, abort, current_app, jsonify, g
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
            return jsonify({"message": i + " 不能为空"}), 400

    result = db.findOne(
        {'email': parse['email']}, {'nickname': 1, 'pwd': 1, '_id': 1})

    if result == None:
        abort(404)

    # 验证
    if check_password_hash(result['pwd'], parse['pwd']):
        login_time = time.time()
        logout_time = time.time() + 60 * 60 * 24 * 3
        db.update({'email': parse['email']}, {
                  "login_time": login_time, "logout_time": logout_time})
        token = auth.encode_auth_token(
            result['_id']['$oid'], result['nickname'], login_time).decode()
        return jsonify({
            "message": "succeed",
            "token": token,
            "uid": result['_id']['$oid'],
            "name": result['nickname'],
            'token_indate': logout_time,
        })

    return jsonify({"message": "用户名或密码不匹配"}), 400


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
    return jsonify({'message': 'succeed'}), 200


@bp.route('/checkToken', methods=['GET'])
@auth.identify(resource=UsersDAO)
def checkToken():
    """
    token验证
    :return: json
    """
    print(g.token_info)
    token_info = g.token_info
    user_data = token_info['data']

    name, uid, = user_data['name'], user_data['id']

    print(name, uid)

    return jsonify({'message': 'succeed', "uid": uid, "name": name}), 200
