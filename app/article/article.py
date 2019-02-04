import json
from flask import jsonify, request, Blueprint, abort, make_response, current_app, url_for
from flask_restful import Api, Resource, reqparse
from .articleDao import ArticleDAO
from app.auth.auth import Auth
from bson.objectid import ObjectId

bp = Blueprint('article', __name__, url_prefix='/article/v1')
article_api = Api(bp)

auth = Auth()


class Articles(Resource):
    # decorators = [auth.identify(resource=ArticleDAO)]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'title', type=str, required=True, help="is required", location='json')
        self.reqparse.add_argument(
            'content', type=str, required=True, help="is required", location='json')
        self.reqparse.add_argument(
            'fileList', type=list, help="is required", location='json')

    # def get(self):
    #     return tasks

    def post(self):
        db = ArticleDAO()
        result = json.loads(db.insert(self.reqparse.parse_args()))
        if result:
            repson = {'article_id': result['$oid']}
        return repson, 201


class Article(Resource):
    # decorators = [auth.identify(resource=ArticleDAO)]

    def __init__(self):
        self.db = ArticleDAO()
        self.reqparse = reqparse.RequestParser()

    def get(self, article_id):
        query = {'_id': ObjectId(article_id)}
        data = self.db.findOne(query)
        if data:
            article_url = url_for('article.article', article_id=article_id)
            result = json.loads(data)
            result['article_id'] = article_id
            result['url'] = article_url
            return result
        abort(404)

    def put(self, article_id):
        self.reqparse.add_argument(
            'title', type=str, required=True, help="is required", location='json')
        self.reqparse.add_argument(
            'content', type=str, required=True, help="is required", location='json')
        self.reqparse.add_argument(
            'fileList', type=list, help="is required", location='json')

        query = {'_id': ObjectId(article_id)}
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


article_api.add_resource(Articles, '/', endpoint='articles')
article_api.add_resource(Article, '/<string:article_id>', endpoint='article')
