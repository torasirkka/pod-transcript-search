"CRUD operations"
from uuid import uuid4
from model import db, Podcast, connect_to_db


def add_podcast(title: str, description: str, img_url: str) -> Podcast:
    """Add a new podcast to the podcasts table."""

    podcast = Podcast()
    podcast.title = title
    podcast.description = description
    podcast.img_url = img_url

    return podcast

def get_all_podcasts():
    """Return list of all podcast objects."""

    return Podcast.query.all()


#-----------------------------------------------

# Legacy code:
def first_16(s:str)-> str:
    """Return the 16 first characters of string.
    
    If the string contains less tha on equal to 16 chars: return string.
    This fn is used in hash fn, do not change!"""

    if len(s) <= 16:
        return s
    else:
        return s[:16]

def last_32(s:str)-> str:
    """Return the 32 last characters of a string.
    
    If the string contains less than or equal to 32 chars: return string.
    This fn is used in hash fn, do not change!"""

    if len(s) <= 32:
        return s
    else:
        return s[-32:]

def only_legal_chars(s:str)-> str:
    """Filter the string s on legal characters. Return the filtered string."""
    s = [char for char in s if re.match(LEGAL_FILENAME_CHARS, char)]
    return ''.join(s)

def create_transcript_cache_id(episode: model.Episode)-> str:
    """Hash fn that generates a unique id for a podcast episode. 
    
    This is the filename for the transcriptions cache stored used as back-up.
    It consists of the first 15 chars of the podcast and episode titles + the
    32 last episode uuid chars"""
    
    pod_title = first_16(only_legal_chars(episode.podcast.title))
    ep_title = first_16(only_legal_chars(episode.episode_title))
    ep_guid = last_32(only_legal_chars(episode.guid))
    cache_id = pod_title + ep_title + ep_guid
    return cache_id


    def testing_feed_links():
    file = open("RSS_feeds.txt")
    
    mp3_urls = []
    uuids = []
    for rss_url in file:
        try:
            rss_data = download_and_parse_rss(podcastparser.normalize_feed_url(rss_url))
            for episode in rss_data['episodes']:
                uuids.append(episode['guid'])
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
        
    return (mp3_urls, uuids)



