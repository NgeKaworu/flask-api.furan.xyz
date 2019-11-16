from flask import request, Blueprint
from flask_restful import Resource, Api


bp = Blueprint('mock', __name__, url_prefix='/mock/v1')
api_mock = Api(bp)


class FailMock(Resource):
    def get(self):
        return {"ok": 'fail'}, 401


class SuccessMock(Resource):
    def get(self):
        return {"ok": 'ok'}, 200


api_mock.add_resource(FailMock, '/fail', endpoint='mockFail')
api_mock.add_resource(SuccessMock, '/success', endpoint='mockSuccess')
