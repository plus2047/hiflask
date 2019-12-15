import flask

app = flask.Flask(__name__)
app.secret_key = "this is a secret key."

user = {
    "username": "plus",
    "bio": "A boy who loves anime."
}

animes = [
    {"name": "Angle Beats!", "year": "2006"},
    {"name": "Fate / Heaven's Feeling", "year": "2019"},
    {"name": "Your name.", "year": "2016"}
]


@app.context_processor
def inject_foo():
    return {"foo": "I am foo."}


@app.template_global()
def bar():
    return "I am bar."


@app.template_filter()
def toTitle(s):
    return s.title()


@app.route("/index")
def index():
    return flask.render_template("index.html", user=user, animes=animes)


@app.route("/watchlist")
def watchlist():
    return flask.render_template("watchlist.html", user=user, animes=animes)


@app.route("/flash")
def flash():
    flask.flash("flash something...")
    return flask.redirect("index")