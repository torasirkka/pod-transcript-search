"CRUD operations"
from typing import Dict, Any, Optional
from datetime import datetime
from model import db, Podcast, Episode, connect_to_db


def add_podcast(title: str, description: str, img_url: str) -> Podcast:
    """Add a new podcast to the podcasts table."""

    podcast = Podcast(description, title, img_url)
    db.session.add(podcast)

    return podcast


if __name__ == "__main__":
    from server import app

    connect_to_db(app)
    db.create_all()

    test_pod = add_podcast(
        description="Talkshow about racism",
        title="Yo, Is This Racist?",
        img_url="www.test_img_url.com",
    )

    test_episode = test_pod.add_episode(
        'Episode2','interesting content')

    db.session.commit()
