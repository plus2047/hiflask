# -*- coding: utf-8 -*-

import flask

app = flask.Flask(__name__)

# the minimal Flask application
@app.route("/")
def index():
    return "HelloWorld!!!"


# bind multiple URL for one view function, hi, hello
@app.route("/hello")
@app.route("/hi")
def say_hello():
    return "<h1> Hello World!!! </hi>"


# dynamic route, URL variable default
@app.route("/hello/<name>")
def greet(name):
    return "<h1> Hello %s !!! </h1>" % name

# custom flask cli command
@app.cli.command()
def hello():
    print("HelloWorld!!!")
