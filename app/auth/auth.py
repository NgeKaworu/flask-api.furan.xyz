import jwt
import datetime
import time
import json
from functools import wraps
from flask import jsonify, current_app, request, make_response
from app.users.usersDao import UsersDAO


class Auth():
    def __init__(self, app=None):
        self.app = app

    @staticmethod
    def encode_auth_token(user_id, login_time):
        """
        生成认证Token
        :param user_id: int
        :param login_time: int(timestamp)
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, hours=2),
                'iat': datetime.datetime.utcnow(),
                'iss': 'ken',
                'data': {
                    'id': user_id,
                    'login_time': login_time
                }
            }
            return jwt.encode(
                payload,
                current_app.config['SECRET_KEY'],
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        验证Token
        :param auth_token:
        :return: integer|string
        """
        try:
            # 增加10秒验证余地
            # payload = jwt.decode(auth_token, current_app.config['SECRET_KEY'], leeway=datetime.timedelta(seconds=10))
            # 取消过期时间验证
            # payload = jwt.decode(auth_token, current_app.config['SECRET_KEY'], options={'verify_exp': False})
            payload = jwt.decode(auth_token, current_app.config['SECRET_KEY'])
            if ('data' in payload and 'id' in payload['data']):
                return payload
            else:
                raise jwt.InvalidTokenError
        except jwt.ExpiredSignatureError:
            return 'Token过期'
        except jwt.InvalidTokenError:
            return '无效Token'

    def identify(self, func):
        @wraps(func)
        def decorator(*args, **kwargs):
            db = UsersDAO()
            token = request.headers.get('Authorization')
            if not token:
                return make_response(jsonify({
                    "error": "need token"
                }), 401)
            result = self.decode_auth_token(token)
            if isinstance(result, str):
                return make_response(jsonify({
                    "error": result
                }), 401)
            user_info = json.loads(db.findOne({"uid": result["data"]['id']}))
            if result["data"]['id'] == kwargs['uid'] and user_info['logout_time'] > time.time():
                ret = func(*args, **kwargs)
                return ret
            else:
                return make_response(jsonify({
                    "error": "permission denied"
                }), 401)
        return decorator
