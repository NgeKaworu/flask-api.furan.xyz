from flask import jsonify, request, Blueprint, abort
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
    requiredQuery = ['nickname', 'pwd', 'email']
    for i in requiredQuery:
        if i not in parse:
            return jsonify({"message": i + " 不能为空"}), 400

    # 唯一字段
    uniqueField = ['email']
    for i in uniqueField:
        if db.findOne({i: parse[i]}):
            return jsonify({"message": i + " 已经存在"}), 302

    # 加盐
    parse['pwd'] = generate_password_hash(parse['pwd'])

    result = db.insert(parse)
    if result:
        return jsonify({"message": "succeed"}), 201

    return jsonify({"message": "未知错误"}), 400
