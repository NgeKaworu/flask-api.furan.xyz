import redis
import pymongo
from flask import current_app


def getRedis():
    pool = redis.ConnectionPool(
        host='localhost', port=6379, decode_responses=True, password=current_app.config['PASSWORD'])
    redisdb = redis.Redis(connection_pool=pool)
    return redisdb


def getMongo():
    mongodb = pymongo.MongoClient(
        'localhost:27017', username='furan', password=current_app.config['PASSWORD'], connect=False)
    return mongodb
