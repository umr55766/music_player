import os
import uuid

from flask import Blueprint, current_app as app, request, jsonify

api_v1_blueprint = Blueprint("api_v1", __name__)

ALLOWED_EXTENSIONS = {'mp3'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@api_v1_blueprint.route("/api/v1/upload/", methods=['POST'])
def upload():
    # check if the post request has the file part
    if 'file' not in request.files:
        resp = jsonify({'message': 'No file part in the request'})
        resp.status_code = 400
        return resp
    file = request.files['file']
    if file.filename == '':
        resp = jsonify({'message': 'No file selected for uploading'})
        resp.status_code = 400
        return resp
    if file and allowed_file(file.filename):
        filename = "%s.mp3" % str(uuid.uuid4())
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        resp = jsonify({'message': 'File successfully uploaded'})
        resp.status_code = 201
        return resp
    else:
        resp = jsonify({'message': 'Allowed file types are %s' % ", ".join(ALLOWED_EXTENSIONS)})
        resp.status_code = 400
        return resp
