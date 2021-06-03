"""Script to seed database."""

import os
import json
from datetime import datetime
import uuid

import crud
import model
import server

os.system("dropdb podcasts")
os.system("createdb podcasts")

model.connect_to_db(server.app)
model.db.create_all()

def example_data_using_crud():
    """Create test data using the CRUD functions.

    Create five podcasts and three episodes per podcast."""
    podcasts = []
    episodes = []
    for i in range(5):
        pod = crud.add_podcast(
            f"Podcast title {i}",
            f"Test podcast description{i}",
            img_url="www.test_img_url{i}.com",
            )
        podcasts.append(pod)

        for i in range(3):
            episode = pod.add_episode(
                f"Episode0{i}",
                f'Interesting content * {i}'
            )
            episodes.append(episode)

    model.db.session.add_all(podcasts + episodes)
    model.db.session.commit()

example_data_using_crud()


def example_data():
    """Create some test data by instantiating class objects directly."""
    podcast_id = str(uuid.uuid4())
    test_pod = Podcast(
        podcast_id=podcast_id,
        description="Talkshow about racism",
        title="Yo, Is This Racist?",
        img_url="www.test_img_url.com",
    )

    test_episode = test_pod.add_episode(
        'Episode2','interesting content')

    db.session.add(test_pod)
    db.session.add(test_episode)
    db.session.commit()

    example_data
