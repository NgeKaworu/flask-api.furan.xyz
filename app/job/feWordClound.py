from flask import request, Blueprint
from flask_restful import Resource, Api, reqparse

from app.db.dao import MongoDAO

bp = Blueprint('feWordClound', __name__, url_prefix='/feWordClound/v1')
api_job = Api(bp)


class FeWordClound(Resource):
    def __init__(self):
        self.db = MongoDAO('jobSearch', 'frontdetail')
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'createTime', type=str, required=True, help="is required", location='args')

    def get(self):
        query = self.reqparse.parse_args()
        print(query)
        return self.db.findOne(query, projection={'_id': 0}), 200


class FeWordCloundDate(Resource):
    def __init__(self):
        self.db = MongoDAO('jobSearch', 'frontdetail')

    def get(self):
        return self.db.find(projection={"createTime": 1, "_id": 0}), 200


api_job.add_resource(FeWordClound, '/',
                     endpoint='feWordClound')
api_job.add_resource(FeWordCloundDate, '/date', endpoint='feWordCloundDate')
