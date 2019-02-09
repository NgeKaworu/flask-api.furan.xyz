import jwt
import datetime
import time
import json
from functools import wraps
from flask import jsonify, current_app, request, g
from bson.objectid import ObjectId
from app.users.usersDao import UsersDAO
from .policy import Policy


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
                'iss': 'sys',
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

    def identify(self, *paramas, **options):
        def wrapper(func):
            @wraps(func)
            def decorator(*args, **kwargs):
                method = request.method
                blueprint = request.blueprint

                if Policy[blueprint][method] == 'all':
                    return func(*args, **kwargs)

                token = request.headers.get('Authorization')

                if not token:
                    return jsonify({"message": "需要登录"}), 401

                token_info = self.decode_auth_token(token)

                if isinstance(token_info, str):
                    return jsonify({"message": token_info}), 401

                g.token_info = token_info
                db = UsersDAO()
                user_info = db.findOne(
                    {"_id": ObjectId(token_info["data"]['id'])}
                )
                if user_info['logout_time'] > time.time():
                    if 'role' in user_info and user_info['role'] == 'admin':
                        return func(*args, **kwargs)

                    if Policy[blueprint][method] == 'admin':
                        return jsonify({"message": "只有管理员可以使用"}), 401

                    if Policy[blueprint][method] == 'owner':
                        if 'uid' in kwargs and kwargs['uid'] == user_info['_id']['$oid']:
                            return func(*args, **kwargs)

                        resource = options['resource']()
                        resource_info = resource.findOne(kwargs)

                        if resource_info and 'owner' in resource_info and resource_info['owner'] == user_info['_id']['$oid']:
                            return func(*args, **kwargs)

                        return jsonify({"message": "权限不足"}), 401
                        
                    return func(*args, **kwargs)
                else:
                    return jsonify({"message": "登陆超时, 请重新登陆"}), 401
                    
            return decorator
        return wrapper
