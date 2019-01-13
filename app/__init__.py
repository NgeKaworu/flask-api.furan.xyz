from flask import Flask, make_response, jsonify

# from .job import job
# from .author import author
from .todo import todos
from .db import db


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('configs.py')
    db.init_app(app)

    @app.errorhandler(404)
    def not_found(error):
        return make_response(jsonify({'error': 'Not found'}), 404)

    # 注册页面
    # app.register_blueprint(author.bp)
    # app.register_blueprint(job.bp)
    app.register_blueprint(todos.bp)

    return app
