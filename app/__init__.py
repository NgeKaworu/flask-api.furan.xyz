from flask import Flask, make_response, jsonify

from .job import job
from .author import author
from .todo import todos
from .users import users
from .users import register
from .users import login
from .files import upload
from .article import article


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('configs.py')

    # 注册页面
    app.register_blueprint(author.bp)
    app.register_blueprint(job.bp)
    app.register_blueprint(todos.bp)
    app.register_blueprint(users.bp)
    app.register_blueprint(register.bp)
    app.register_blueprint(login.bp)
    app.register_blueprint(upload.bp)
    app.register_blueprint(article.bp)

    return app
