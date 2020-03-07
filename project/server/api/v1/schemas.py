from marshmallow import Schema, fields, ValidationError, validates, post_load

from project.server.models import Song


def allowed_file(filename, allowed_extensions):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions


class SongSchema(Schema):
    id = fields.Int(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    song_url = fields.Str(dump_only=True)

    song = fields.Field(required=True)
    title = fields.Str(required=True)
    artist = fields.Str(required=True)
    album = fields.Str(required=True)

    @validates('song')
    def validate_song(self, value):
        if not allowed_file(value.filename, ["mp3"]):
            raise ValidationError("Allowed file types are mp3")

    @post_load
    def make_song(self, data, **kwargs):
        return Song(**data)
