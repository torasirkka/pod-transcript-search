"""Script to seed database."""

import os
import json
from datetime import datetime
from typing import Tuple
import parse_rss
import model
import server

os.system("dropdb podcasts")
os.system("createdb podcasts")

model.connect_to_db(server.app)
model.db.create_all()

file = open("RSS_feeds.txt")

podcasts_to_add = []
episodes_to_add = []
for rss_url in file:
    rss_data = parse_rss.retrieve_rss_data(rss_url)
    try:
        podcast =  parse_rss.create_podcast_obj(rss_data)
        podcasts_to_add.append(podcast)
    except KeyError:
        print('Could not parse RSS. Please check that the RSS-link is valid.')
 #   for episode in rss_data['episodes'][:2]:
 #       print(episode)
  #      episode_data = parse_rss.parse_episode_data(episode)
  #      print(episode_data)
   #     print()

model.db.session.add_all(podcasts_to_add)
model.db.session.commit()
print('success!')





# def example_data_using_crud():
#     """Create test data using the CRUD functions.

#     Create five podcasts and three episodes per podcast."""
#     podcasts = []
#     episodes = []
#     for i in range(5):
#         pod = crud.add_podcast(
#             f"Podcast title {i}",
#             f"Test podcast description{i}",
#             img_url="www.test_img_url{i}.com",
#             )
#         podcasts.append(pod)

#         for i in range(3):
#             episode = pod.add_episode(
#                 f"Episode0{i}",
#                 f'Interesting content * {i}'
#             )
#             episodes.append(episode)

#     model.db.session.add_all(podcasts + episodes)
#     model.db.session.commit()

# def example_data():
#     """Create some test data by instantiating class objects directly."""
#     test_pod = Podcast(
#         description="Talkshow about racism",
#         title="Yo, Is This Racist?",
#         img_url="www.test_img_url.com",
#     )

#     test_episode = test_pod.add_episode(
#         'Episode2','interesting content')

#     def add_episode(self,
#         title: str,
#         description:str,
#         release_date:Optional[datetime]=None,
#         transcript: Optional[Dict[Any,Any]]={},
#         status: str=""):
#         """Method to add a new episode to the episodes table"""
        
#         episode = Episode(self.podcast_id, title, description, release_date, transcript, status)
#         return episode

#     db.session.add(test_pod)
#     db.session.add(test_episode)
#     db.session.commit()



if __name__ == "__main__":
    from server import app

#    connect_to_db(app)
#    db.create_all()
    #example_data()
    