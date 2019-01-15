from .db import getRedis, getMongo
from bson.json_util import dumps
import json
from flask import abort


class DAO(object):
    def __init__(self, db, collection):
        self.redisDB = getRedis()
        self.redisCol = collection
        self.mongoClient = getMongo()
        self.mongoDB = self.mongoClient[db]
        self.mongoCol = self.mongoDB[collection]

    def __del__(self):
        self.mongoClient.close()
        self.redisDB.connection_pool.disconnect()

    def get(self):
        redisCache = self.redisDB.get(self.redisCol)
        if redisCache:
            return json.loads(redisCache)
        else:
            mongoData = [i for i in self.mongoCol.find()]
            if mongoData:
                jsonData = dumps(mongoData)
                self.redisDB.set(self.redisCol, jsonData)
                return json.loads(jsonData)
            else:
                abort(404)

    def get_one(self, query):
        queryVal, = query.values()
        withQuery = self.redisCol + queryVal
        redisCache = self.redisDB.get(withQuery)
        if redisCache:
            return json.loads(redisCache)
        else:
            mongoData = self.mongoCol.find_one(query)
            if mongoData:
                jsonData = dumps(mongoData)
                print(jsonData)
                self.redisDB.set(withQuery, jsonData)
                return json.loads(jsonData)
            else:
                abort(404)
