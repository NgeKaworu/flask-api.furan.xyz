from flask import request, Blueprint
from flask_restful import Resource, Api, reqparse

from app.db.dao import MongoDAO

bp = Blueprint('feWordCloud', __name__, url_prefix='/feWordCloud/v1')
api_job = Api(bp)


class FeWordCloud(Resource):
    def __init__(self):
        self.db = MongoDAO('jobSearch', 'frontdetail')
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'createTime', type=str, required=True, help="is required", location='args')

    def get(self):
        query = self.reqparse.parse_args()
        return self.db.findOne(query, projection={'_id': 0}), 200


class FeWordCloudDate(Resource):
    def __init__(self):
        self.db = MongoDAO('jobSearch', 'frontdetail')

    def get(self):
        info = self.db.find(projection={"createTime": 1, "_id": 0})
        print(info)
        return info[0], 200


api_job.add_resource(FeWordCloud, '/',
                     endpoint='feWordCloud')
api_job.add_resource(FeWordCloudDate, '/date', endpoint='feWordCloudDate')
