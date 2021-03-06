from flask import request, Blueprint, abort, current_app, url_for, g
from flask_restful import Api, Resource, reqparse
from .articleDao import ArticleDAO
from app.auth.auth import Auth
from bson.objectid import ObjectId
import time

bp = Blueprint('article', __name__, url_prefix='/article/v1')
article_api = Api(bp)

auth = Auth()


class Articles(Resource):
    decorators = [auth.identify(resource=ArticleDAO)]

    def __init__(self):
        self.db = ArticleDAO()
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'title', type=str, required=True, help="is required", location='json')
        self.reqparse.add_argument(
            'content', type=str, required=True, help="is required", location='json')
        self.reqparse.add_argument(
            'fileList', type=list, help="is required", location='json')

    def get(self, page=1):
        result, count = self.db.find(limit=10, page=page-1, projection={
            'title': 1, '_id': 1, 'content': 1, 'owner': 1, 'tags': 1}, sort=[('last_update_date', -1)])
        if result:
            # 过滤 以及截取内容
            reps = {'list': [{**i, '_id': i['_id']['$oid'],
                              'content': '\n'.join(i['content'].split('\n', 5)[:5])} for i in result], 'total': count}
            return reps
        abort(404)

    def post(self):
        db = ArticleDAO()
        owner = g.token_info['data']['id']
        result = db.insert({**self.reqparse.parse_args(),
                            "owner": owner, 'create_date': time.time(), 'last_update_date': time.time()})
        if result:
            repson = {'article_id': result['$oid']}
            return repson, 201

        abort(404)


class Article(Resource):
    decorators = [auth.identify(resource=ArticleDAO)]

    def __init__(self):
        self.db = ArticleDAO()
        self.reqparse = reqparse.RequestParser()

    def get(self, article_id):

        try:
            query = {'_id': ObjectId(article_id)}
            result = self.db.findOne(query)
            if result:
                article_url = url_for('article.article', article_id=article_id)
                result['article_id'] = article_id
                result['url'] = article_url
                return result
        except:
            abort(404)
        abort(404)

    def put(self, article_id):
        self.reqparse.add_argument(
            'title', type=str, required=True, help="is required", location='json')
        self.reqparse.add_argument(
            'content', type=str, required=True, help="is required", location='json')
        self.reqparse.add_argument(
            'fileList', type=list, location='json')
        self.reqparse.add_argument(
            'tags', type=list, location='json')
        query = {'_id': ObjectId(article_id)}
        update = {**self.reqparse.parse_args(), 'last_update_date': time.time()}
        result = self.db.update(query, update)
        if result['n']:
            return {'update': article_id}, 202

        abort(404)

    def delete(self, article_id):
        query = {'_id': ObjectId(article_id)}
        result = self.db.remove(query)
        if result['n']:
            return {'deleted': article_id}, 202

        abort(404)


article_api.add_resource(Articles, '/', '/<int:page>', endpoint='articles')
article_api.add_resource(Article, '/<string:article_id>', endpoint='article')
