import redis
import pymongo
import click
from flask import current_app,  g


def getRedis():
    if 'redis' not in g:
        pool = redis.ConnectionPool(
            host='localhost', port=6379, decode_responses=True, password=current_app.config['PASSWORD'])
        g.redis = redis.Redis(connection_pool=pool)
        return g.redis


def getMongo():
    if 'mongo' not in g:
        g.mongo = pymongo.MongoClient(
            'localhost:27017', username='furan', password=current_app.config['PASSWORD'], connect=False)
        return g.mongo


def close_db(e=None):
    redis = g.pop('redis', None)
    mongo = g.pop('mongo', None)

    if redis is not None:
        redis.connection_pool.disconnect()

    if mongo is not None:
        mongo.close()


def init_app(app):
    with app.app_context():
        getRedis()
        getMongo()
    app.teardown_appcontext(close_db)
