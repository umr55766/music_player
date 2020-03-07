from flask import Blueprint, request
from flask.views import MethodView
from marshmallow import ValidationError
from werkzeug.utils import redirect

from project.server import db
from project.server.api.v1.schemas import SongSchema
from project.server.models import Song

api_v1_blueprint = Blueprint("api_v1", __name__)


class SongAPI(MethodView):
    schema = SongSchema()

    def get(self, song_id):
        if song_id is None:
            songs = Song.query.all()
            return {"songs": self.schema.dump(songs, many=True)}, 200
        else:
            song = Song.query.get(song_id)
            return self.schema.dump(song), 200 if song else 404

    def post(self):
        try:
            song = self.schema.load(data={**request.form, **request.files})
        except ValidationError as error:
            return error.messages, 400

        db.session.add(song)
        db.session.commit()

        return redirect("http://localhost:5000")

    def delete(self, song_id):
        result = Song.query.filter_by(id=song_id).delete()
        db.session.commit()
        return "", 204 if result else 404


song_view = SongAPI.as_view('song_api')
api_v1_blueprint.add_url_rule('/songs/', defaults={'song_id': None}, view_func=song_view, methods=['GET',])
api_v1_blueprint.add_url_rule('/songs/', view_func=song_view, methods=['POST',])
api_v1_blueprint.add_url_rule('/songs/<int:song_id>/', view_func=song_view, methods=['GET', 'PUT', 'DELETE'])
