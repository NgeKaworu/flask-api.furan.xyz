from flask import request, Blueprint, jsonify

bp = Blueprint('todos', __name__, url_prefix='/todo/api/v1')

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


@bp.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})
