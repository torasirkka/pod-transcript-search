"""Models for podcast transcript search app."""

import re
from flask_sqlalchemy import SQLAlchemy, BaseQuery
from sqlalchemy_searchable import SearchQueryMixin
from sqlalchemy_utils.types import TSVectorType
from sqlalchemy_searchable import make_searchable

db = SQLAlchemy()
make_searchable(db.metadata)


class Podcast(db.Model):
    """A podcast."""

    __tablename__ = "podcasts"

    podcast_id = db.Column(
        db.Integer, primary_key=True, nullable=False, autoincrement=True
    )
    title = db.Column(db.String)
    img_url = db.Column(db.String)
    description = db.Column(db.Text)

    episodes = db.relationship("Episode", backref="podcast")

    def __repr__(self):
        return f"<Podcast podcast_id={self.podcast_id} title={self.title}>"


class Episode(db.Model):
    """A podcast episode."""

    __tablename__ = "episodes"

    episode_id = db.Column(
        db.Integer, primary_key=True, nullable=False, autoincrement=True
    )
    podcast_id = db.Column(db.Integer(), db.ForeignKey("podcasts.podcast_id"))
    episode_title = db.Column(db.String)
    description = db.Column(db.Text)
    release_date = db.Column(db.DateTime)
    mp3_url = db.Column(db.String)
    transcript = db.Column(db.Text)
    status = db.Column(db.String)
    guid = db.Column(db.String)

    searchepisode = db.relationship("SearchEpisode", backref="episode")

    def __repr__(self):
        return (
            f"<Episode episode_id={self.episode_id} episode_title={self.episode_title}>"
        )


class SearchEpisodeQuery(BaseQuery, SearchQueryMixin):
    pass


class SearchEpisode(db.Model):
    """The information to be searched in an episode."""

    query_class = SearchEpisodeQuery
    __tablename__ = "searchepisodes"

    searchepisodes_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    episode_id = db.Column(
        db.Integer, db.ForeignKey("episodes.episode_id"), unique=True, nullable=False
    )
    transcript = db.Column(db.Text)
    description = db.Column(db.Text)
    title = db.Column(db.Text)
    searchepisodes_vector = db.Column(
        TSVectorType("transcript", "description", "title")
    )

    def __repr__(self):
        return f"<Searchepisode searchepisodes_id={self.searchepisodes_id}>"


def cache_id(ep: Episode) -> str:
    """Hash fn that generates a unique cache id for a podcast episode.

    This is the filename for the transcriptions cache stored used as back-up.
    It consists of the first 15 chars of the podcast and episode titles + the
    32 last episode uuid chars.
    """

    # TODO: check out https://docs.python.org/3/library/functools.html#functools.cached_property

    # WARNING: LEGAL_FILENAME_CHARS is used in hash fn to generate unique ids. DO NOT ALTER! May cause
    # transcription of files already transcribed!
    LEGAL_FILENAME_CHARS = r"[a-zA-Z0-9]"

    def only_legal_chars(s: str) -> str:
        return "".join([char for char in s if re.match(LEGAL_FILENAME_CHARS, char)])

    pod_title = only_legal_chars(ep.podcast.title)
    ep_title = only_legal_chars(ep.episode_title)
    ep_guid = only_legal_chars(ep.guid)

    return pod_title[:17] + ep_title[:17] + ep_guid[-32:]


def connect_to_db(flask_app, db_uri="postgresql:///podcasts"):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = False
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


db.configure_mappers()

if __name__ == "__main__":
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)