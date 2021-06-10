"""Server for pod transcript app."""
from flask import Flask, jsonify, render_template, request, flash, session, redirect
import model
import parse_rss
import urllib
import podcastparser

app = Flask(__name__)

@app.route("/")
def homepage():
    """View homepage."""

    return render_template("homepage.html")

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

@app.route("/api/add_podcast", methods = ["POST"])
def add_podcast():
    """Parse feed url. If successful: commit podcast and episodes to db.""" 
    rss_url = request.get_json()
    print(f'**************************\nthe rss:{rss_url}, {type(rss_url)}')
    if not rss_url:
        return f"Url is empty"
    try:
        new_podcast = parse_rss.to_podcasts_and_episodes(rss_url)
        # check if podcast already in db:
        titles_in_db = [pod.title for pod in model.Podcast.query.all()]
        #print(titles_in_db)
        if new_podcast.title in model.Podcast.query.all():
            return f"{new_podcast.title} already exists in library!"
            # TO_DO HOW TO GET THE ID OF THE PODCAST?
            #return redirect('/api/podcasts/{}')
        else:
            model.db.session.add(new_podcast)
            model.db.session.commit()
            return f"{new_podcast.title} successfully added!"
            #return redirect('/api/podcasts/{new_podcast.podcast_id}') 

    except urllib.error.HTTPError as err:
        return f"{err}\n Uups, I can't seem to download podcast data from {rss_url}."

    except urllib.error.URLError:
        return f"{err}\n Uups, I can't seem to download podcast data from {rss_url}."

    except podcastparser.FeedParseError as err:
        return f"{err} Could not parse the info in the url."

if __name__ == "__main__":
    model.connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
