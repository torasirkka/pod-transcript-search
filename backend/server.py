"""Server for pod transcript app."""
from flask import Flask, render_template, request, flash, session, redirect
import model

app = Flask(__name__)

@app.route("/")
def homepage():
    """View homepage."""

    return render_template("homepage.html")

@app.route("/api/all-podcasts.json")
def get_cards_json():
    """Return a JSON response with all podcasts in DB."""

    podcasts = model.Podcast.query.all()
    podcasts_list = []

    for p in podcasts:
        podcasts_list.append({"title": p.title})

    return {"podcasts": podcast_list}


if __name__ == "__main__":
    model.connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
