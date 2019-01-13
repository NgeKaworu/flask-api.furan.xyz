from flask import request, Blueprint, jsonify, abort


bp = Blueprint('todos', __name__, url_prefix='/todo/api/v1/tasks')

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


@bp.route('/', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})


@bp.route('/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = list(filter(lambda t: t['id'] == task_id, tasks))
    print(task)
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task[0]})
