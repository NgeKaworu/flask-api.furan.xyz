import redis
import pymongo
from settings import password


def getRedis():
    pool = redis.ConnectionPool(
        host='localhost', port=6379, decode_responses=True, password=password)

    r = redis.Redis(connection_pool=pool)
    return r


def getMongo():
    mongoDB = pymongo.MongoClient(
        'localhost:27017', username='furan', password=password, connect=False)
    return mongoDB
