from flask import request, Blueprint, jsonify
from app.db import getRedis, getMongo
import json
from bson.json_util import dumps

bp = Blueprint('author', __name__, url_prefix='/author')

_mongodb = 'quotes'
_collections = 'author'

redisDB = getRedis()
mongoClient = getMongo()

mongoDB = mongoClient[_mongodb]
mongoCol = mongoDB[_collections]


@bp.route('/getCount', methods=['GET'])
def getCount():
    redisCance = redisDB.get(_collections)
    if redisCance:
        return jsonify(redisCance)
    else:
        mongoData = [i for i in mongoCol.find()]
        if mongoData:
            jsonData = dumps(mongoData)
            redisDB.set(_collections, jsonData)
            return jsonify(jsonData)
        else:
          return jsonify({'resulte': 'No Data'})
