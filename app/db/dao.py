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

    def find(self, limit=0, page=0, projection=None, sort='_id'):
        skip = page * limit
        cursor = self.mongoCol.find({}, projection).skip(
            skip).limit(limit).sort(sort)
        count = cursor.count()
        result = [i for i in cursor]
        # 解析成 json bson => string => json
        return json.loads(dumps(result)), count if result else result

    def findOne(self, query, projection=None):
        result = self.mongoCol.find_one(query, projection)
        return json.loads(dumps(result)) if result else result

    def update(self, query, update):
        result = self.mongoCol.update(query, {'$set': update})
        return result

    def remove(self, query):
        result = self.mongoCol.remove(query)
        return result

    def insert(self, query):
        result = self.mongoCol.insert(query)
        return json.loads(dumps(result)) if result else result

    def aggregate(self, pipeline=[]):
        cursor = self.mongoCol.aggregate(pipeline)
        result = [i for i in cursor]
        # 解析成 json bson => string => json
        return json.loads(dumps(result)), count if result else result


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
    def get(self, *arg, **kwarg):
        redisCache = RedisDAO.get(self, self.redisCol)
        if redisCache:
            return json.loads(redisCache)
        else:
            mongoData, count = MongoDAO.find(self, *arg, **kwarg)
            if mongoData:
                self.redisDB.set(self.redisCol, json.dumps(mongoData))
                return mongoData
            else:
                abort(404)

    def get_one(self, query):
        queryVal, = query.values()
        withQuery = self.redisCol + queryVal
        redisCache = RedisDAO.get(self, withQuery)
        if redisCache:
            return json.loads(redisCache)
        else:
            mongoData = MongoDAO.findOne(self, query)
            if mongoData:
                self.redisDB.set(withQuery, json.dumps(mongoData))
                return mongoData
            else:
                abort(404)
