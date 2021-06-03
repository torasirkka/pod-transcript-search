"""Models for podcast transcript search app."""

from typing import Optional, Dict, Any
from datetime import datetime
import uuid

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON

db = SQLAlchemy()


def connect_to_db(flask_app, db_uri="postgresql:///podcasts", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


class Podcast(db.Model):
    """A podcast."""

    __tablename__ = "podcasts"

    podcast_id = db.Column(db.String(36), primary_key=True, nullable=True)
    title = db.Column(db.String(100))
    img_url = db.Column(db.String(200))
    description = db.Column(db.Text())

    episodes = db.relationship("Episode", backref="podcast")

    def __repr__(self):
        return f"<Podcast podcast_id={self.podcast_id} title={self.title}>"

    def __init__(self, title: str, description: str, img_url: str):
        """Custom init method that generates and attaches a UUID primary key to the object being instantiated."""
        podcast_id = str(uuid.uuid4())
        podcast = super().__init__(
            podcast_id=podcast_id, title=title, description=description, img_url=img_url
        )
        return podcast

    def add_episode(self,
        title: str,
        description:str,
        release_date:datetime=datetime.today(),
        transcript: Optional[Dict[Any,Any]]={},
        status: str=""):
        """Method to add a new episode to the episodes table"""
        
        episode = Episode(self.podcast_id, title, description, release_date, transcript, status)
        db.session.add(episode)
        return episode

class Episode(db.Model):
    """A podcast episode."""

    __tablename__ = "episodes"

    episode_id = db.Column(db.String(36), primary_key=True)
    podcast_id = db.Column(
        db.String(36), db.ForeignKey("podcasts.podcast_id"), nullable=False
    )
    episode_title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text())
    release_date = db.Column(db.DateTime())
    transcript = db.Column(db.JSON)
    status = db.Column(db.String(10))

    def __init__(
        self,
        podcast_id: str,
        title: str,
        description: str,
        release_date: datetime,
        transcript: Optional[Dict[Any, Any]],
        status: str,
    ):
        """Custom init method that generates and attaches a UUID primary key to the object being instantiated."""
        episode_id = str(uuid.uuid4())
        episode = super().__init__(
            episode_id=episode_id,
            podcast_id=podcast_id,
            episode_title=title,
            description=description,
            release_date=release_date,
            transcript=transcript,
            status=status,
        )
        return episode

    def __repr__(self):
        return (
            f"<Episode episode_id={self.episode_id} episode_title={self.episode_title}>"
        )


if __name__ == "__main__":
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)
