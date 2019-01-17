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

    def get(self):
        mongoData = [i for i in self.mongoCol.find()]
        if mongoData:
            # 解析成string bson => string
            return dumps(mongoData)

    def get_one(self, query):
        mongoData = self.mongoCol.find_one(query)
        if mongoData:
            return dumps(mongoData)


class RedisDAO():
    def __init__(self, collection):
        self.redisDB = getRedis()
        self.redisCol = collection

    def __del__(self):
        self.redisDB.connection_pool.disconnect()

    def get(self):
        redisCache = self.redisDB.get(self.redisCol)
        if redisCache:
            return redisCache

    def get_one(self, query):
        redisCache = self.redisDB.get(query)
        if redisCache:
            return redisCache


class DAO(MongoDAO, RedisDAO):
    def __init__(self, db, collection):
        MongoDAO.__init__(self, db, collection)
        RedisDAO.__init__(self, collection)

    # 先读redis, redis没有就读mongo并且写入redis, 都没有就返回404
    def get(self):
        redisCache = RedisDAO.get(self)
        if redisCache:
            return json.loads(redisCache)
        else:
            mongoData = MongoDAO.get(self)
            if mongoData:
                self.redisDB.set(self.redisCol, mongoData)
                return json.loads(mongoData)
            else:
                abort(404)

    def get_one(self, query):
        queryVal, = query.values()
        withQuery = self.redisCol + queryVal
        redisCache = RedisDAO.get_one(self, withQuery)
        if redisCache:
            return json.loads(redisCache)
        else:
            mongoData = MongoDAO.get_one(self, query)
            if mongoData:
                self.redisDB.set(withQuery, mongoData)
                return json.loads(mongoData)
            else:
                abort(404)
