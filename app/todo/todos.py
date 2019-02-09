from flask import request, Blueprint,   abort
from flask_restful import Api, Resource, reqparse, fields, marshal_with, marshal

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

task_fields = {
    'title': fields.String,
    'description': fields.String,
    'done': fields.Boolean,
    'uri': fields.Url('todos.todo')
}


class Todos(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type=str, required=True,
                                   help='No task title provided', location='json')
        self.reqparse.add_argument('description', type=str, default="",
                                   location='json')
        self.reqparse.add_argument('done', type=bool, location='json')

    @marshal_with(task_fields)
    def get(self):
        return tasks

    @marshal_with(task_fields)
    def post(self):
        task = {}
        args = self.reqparse.parse_args()
        task['id'] = tasks[-1]['id']+1
        for k, v in args.items():
            if v != None:
                task[k] = v
        tasks.append(task)
        return task, 201


class Todo(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type=str, location='json')
        self.reqparse.add_argument('description', type=str, location='json')
        self.reqparse.add_argument('done', type=bool, location='json')

    @marshal_with(task_fields)
    def get(self, id):
        task = list(filter(lambda x: x['id'] == id, tasks))
        if len(task) == 0:
            abort(404)
        task = task[0]
        return task

    @marshal_with(task_fields)
    def put(self, id):
        task = list(filter(lambda t: t['id'] == id, tasks))
        if len(task) == 0:
            abort(404)
        task = task[0]
        args = self.reqparse.parse_args()
        for k, v in args.items():
            if v != None:
                task[k] = v
        return task

    def delete(self, id):
        task = list(filter(lambda x: x['id'] == id, tasks))
        if len(task) == 0:
            abort(404)
        task = task[0]
        tasks.remove(task)
        return {'result': True}


api_todos.add_resource(Todos, '/', endpoint='todos')
api_todos.add_resource(Todo, '/<int:id>', endpoint='todo')
