from flask import request, Blueprint, jsonify
from dao import DAO

bp = Blueprint('author', __name__, url_prefix='/author')


tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]


@bp.route('/getCount', methods=['GET'])
def getCount():
    return jsonify(author.get())


@bp.route('/getAbout', methods=['GET'])
def getAbout():
    param = request.args.get('author')
    query = {'author': param}
    return jsonify(about.get_one(query))
