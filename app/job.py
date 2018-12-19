from flask import request, Blueprint, jsonify
from app.dao import DAO

bp = Blueprint('job', __name__, url_prefix='/job')


@bp.route('/getCloud', methods=['GET'])
def getCloud():
    db = DAO('jobSearch', 'cloud')
    return jsonify(db.get())


@bp.route('/getDetail', methods=['GET'])
def getDetail():
    db = DAO('jobSearch', 'detail')
    return jsonify(db.get())
