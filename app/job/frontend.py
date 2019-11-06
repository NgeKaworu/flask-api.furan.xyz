from flask import request, Blueprint
from flask_restful import Resource, Api, reqparse

import re
import jieba.analyse

from ..db.dao import DAO

bp = Blueprint('frontend', __name__, url_prefix='/frontend/v1')
api_job = Api(bp)


class Frontend(Resource):
    def __init__(self):
        self.db = DAO('jobSearch', 'front')
        self.reqparse = reqparse.RequestParser()
        self.keyWord = r'开发|实习|初|中|高|级|工程|软件|硬件|程序|技术|佛山|管理|程序|员|生|师|web|it'
        self.synonym = [
            (r'javascript', 'js'),
            (r'.net', 'net'),
            (r'bootstrap', 'bs'),
            (r'css3', 'css'),
            (r'html5|html', 'h5'),
            (r'angularjs', 'angular'),
            (r'reactjs', 'react'),
            (r'vuejs', 'vue')
        ]

    # 分词+词频统计
    @staticmethod
    def _analyse(sentence, synonym, allowPOS):
        # 根据规则转换近义词
        newValue = sentence
        for i in synonym:
            newValue = re.sub(i[0], i[1], newValue)

        topWord = jieba.analyse.extract_tags(
            newValue, topK=50, withWeight=True, allowPOS=allowPOS)
        return [{'word': i[0], 'count': i[1]} for i in topWord]

    @staticmethod
    def _filter(value, keyWord):
        return re.sub(keyWord, ' ', value.lower().strip())

    def get(self):
        query = self.reqparse.parse_args()
        # 理论上需要做一层redis
        res, count = self.db.find({**query, 'area': re.compile(query.get('area', ''))}, projection={
            '_id': 0, 'detail': 1})

        detailText = ''.join([i['detail'] for i in res])
        result = self._analyse(detailText, self.synonym, allowPOS=('eng',))

        return result, 200


api_job.add_resource(Frontend, '/', endpoint='frontend')
