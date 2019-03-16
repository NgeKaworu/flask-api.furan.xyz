from flask import request, Blueprint, abort, jsonify
from .articleDao import ArticleDAO

bp = Blueprint('tags', __name__, url_prefix='/tags/v1')


@bp.route('/', methods=['GET'])
@bp.route('/<int:page>', methods=['GET'])
def Archive(page=1):
    limit = 10
    page = page - 1
    skip = page * limit
    db = ArticleDAO()
    pipline = [
        {'$unwind': '$tags'},
        {
            "$group": {
                "_id": '$tags',
                "sum": {'$sum': 1},
            }
        },
        {"$sort": {'sum': -1}},
        {"$skip": skip},
        {"$limit": limit},
    ]
    result = db.aggregate(pipline)
    if result:
        return jsonify(result)
    return jsonify({"message": '没有找到'}), 404


@bp.route('/<string:tag>', methods=['GET'],  strict_slashes=False)
@bp.route('/<string:tag>/<int:page>', methods=['GET'], strict_slashes=False)
def logout(tag, page=1):
    db = ArticleDAO()
    query = {'tags': tag}
    result, count = db.find(query=query, limit=10, page=page-1, projection={
        'title': 1, '_id': 1, 'content': 1, 'owner': 1}, sort=[('last_update_date', -1)])
    if result:
        # 过滤 以及截取内容
        reps = {'list': [{**i, '_id': i['_id']['$oid'],
                          'content': '\n'.join(i['content'].split('\n', 5)[:5])} for i in result], 'total': count}
        return jsonify(reps)
    return jsonify({"message": '没有找到'}), 404
