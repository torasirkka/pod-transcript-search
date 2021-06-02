"""Script to seed database"""

import os
import json
from random import choice, randint
from datetime import datetime

import crud
import model
import server

os.system('dropdb podcasts')
os.system('createdb podcasts')

model.connect_to_db(server.app)
model.db.create_all()

"""Script to seed database."""

import os
import json
from datetime import datetime

import crud
import model
import server

os.system("dropdb podcasts")
os.system("createdb podcasts")

model.connect_to_db(server.app)
model.db.create_all()


def example_data():
    """Create some sample data."""
    import uuid
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