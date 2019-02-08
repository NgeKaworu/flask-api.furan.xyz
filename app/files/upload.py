import uuid
import os
from flask import Flask, request, url_for, send_from_directory, current_app, Blueprint, g, jsonify
from werkzeug.utils import secure_filename
from flask_restful import Api, Resource

from .filesDao import FilesDAO
from app.auth.auth import Auth

bp = Blueprint('files', __name__, url_prefix='/files/v1')
api_files = Api(bp)

auth = Auth()


def allowed_file(filename):
    return '.' in filename and \
           os.path.splitext(
               filename)[-1][1:] in current_app.config['ALLOWED_EXTENSIONS']


@bp.route('/upload', methods=['POST'])
@auth.identify(resource=FilesDAO)
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
        result = db.insert({
            'name': name,
            'path': path,
            'type': ext[1:],
            'owner': g.token_info["data"]['id']
        })
        return jsonify({
            'message': 'OK',
            'url': file_url,
            'f_id': result['$oid']
        })
    return {
        'message': 'bad type'
    }, 406


class File(Resource):
    decorators = [auth.identify(resource=FilesDAO)]

    def get(self, filename):
        return send_from_directory(current_app.config['UPLOAD_FOLDER'],
                                   filename)

    def delete(self, filename):
        return {
            'message': 'bad type'
        }, 406


api_files.add_resource(File, '/<string:filename>', endpoint = 'file')
