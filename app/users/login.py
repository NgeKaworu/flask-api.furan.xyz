from flask import jsonify, request, Blueprint, abort, make_response
from werkzeug.security import check_password_hash
from .usersDao import UsersDAO
import json

bp = Blueprint('login', __name__, url_prefix='/login')


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
        {'email': parse['email']}, {'pwd': 1, '_id': 0}))
    # 验证
    if check_password_hash(result['pwd'], parse['pwd']):
        return make_response(jsonify({
            "message": "succeed"
        }), 200)

    return make_response(jsonify({
        "error": "email or pwd not match"
    }), 400)
