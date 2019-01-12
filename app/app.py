import job
import author
import todos
from flask import Flask

app = Flask(__name__)

# 注册页面
app.register_blueprint(author.bp)
app.register_blueprint(job.bp)
app.register_blueprint(todos.bp)

if __name__ == '__main__':
    app.run(threaded=True)
