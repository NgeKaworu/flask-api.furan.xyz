from flask import request, Blueprint, jsonify
from app.db import getRedis, getMongo
import json
from bson.json_util import dumps

bp = Blueprint('author', __name__, url_prefix='/author')

_mongodb = 'quotes'

redisDB = getRedis()
mongoClient = getMongo()

mongoDB = mongoClient[_mongodb]


@bp.route('/getCount', methods=['GET'])
def getCount():
    _collections = 'author'
    mongoCol = mongoDB[_collections]
    redisCache = redisDB.get(_collections)
    if redisCache:
        return jsonify(redisCache)
    else:
        mongoData = [i for i in mongoCol.find()]
        if mongoData:
            jsonData = dumps(mongoData)
            redisDB.set(_collections, jsonData)
            return jsonify(jsonData)
        else:
          return jsonify({'resulte': 'No Data'})


@bp.route('/getAbout', methods=['GET'])
def getAbout():
    _collections = 'about'
    mongoCol = mongoDB[_collections]

    param = request.args.get('author')

    cacheName = 'About' + param
    redisCache = redisDB.get(cacheName)

    if redisCache:
        return jsonify(redisCache)
    else:
        mongoData = mongoCol.find_one({ 'author': param })
        if mongoData:
            jsonData = dumps(mongoData)
            redisDB.set(cacheName, jsonData)
            return jsonify(jsonData)
        else:
          return jsonify({'resulte': 'No Data'})
