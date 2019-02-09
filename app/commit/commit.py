import json
from flask import jsonify, request, Blueprint, abort, current_app
from flask_restful import Api, Resource, reqparse, fields, marshal, marshal_with
from .commitDao import CommitDAO
from app.auth.auth import Auth

bp = Blueprint('commit', __name__, url_prefix='/commit/v1')
commit_api = Api(bp)

commit_fields = {
    'commit_id': fields.String,
    'email': fields.String,
    'uri': fields.Url('commit.commit')
}

auth = Auth()


class Commit(Resource):
    decorators = [auth.identify(resource=CommitDAO)]

    def __init__(self):
        self.db = CommitDAO()
        self.reqparse = reqparse.RequestParser()

    @marshal_with(commit_fields)
    def get(self, commit_id):
        query = {'commit_id': commit_id}
        data = self.db.findOne(query)

        if data:
            return jsonify(data)

        abort(404)

    def put(self, commit_id):
        self.reqparse.add_argument(
            'pwd', type=str, required=True, help="is required", location='json')
        self.reqparse.add_argument(
            'email', type=str, required=True, help="is required", location='json')
        query = {"commit_id": commit_id}
        update = self.reqparse.parse_args()
        result = self.db.update(query, update)

        if result['n']:
            return jsonify({'update': commit_id}, 202)

        return abort(404)

    def delete(self, commit_id):
        query = {'commit_id': commit_id}
        result = self.db.remove(query)

        if result['n']:
            return jsonify({'deleted': commit_id}, 202)

        return abort(404)


commit_api.add_resource(Commit, '/<string:commit_id>', endpoint='commit')
