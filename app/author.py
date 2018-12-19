from flask import request, Blueprint, jsonify
from app.dao import DAO

bp = Blueprint('author', __name__, url_prefix='/author')


@bp.route('/getCount', methods=['GET'])
def getCount():
    db = DAO('quotes', 'author')
    return jsonify(db.get())


@bp.route('/getAbout', methods=['GET'])
def getAbout():
    db = DAO('quotes', 'about')
    param = request.args.get('author')
    query = {'author': param}
    return jsonify(db.get_one(query))
