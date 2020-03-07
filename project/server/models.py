# project/server/models.py


import datetime
import os
import uuid

from flask import current_app as app

from project.server import db, bcrypt


class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, email, password, admin=False):
        self.email = email
        self.password = bcrypt.generate_password_hash(
            password, app.config.get("BCRYPT_LOG_ROUNDS")
        ).decode("utf-8")
        self.registered_on = datetime.datetime.now()
        self.admin = admin

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def __repr__(self):
        return "<User {0}>".format(self.email)


class Song(db.Model):

    __tablename__ = "songs"

    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    artist = db.Column(db.String(255), nullable=False)
    album = db.Column(db.String(255), nullable=False)
    song_url = db.Column(db.String(255), nullable=False)

    # artist_id = Column(Integer, ForeignKey(Artist.id), primary_key=True)
    # artist = relationship('Artist', foreign_keys='Song.artist_id')
    #
    # album_id = Column(Integer, ForeignKey(Album.id), primary_key=True)
    # album = relationship('Album', foreign_keys='Song.album_id')

    def __init__(self, title, artist, album, song):
        self.created_at = datetime.datetime.now()
        self.title = title
        self.artist = artist
        self.album = album
        self.song_url = "songs/%s.mp3" % str(uuid.uuid4())
        song.save(os.path.join(app.static_folder, self.song_url))

    def response(self):
        return