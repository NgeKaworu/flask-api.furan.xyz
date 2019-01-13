from flask import request, Blueprint, jsonify
from ..db.dao import DAO

bp = Blueprint('job', __name__, url_prefix='/job')


@bp.route('/getCloud', methods=['GET'])
def getCloud():
    cloud = DAO('jobSearch', 'cloud')
    return jsonify(cloud.get())


@bp.route('/getDetail', methods=['GET'])
def getDetail():
    detail = DAO('jobSearch', 'detail')
    return jsonify(detail.get())
