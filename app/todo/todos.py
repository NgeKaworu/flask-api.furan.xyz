from flask import request, Blueprint, jsonify, abort
from flask_restful import Api, Resource

bp = Blueprint('todos', __name__, url_prefix='/todo/v1/tasks')
api_todos = Api(bp)

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


class Todos(Resource):
    def get(self):
        return jsonify({'tasks': tasks})


class Todo(Resource):
    def get(self, id):
        task = list(filter(lambda t: t['id'] == id, tasks))
        if len(task) == 0:
            abort(404)
        return jsonify({'task': task[0]})


api_todos.add_resource(Todos, '/', endpoint='todos')
api_todos.add_resource(Todo, '/<int:id>', endpoint='todo')
