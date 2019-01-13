import redis
import pymongo
from flask import current_app, Flask

app = Flask('MainApp')


def getRedis():
    with app.app_context():
        pool = redis.ConnectionPool(
            host='localhost', port=6379, decode_responses=True, password=current_app.config['PASSWORD'])

        r = redis.Redis(connection_pool=pool)
        return r


def getMongo():
    with app.app_context():
        mongoDB = pymongo.MongoClient(
            'localhost:27017', username='furan', password=current_app.config['PASSWORD'], connect=False)
        return mongoDB
