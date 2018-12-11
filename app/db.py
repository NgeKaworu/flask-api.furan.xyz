import redis
import pymongo
from flask import g

_password = 'FRO0o0<,>.'


def getRedis():
    if 'redisDB' not in g:
        pool = redis.ConnectionPool(
            host='localhost', port=6379, decode_responses=True, password=_password)

        g.redisDB = redis.Redis(connection_pool=pool)

    return g.redisDB


def getMongo():
    if 'mongoDB' not in g:
            g.mongoDB = pymongo.MongoClient(
                'localhost:27017', username='furan', password=_password)
    return g.mongoDB


def close_db(e=None):
    redisDB = g.pop('redisDB', None)
    if redisDB:
        redisDB.connection_pool.disconnect()
    
    mongoDB = g.pop('mongoDB', None)
    if mongoDB:
        mongoDB.close()


def init_app(app):
    app.teardown_appcontext(close_db)
