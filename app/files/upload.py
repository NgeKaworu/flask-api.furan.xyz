import uuid
import os
from flask import Flask, request, url_for, send_from_directory, current_app, jsonify, Blueprint
from werkzeug.utils import secure_filename
from flask_restful import Api, Resource, reqparse, fields, marshal_with, marshal
from .filesDao import FilesDAO

bp = Blueprint('files', __name__, url_prefix='/files/v1')
api_files = Api(bp)


def allowed_file(filename):
    return '.' in filename and \
           os.path.splitext(
               filename)[-1][1:] in current_app.config['ALLOWED_EXTENSIONS']


@bp.route('/upload', methods=['POST'])
def upload_file():
    db = FilesDAO()
    file = request.files['file']
    if file and allowed_file(file.filename):
        name = secure_filename(file.filename)
        uuname = str(uuid.uuid4())
        ext = os.path.splitext(name)[-1]
        path = uuname + ext
        file.save(os.path.join(
            current_app.config['UPLOAD_FOLDER'], path))
        file_url = url_for('files.file', filename=path)
        db.insert({
            'name': name,
            'path': path,
            'type': ext[1:],
            # 'owner': g.token_info["data"]['id']
        })
        return jsonify({
            'msg': 'OK',
            'url': file_url
        })
    return jsonify({
        'error': 'bad type'
    })


class File(Resource):
    def get(self, filename):
        return send_from_directory(current_app.config['UPLOAD_FOLDER'],
                                   filename)


api_files.add_resource(File, '/<string:filename>', endpoint='file')
