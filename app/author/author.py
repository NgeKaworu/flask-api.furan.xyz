from flask import request, Blueprint, jsonify
from flask_restful import Resource, Api

from ..db.dao import DAO

bp = Blueprint('author', __name__, url_prefix='/author/v1')
api_author = Api(bp)


class AuthorCount(Resource):
    def __init__(self):
        self.db = DAO('quotes', 'author')

    def get(self):
        return jsonify(self.db.get())


class AuthorAbout(Resource):
    def __init__(self):
        self.db = DAO('quotes', 'about')

    def get(self, author):
        query = {'author': author}
        return jsonify(self.db.get_one(query))


api_author.add_resource(AuthorCount, '/', endpoint='authorcount')
api_author.add_resource(AuthorAbout, '/about/<string:author>',
                        endpoint='authorabout')
