from flask import request, Blueprint, jsonify
from dao import DAO

bp = Blueprint('job', __name__, url_prefix='/job')


cloud = DAO('jobSearch', 'cloud')


@bp.route('/getCloud', methods=['GET'])
def getCloud():
    return jsonify(cloud.get())


detail = DAO('jobSearch', 'detail')


@bp.route('/getDetail', methods=['GET'])
def getDetail():
    return jsonify(detail.get())
