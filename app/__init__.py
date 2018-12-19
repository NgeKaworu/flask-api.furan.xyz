from flask import Flask, Blueprint

def create_app():
    # create and configure the app
    app = Flask(__name__)

    #注册页面
    from app import author
    app.register_blueprint(author.bp)
    from app import job
    app.register_blueprint(job.bp)

    return app
