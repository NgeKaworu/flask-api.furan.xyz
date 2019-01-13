from flask import request, Blueprint, jsonify
from ..db.dao import DAO

bp = Blueprint('author', __name__, url_prefix='/author')


@bp.route('/getCount', methods=['GET'])
def getCount():
    author = DAO('quotes', 'author')
    return jsonify(author.get())


@bp.route('/getAbout', methods=['GET'])
def getAbout():
    about = DAO('quotes', 'about')
    param = request.args.get('author')
    query = {'author': param}
    return jsonify(about.get_one(query))
