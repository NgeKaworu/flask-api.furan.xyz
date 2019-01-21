from flask import jsonify, request, Blueprint, abort, make_response
from werkzeug.security import check_password_hash
from .usersDao import UsersDAO
import json
import time
from app.auth.auth import Auth


bp = Blueprint('login', __name__, url_prefix='/login')
auth = Auth()


@bp.route('/', methods=['POST'])
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
                "error": i + " is required."
            }), 400)

    result = json.loads(db.findOne(
        {'email': parse['email']}, {'uid': 1, 'pwd': 1, '_id': 0}))
    # 验证
    if check_password_hash(result['pwd'], parse['pwd']):
        login_time = time.time()
        db.update({'email': parse['email']}, {"login_time": login_time})
        token = auth.encode_auth_token(result['uid'], login_time).decode()
        return make_response(jsonify({
            "message": "succeed",
            "token": token
        }), 200)

    return make_response(jsonify({
        "error": "email or pwd not match"
    }), 400)
