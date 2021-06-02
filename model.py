"""Models for podcast transcript search app."""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON

db = SQLAlchemy()


def connect_to_db(flask_app, db_uri='postgresql:///podcasts', echo=True):
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    flask_app.config['SQLALCHEMY_ECHO'] = echo
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = flask_app
    db.init_app(flask_app)

    print('Connected to the db!')


class Podcast(db.Model):
    """A podcast."""

    __tablename__ = 'podcasts'

    podcast_id = db.Column(db.String(36), primary_key=True, nullable=True)
    title = db.Column(db.String(100))
    img_url = db.Column(db.String(200))
    description = db.Column(db.Text())

    episodes = db.relationship('Episode', backref='podcast')

    def __repr__(self):
        return f'<Podcast podcast_id={self.podcast_id} title={self.title}>'


class Episode(db.Model):
    """A podcast episode."""

    __tablename__ = 'episodes'

    episode_id = db.Column(db.String(36), primary_key=True)
    podcast_id = db.Column(db.String(36), db.ForeignKey('podcasts.podcast_id'))
    episode_title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text())
    release_date = db.Column(db.DateTime())
    transcript = db.Column(db.JSON)
    status = db.Column(db.String(10))

    def __repr__(self):
        return f'<Episode episode_id={self.episode_id} episode_title={self.episode_title}>'   


if __name__ == '__main__':
    from server import app
    import uuid


    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)
    podcast_id = str(uuid.uuid4())
    test_pod = Podcast(podcast_id=podcast_id,
                        description='Talkshow about racism',
                        title= 'Yo, Is This Racist?',
                        img_url='www.test_img_url.com')

    test_episode = Episode(episode_id=str(uuid.uuid4()),
                        podcast_id = podcast_id,
                        episode_title = 'Episode2')

    db.session.add(test_pod)
    db.session.add(test_episode)
    db.session.commit()
    