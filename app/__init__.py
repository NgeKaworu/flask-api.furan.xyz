from .job import job
from .author import author
from .todo import todos
from flask import Flask, make_response, jsonify


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    print('__name____name____name__', __name__)
    app.config.from_pyfile('configs.py')

    @app.errorhandler(404)
    def not_found(error):
        return make_response(jsonify({'error': 'Not found'}), 404)

    # 注册页面
    app.register_blueprint(author.bp)
    app.register_blueprint(job.bp)
    app.register_blueprint(todos.bp)

    return app
