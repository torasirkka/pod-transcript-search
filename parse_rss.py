"""Python script that parses data from RSS files and adds it to a database"""

from typing import Tuple, Dict, List, Optional, Any
import podcastparser
import urllib.request
import datetime
import re
import uuid
import model
import os

def parse_rss_data(feed_url: str) -> Optional[Dict]:
    """Retrieve podcast data from feedurl."""
    #to-do: remember to add try-except before calling this fn! To check that the feed url is valid
    return podcastparser.parse(feed_url, urllib.request.urlopen(feed_url))

def create_podcast_obj(rss_data: Dict[Any,Any]) -> model.Podcast:
    """Create a podcast object."""
    pod = model.Podcast()
    pod.podcast_id = uuid.uuid4()
    pod.title = parse_podcast_title(rss_data)
    pod.img_url = parse_podcast_img_url(rss_data)
    pod.description = parse_podcast_description(rss_data)

    return pod

def create_episode_obj(rss_episode_data: Dict[Any,Any]) -> Dict[str,str]:
    """Parse out data needed to instantiate an episode object."""

    episode = model.Episode()
    episode.episode_id = uuid.uuid4()
    episode.episode_title = parse_episode_title(rss_episode_data)
    episode.description = parse_episode_description(rss_episode_data)
    episode.release_date = parse_episode_release_date(rss_episode_data)
    #To-do: the location of the mp3 is not constant! Find solution!
    episode.mp3_url = parse_episode_mp3_url(rss_episode_data)
    #To-do: add guid and hash map value
    # episode.guid = rss_episode_data['']

    return episode

def parse_podcast_title(rss_data: Dict[Any,Any])-> Optional[str]:
    """Retrieve the title of a podcast from an rss XML file object."""
    return rss_data['title']

def parse_podcast_img_url(rss_data: Dict[Any,Any])-> Optional[str]:
    """Retrieve the podcasts image url."""
    return rss_data['cover_url']

def parse_podcast_description(rss_data: Dict[Any,Any])-> Optional[str]:
    """Retrieve the podcasts image url."""
    return rss_data['description']

def parse_episode_title(episode: Dict[Any,Any])-> Optional[str]:
    """Retrieve the podcasts description."""
    return episode['title']

def parse_episode_description(episode: Dict[Any,Any])-> Optional[str]:
    """Retrieve the podcasts description."""
    return episode.get('description','')

def parse_episode_release_date(episode: Dict[Any,Any])-> datetime.date:
    """Retrieve the podcasts release date."""
    return datetime.date.fromtimestamp(episode.get('published', 0))

def parse_episode_mp3_url(episode: Dict[Any,Any])-> Optional[str]:
    """Retrieve the podcasts release date."""

    id_pattern = 'audio/mpeg'
    for enclosure in episode['enclosures']:
        if re.match(id_pattern, enclosure['mime_type']):
            return enclosure['url']
    
    return None


def to_podcasts_and_episodes(feed_url: str)-> model.Podcast:
    """Return podcast and episode objects parsed from feed_url."""
    # try:
    rss_data = parse_rss_data(podcastparser.normalize_feed_url(feed_url))
    # except error:
    #     print('Oh no, could not read the RSS feed. Is the link valid?')
    #     #To-do: implement redirect to homepage/ don't update state.
    # try:
    podcast =  create_podcast_obj(rss_data)
    # except KeyError:
    #     print('Could not parse RSS. Please check that the RSS-link is valid.')
    episodes = []
    for episode in rss_data['episodes']:
        # Create episode object & link it to a podcast as intended by Flask-alchemy:
        podcast.episodes.append(create_episode_obj(episode))

    return podcast


#---------------------------------------
# For testing to parse 100 RSS feeds:

def testing_feed_links():
    file = open("RSS_feeds.txt")
    
    mp3_urls = []
    for rss_url in file:
        try:
            rss_data = parse_rss_data(rss_url)
            for episode in rss_data['episodes']:
                print(parse_podcast_title(rss_data))
                print(type(episode))
                enclosures = episode['enclosures']
                for enc in enclosures:
                    if enc['mime_type'] :
                        mp3_urls.append(enc['url'])
                    print(enc['url'])
                    print(f'\n')

        except urllib.error.HTTPError:
            print(rss_url)
            continue

        except podcastparser.FeedParseError:
            print(rss_url)
            continue

        except urllib.error.URLError:
            print(rss_url)
            continue
        
    return mp3_urls




if __name__ == "__main__":
    from server import app
    import server
    os.system("dropdb podcasts")
    os.system("createdb podcasts")

    model.connect_to_db(server.app)
    model.db.create_all()
    podcast = to_podcasts_and_episodes('https://feeds.simplecast.com/pvzhyDQn')
    objects_list = [podcast] + podcast.episodes
    # print(objects_list)
    model.db.session.add_all(objects_list)
    model.db.session.commit()
    print('success!')

