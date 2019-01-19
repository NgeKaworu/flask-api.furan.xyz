from flask import jsonify, request, Blueprint, abort, make_response
from werkzeug.security import generate_password_hash
from .usersDao import UsersDAO

bp = Blueprint('register', __name__, url_prefix='/register')


@bp.route('/', methods=['POST'])
def register():
    """
    用户注册
    :return: json
    """
    db = UsersDAO()
    parse = request.json.copy()
    # 验证关键字
    requiredQuery = ['uid', 'pwd', 'email']
    for i in requiredQuery:
        if i not in parse:
            return make_response(jsonify({
                "error": i + " is required."
            }), 400)

    # 唯一字段
    uniqueField = ['uid', 'email']
    for i in uniqueField:
        if db.findOne({i: parse[i]}) != 'null':
            return make_response(jsonify({
                "message": i + " is existed"
            }), 302)

    # 加盐
    parse['pwd'] = generate_password_hash(parse['pwd'])

    result = db.insert(parse)
    if result:
        return make_response(jsonify({"message": "succeed"}), 201)

    abort(400)
