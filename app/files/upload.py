import uuid
import os
from flask import Flask, request, url_for, send_from_directory, current_app, jsonify, Blueprint
from werkzeug.utils import secure_filename

bp = Blueprint('files', __name__, url_prefix='/files/v1')


def allowed_file(filename):
    return '.' in filename and \
           os.path.splitext(
               filename)[-1][1:] in current_app.config['ALLOWED_EXTENSIONS']


@bp.route('/<filename>')
def uploaded_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'],
                               filename)


@bp.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        uuname = str(uuid.uuid4())
        ext = os.path.splitext(filename)[-1]
        fillname = uuname + ext
        file.save(os.path.join(
            current_app.config['UPLOAD_FOLDER'], fillname))
        file_url = url_for('files.uploaded_file', filename=fillname)
        return jsonify({
            'msg': 'OK',
            'url': file_url
        })
    return jsonify({
        'error': 'bad type'
    })
