import redis
import pymongo

_password = 'FRO0o0<,>.'


def getRedis():
    pool = redis.ConnectionPool(
        host='localhost', port=6379, decode_responses=True, password=_password)

    r = redis.Redis(connection_pool=pool)

    return r


def getMongo():
    mongoDB = pymongo.MongoClient(
          'localhost:27017', username='furan', password=_password)
    return mongoDB
