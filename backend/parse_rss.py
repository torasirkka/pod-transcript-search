"""Python script that parses data from RSS files and adds it to a database"""

from typing import Tuple, Dict, List, Optional, Any
import podcastparser
import urllib.request
import datetime
import re
import model
import os


def download_and_parse_rss(feed_url: str) -> Optional[Dict]:
    """Retrieve podcast data from feedurl."""
    #to-do: remember to add try-except before calling this fn! To check that the feed url is valid
    return podcastparser.parse(feed_url, urllib.request.urlopen(feed_url))

def create_podcast_obj(rss_data: Dict[Any,Any]) -> model.Podcast:
    """Create a podcast object."""
    podcast = model.Podcast()
    if 'title' in rss_data:        
        podcast.title = rss_data['title']
    if 'cover_url' in rss_data:
        podcast.img_url = rss_data['cover_url']
    if 'description' in rss_data:
        podcast.description = rss_data['description']

        for episode in rss_data['episodes']:
            ep_obj = create_episode_obj(episode)
            podcast.episodes.append(ep_obj)
            
    return podcast

def create_episode_obj(rss_episode_data: Dict) -> model.Episode:
    """Create an episode object."""
    episode = model.Episode()
    if 'title' in rss_episode_data:
        episode.episode_title = rss_episode_data['title']
    if 'description' in rss_episode_data:
        episode.description = rss_episode_data['description']
    if 'published' in rss_episode_data:
        episode.release_date = datetime.date.fromtimestamp(rss_episode_data['published'])
    if 'enclosures' in rss_episode_data:
        episode.mp3_url = parse_episode_mp3_url(rss_episode_data['enclosures'])
    if 'guid' in rss_episode_data:
        episode.guid = rss_episode_data['guid']

    return episode

def parse_episode_mp3_url(enclosures: List[Dict]) -> Optional[str]:
    """Retrieve the podcasts release date."""

    id_pattern = r'^audio/'
    for enc in enclosures:
        if re.match(id_pattern, enc['mime_type']):
            return enc['url']
    
    return None

def to_podcasts_and_episodes(feed_url: str)-> model.Podcast:
    """Return podcast and episode objects parsed from feed_url."""
    try:
        rss_data = download_and_parse_rss(podcastparser.normalize_feed_url(feed_url))
    
    except urllib.error.HTTPError as err:
        print(f'{err} when trying to download {rss_url}')
        raise

    except urllib.error.URLError:
        print(f'{err} when trying to download {rss_url}')
        raise

    except podcastparser.FeedParseError as err:
        print(f'{err} when trying to parse {rss_url}')
        raise

    return create_podcast_obj(rss_data)

if __name__ == "__main__":
    from server import app
    import server
    os.system("dropdb podcasts")
    os.system("createdb podcasts")

    model.connect_to_db(server.app)
    model.db.create_all()
    file = open("RSS_feeds.txt")
    i = 0
    for rss_url in file:
        podcast = to_podcasts_and_episodes(rss_url)
        objects_list = [podcast] + podcast.episodes
        print(objects_list)
        model.db.session.add_all(objects_list)
        print('*'*40)
        print('')
        print(f'RSS feed nr {i}')
        i += 0
    model.db.session.commit()
    print('success!')

