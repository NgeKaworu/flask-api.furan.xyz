import redis
import pymongo

_password = 'FRO0o0<,>.'


def getRedis():
  pool = redis.ConnectionPool(
      host='localhost', port=6379, decode_responses=True, password=_password)
  return pool


def getMongo():
  mongoDB = pymongo.MongoClient(
      'localhost:27017', username='furan', password=_password)
  return mongoDB
