from flask import request, Blueprint
from app.db import getRedis, getMongo

bp = Blueprint('auth', __name__, url_prefix='/author')

@bp.route('/getCount', methods=('GET'))
def getCount():
