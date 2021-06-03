"""Server for pod transcript app."""
from flask import Flask, render_template, request, flash, session, redirect
from jinja2 import StrictUndefined

from model import connect_to_db
import crud

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


@app.route("/")
def homepage():
    """View homepage."""

    podcasts = crud.get_all_podcasts()
    pod_titles = []
    for pod in podcasts:
        pod_titles.append(pod.title)

    return render_template("homepage.html", podcasts = pod_titles)



if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
