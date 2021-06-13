"""Models for podcast transcript search app."""

from typing import Optional, Dict, Any
from datetime import datetime
import re
from functools import cached_property

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON

db = SQLAlchemy()

class Podcast(db.Model):
    """A podcast."""

    __tablename__ = "podcasts"

    podcast_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    title = db.Column(db.String)
    img_url = db.Column(db.String)
    description = db.Column(db.Text)

    episodes = db.relationship("Episode", backref="podcast")

    def __repr__(self):
        return f"<Podcast podcast_id={self.podcast_id} title={self.title}>"


class Episode(db.Model):
    """A podcast episode."""

    __tablename__ = "episodes"

    episode_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    podcast_id = db.Column(
        db.Integer(), db.ForeignKey("podcasts.podcast_id"))
    episode_title = db.Column(db.String)
    description = db.Column(db.Text)
    release_date = db.Column(db.DateTime)
    mp3_url = db.Column(db.String)
    transcript = db.Column(db.JSON)
    status = db.Column(db.String)
    guid = db.Column(db.String)

    def __repr__(self):
        return (
            f"<Episode episode_id={self.episode_id} episode_title={self.episode_title}>"
        )
    @cached_property
    def cache_id(self) -> str:
        """Hash fn that generates a unique id for a podcast episode. 
    
        This is the filename for the transcriptions cache stored used as back-up.
        It consists of the first 15 chars of the podcast and episode titles + the
        32 last episode uuid chars.
        """
        
        # TODO: check out https://docs.python.org/3/library/functools.html#functools.cached_property

        # WARNING: LEGAL_FILENAME_CHARS is used in hash fn to generate unique ids. DO NOT ALTER! May cause 
        # transcription of files already transcribed!
        LEGAL_FILENAME_CHARS = r'[a-zA-Z0-9]'

        def only_legal_chars(s: str) -> str:
            return ''.join([char for char in s if re.match(LEGAL_FILENAME_CHARS, char)])

        pod_title = only_legal_chars(self.podcast.title)
        ep_title = only_legal_chars(self.episode_title)
        ep_guid = only_legal_chars(self.guid)

        return pod_title[:17] + ep_title[:17] + ep_guid[-32:]


def connect_to_db(flask_app, db_uri="postgresql:///podcasts", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)