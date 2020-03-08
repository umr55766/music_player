import os

from flask import Blueprint, request, current_app
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

        return redirect("/") if request.args.get('redirectToHome') else (self.schema.dump(song), 200)

    def delete(self, song_id):
        song = Song.query.filter_by(id=song_id).first()

        if not song:
            return 404

        os.remove(os.path.join(current_app.static_folder, song.song_url))
        db.session.delete(song)
        db.session.commit()
        return "", 204


song_view = SongAPI.as_view('song_api')
api_v1_blueprint.add_url_rule('/songs/', defaults={'song_id': None}, view_func=song_view, methods=['GET',])
api_v1_blueprint.add_url_rule('/songs/', view_func=song_view, methods=['POST',])
api_v1_blueprint.add_url_rule('/songs/<int:song_id>/', view_func=song_view, methods=['GET', 'PUT', 'DELETE'])
