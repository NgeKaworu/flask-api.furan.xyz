import job
import author
import todos
from flask import Flask, make_response, jsonify


app = Flask(__name__)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


# 注册页面
app.register_blueprint(author.bp)
app.register_blueprint(job.bp)
app.register_blueprint(todos.bp)

if __name__ == '__main__':
    app.run(threaded=True)
