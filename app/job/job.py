from flask import request, Blueprint, jsonify
from flask_restful import Resource, Api

from ..db.dao import DAO

bp = Blueprint('job', __name__, url_prefix='/job/v1')
api_job = Api(bp)


class JobCloud(Resource):
    def __init__(self):
        self.db = DAO('jobSearch', 'cloud')

    def get(self):
        return jsonify(self.db.get())


class JobDetail(Resource):
    def __init__(self):
        self.db = DAO('jobSearch', 'detail')

    def get(self):
        return jsonify(self.db.get())


api_job.add_resource(JobCloud, '/cloud', endpoint='cloud')
api_job.add_resource(JobDetail, '/detail', endpoint='detail')
