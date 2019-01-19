from .db import getRedis, getMongo
from bson.json_util import dumps
import json
from flask import abort


class MongoDAO():
    def __init__(self, db, collection):
        self.mongoClient = getMongo()
        self.mongoDB = self.mongoClient[db]
        self.mongoCol = self.mongoDB[collection]

    def __del__(self):
        self.mongoClient.close()

    def find(self):
        result = [i for i in self.mongoCol.find()]
        # 解析成string bson => string
        return dumps(result)

    def findOne(self, query):
        result = self.mongoCol.find_one(query)
        return dumps(result)

    def update(self, query, update):
        result = self.mongoCol.update(query, {'$set': update})
        return result

    def remove(self, query):
        result = self.mongoCol.remove(query)
        return result

    def insert(self, query):
        result = self.mongoCol.insert(query)
        return result


class RedisDAO():
    def __init__(self, collection):
        self.redisDB = getRedis()
        self.redisCol = collection

    def __del__(self):
        self.redisDB.connection_pool.disconnect()

    def get(self, query):
        result = self.redisDB.get(query)
        return result


class DAO(MongoDAO, RedisDAO):
    def __init__(self, db, collection):
        MongoDAO.__init__(self, db, collection)
        RedisDAO.__init__(self, collection)

    # 先读redis, redis没有就读mongo并且写入redis, 都没有就返回404
    def get(self):
        redisCache = RedisDAO.get(self, self.redisCol)
        if redisCache:
            return json.loads(redisCache)
        else:
            mongoData = MongoDAO.find(self)
            if mongoData:
                self.redisDB.set(self.redisCol, mongoData)
                return json.loads(mongoData)
            else:
                abort(404)

    def get_one(self, query):
        queryVal, = query.values()
        query = self.redisCol + queryVal
        redisCache = RedisDAO.get(self, query)
        if redisCache:
            return json.loads(redisCache)
        else:
            mongoData = MongoDAO.findOne(self, query)
            if mongoData:
                self.redisDB.set(query, mongoData)
                return json.loads(mongoData)
            else:
                abort(404)
