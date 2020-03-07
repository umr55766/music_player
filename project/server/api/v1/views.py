from flask import Blueprint, request
from marshmallow import ValidationError

from project.server import db
from project.server.api.v1.schemas import SongSchema

api_v1_blueprint = Blueprint("api_v1", __name__)


@api_v1_blueprint.route("/api/v1/upload/", methods=['POST'])
def upload():
    schema = SongSchema()

    try:
        song = schema.load(data={**request.form, **request.files})
    except ValidationError as error:
        return error.messages, 400

    db.session.add(song)
    db.session.commit()

    return schema.dump(song), 201
