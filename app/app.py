from flask import Flask

app = Flask(__name__)

#注册页面
import author
app.register_blueprint(author.bp)
import job
app.register_blueprint(job.bp)

if __name__ == '__main__':
    app.run()
