from flask import request, Blueprint, jsonify
from dao import DAO

bp = Blueprint('author', __name__, url_prefix='/author')


author = DAO('quotes', 'author')
@bp.route('/getCount', methods=['GET'])
def getCount():
    return jsonify(author.get())


about = DAO('quotes', 'about')
@bp.route('/getAbout', methods=['GET'])
def getAbout():
    param = request.args.get('author')
    query = {'author': param}
    return jsonify(about.get_one(query))
