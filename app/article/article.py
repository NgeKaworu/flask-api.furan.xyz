import json
from flask import jsonify, request, Blueprint, abort, make_response, current_app
from flask_restful import Api, Resource, reqparse, fields, marshal, marshal_with
from .articleDao import ArticleDAO
from app.auth.auth import Auth

bp = Blueprint('article', __name__, url_prefix='/article/v1')
article_api = Api(bp)

article_fields = {
    'article_id': fields.String,
    'email': fields.String,
    'uri': fields.Url('article.article')
}

auth = Auth()


class Article(Resource):
    decorators = [auth.identify(resource=ArticleDAO)]

    def __init__(self):
        self.db = ArticleDAO()
        self.reqparse = reqparse.RequestParser()

    @marshal_with(article_fields)
    def get(self, article_id):
        query = {'article_id': article_id}
        data = self.db.findOne(query)
        if data:
            return json.loads(data)
        abort(404)

    def put(self, article_id):
        self.reqparse.add_argument(
            'pwd', type=str, required=True, help="is required", location='json')
        self.reqparse.add_argument(
            'email', type=str, required=True, help="is required", location='json')
        query = {"article_id": article_id}
        update = self.reqparse.parse_args()
        result = self.db.update(query, update)
        if result['n']:
            return make_response(jsonify({'update': article_id}), 202)
        return abort(404)

    def delete(self, article_id):
        query = {'article_id': article_id}
        result = self.db.remove(query)
        if result['n']:
            return make_response(jsonify({'deleted': article_id}), 202)
        return abort(404)


article_api.add_resource(Article, '/<string:article_id>', endpoint='article')
