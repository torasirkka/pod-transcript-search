"CRUD operations"
from typing import Dict, List
from datetime import datetime
from model import db, Podcast, Episode, connect_to_db
import uuid

def add_new_podcast(title:str, description:str, img_url:str):
    """Add a new podcast to the podcast table."""

    podcast_id = str(uuid.uuid4())
    podcast = Podcast(podcast_id=podcast_id,
                        description=description,
                        title=title,
                        img_url=img_url)

    db.session.add(podcast)
    db.session.commit()

    return podcast

def add_new_episode(podcast_id: str, 
                    title: str, 
                    description: str, 
                    release_date: datetime = '',
                    transcript: str = {},
                    status: str = '',
                    ):
    """Add a new episode to the episode table."""

    episode_id = str(uuid.uuid4())
    episode = Episode(episode_id = episode_id,
                        podcast_id = podcast_id,
                        episode_title = title,
                        description = description,
                        release_date = release_date,
                        transcript = transcript,
                        status = status)

    db.session.add(episode)
    db.session.commit()

    return episode

if __name__=='__main__':
    from server import app
    connect_to_db(app)

    # test_pod = add_new_podcast(description='Talkshow about racism',
    #                     title= 'Yo, Is This Racist?',
    #                     img_url='www.test_img_url.com')
    
    # podcast_id = test_pod.podcast_id
    
    # test_episode = Episode(episode_id=str(uuid.uuid4()),
    #                     podcast_id = podcast_id,
    #                     episode_title = 'Episode2')