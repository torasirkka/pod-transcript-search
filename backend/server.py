"""Server for pod transcript app."""
from flask import Flask, jsonify, render_template, request, flash, session, redirect
import model
import parse_rss
import urllib
import podcastparser

app = Flask(__name__)

# GET /api/podcasts -> list of all podcasts
# POST /api/podcasts -> create podcast from rss feed
# GET /api/podcasts/<id> -> one podcast
# GET /api/podcasts/<id>/episodes -> episodes in podcast
# GET /api/podcasts/<id>/episodes/search -> search episodes in podcast


@app.route("/api/podcasts")
def get_podcasts_json():
    """Return a JSON response with all podcasts in db."""

    pods = model.Podcast.query.all()
    podcasts = []
    for pod in pods:
        podcast = {
            "id": pod.podcast_id,
            "title": pod.title,
            "description": pod.description,
            "img_url": pod.img_url,
        }
        podcasts.append(podcast)

    return jsonify(podcasts)


@app.route("/api/podcasts/<int:podcast_id>")
def get_specific_podcast_json(podcast_id):
    """Return a JSON response details about one podcasts in db."""
    pod = model.Podcast.query.get(podcast_id)
    podcast = {
        "id": pod.podcast_id,
        "title": pod.title,
        "description": pod.description,
        "img_url": pod.img_url,
    }

    return jsonify(podcast)


@app.route("/api/podcasts/<int:podcast_id>/search")
def get_podcast_episodes(podcast_id):
    """Return a JSON response details about one podcasts in db."""

    pod = model.Podcast.query.get(podcast_id)
    query = request.args.get("q", "")

    # create list of dicts with episode information:
    episodes = []
    for ep in pod.episodes:
        ep_data = {
            "id": ep.episode_id,
            "title": ep.episode_title,
            "description": ep.description,
            "published": ep.release_date,
            "mp3_url": ep.mp3_url,
            "transcript": ep.transcript,
            "status": ep.status,
            "guid": ep.guid,
        }

        if not query:
            episodes.append(ep_data)
        else:
            if query in ep_data["description"]:
                episodes.append(ep_data)
    return jsonify(episodes)


@app.route("/api/podcasts", methods=["POST"])
def add_podcast():
    """Parse feed url. If successful: commit podcast and episodes to db. Return podcast"""

    rss_url = request.get_json()

    if not rss_url:
        return "Empty or outdated url."

    try:
        new_podcast = parse_rss.to_podcasts_and_episodes(rss_url)

    except urllib.error.HTTPError as err:
        return f"{err}\n Uups, I can't seem to download podcast data from {rss_url}."

    except urllib.error.URLError:
        return f"{err}\n Uups, I can't seem to download podcast data from {rss_url}."

    except podcastparser.FeedParseError as err:
        return f"{err} Could not parse the info in the url."

    # check if podcast already in db:
    titles_in_db = [pod.title for pod in model.Podcast.query.all()]
    if new_podcast.title in titles_in_db:
        return f"{new_podcast.title} already exists in library!"

    # Validate that the content is podcast-related. Valid podcasts must have >= 10%
    # non-empty mp3_urls:
    mp3_urls = [episode.mp3_url for episode in new_podcast.episodes]
    if mp3_urls.count(None) / len(mp3_urls) >= 0.1:
        return f"{new_podcast.title} is not a valid podcast feed."
    else:
        model.db.session.add(new_podcast)
        model.db.session.commit()
        # return f"{new_podcast.title} successfully added!"  # return new podcast obj as JSON

        episode_ids = [ep.episode_id for ep in new_podcast.episodes]
        podcast = {
            "id": new_podcast.podcast_id,
            "title": new_podcast.title,
            "description": new_podcast.description,
            "img_url": new_podcast.img_url,
            "episode_ids": episode_ids,
        }
        return podcast


if __name__ == "__main__":
    model.connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
