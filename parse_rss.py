"""Python script that parses data from RSS files and adds it to a database"""

from typing import Tuple, Dict, Optional, Any
#from podsearch.model import Episode
import podcastparser
import urllib.request


def get_rss_data(feed_url: str) -> Optional[Dict]:
    """Retrieve podcast data from feedurl."""

    return podcastparser.parse(feed_url, urllib.request.urlopen(feed_url))

def parse_podcasts_data(rss_data: Dict[Any,Any]) -> Tuple[str]:
    """Parse out the data needed to instantiate a podcast object."""
    title = rss_data['title']
    img_url = rss_data['cover_url']
    description = rss_data['description']

    return (title, img_url, description)

def parse_episode_data(rss_episode_data: Dict[Any,Any]) -> Tuple[str]:
    """Parse out data needed to instantiate an episode object."""
    title = rss_episode_data['title']
    description_html = rss_episode_data['description']
    release_date = rss_episode_data['published']
    mp3_url = rss_episode_data['enclosures'][2]['url']
    guid = rss_episode_data['guid']

    return (title, description, release_date, mp3_url, guid)

