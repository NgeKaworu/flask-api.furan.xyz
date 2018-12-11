from flask import Flask, Blueprint


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    #初始化数据库
    from app import db
    db.init_app(app)

    #注册页面
    from app import author
    app.register_blueprint(author.bp)

    return app
