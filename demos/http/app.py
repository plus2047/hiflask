# -*- coding: utf-8 -*-
"""
    :author: Grey Li (李辉)
    :url: http://greyli.com
    :copyright: © 2018 Grey Li
    :license: MIT, see LICENSE for more details.
"""
import os
import urllib
import urllib.parse
import jinja2
import jinja2.utils
import flask

app = flask.Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'secret string')


# get name value from query string and cookie
@app.route('/')
@app.route('/hello')
def hello():
    name = flask.request.args.get("name")
    name = name if name else flask.request.cookies.get("name", "Human")
    return "<h1> Hello, %s </h1>" % name + \
        ("<p>[Authorized]</p>" if "logged_in" in flask.session else "<p>[Unauthorized]</p>")


# return error response
@app.route('/brew/<drink>')
def teapot(drink):
    if drink == 'coffee':
        flask.abort(418)
    else:
        return 'A drop of tea.'


# return response with different formats
@app.route('/note', defaults={'content_type': 'text'})
@app.route('/note/<content_type>')
def note(content_type):
    content_type = content_type.lower()
    if content_type == 'text':
        body = '''Note
to: Peter
from: Jane
heading: Reminder
body: Don't forget the party!
'''
        response = flask.make_response(body)
        response.mimetype = 'text/plain'
    elif content_type == 'html':
        body = '''<!DOCTYPE html>
<html>
<head></head>
<body>
  <h1>Note</h1>
  <p>to: Peter</p>
  <p>from: Jane</p>
  <p>heading: Reminder</p>
  <p>body: <strong>Don't forget the party!</strong></p>
</body>
</html>
'''
        response = flask.make_response(body)
        response.mimetype = 'text/html'
    elif content_type == 'xml':
        body = '''<?xml version="1.0" encoding="UTF-8"?>
<note>
  <to>Peter</to>
  <from>Jane</from>
  <heading>Reminder</heading>
  <body>Don't forget the party!</body>
</note>
'''
        response = flask.make_response(body)
        response.mimetype = 'application/xml'
    elif content_type == 'json':
        body = {"note": {
            "to": "Peter",
            "from": "Jane",
            "heading": "Remider",
            "body": "Don't forget the party!"
        }
        }
        response = flask.jsonify(body)
        # equal to:
        # response = make_response(json.dumps(body))
        # response.mimetype = "application/json"
    else:
        flask.abort(400)
    return response


# set cookie
@app.route('/set/<name>')
def set_cookie(name):
    response = flask.make_response(flask.redirect(flask.url_for('hello')))
    response.set_cookie('name', name)
    return response


# log in user
@app.route('/login')
def login():
    flask.session['logged_in'] = True
    return flask.redirect(flask.url_for('hello'))


# protect view
@app.route('/admin')
def admin():
    if 'logged_in' not in flask.session:
        flask.abort(403)
    return 'Welcome to admin page.'


# log out user
@app.route('/logout')
def logout():
    if 'logged_in' in flask.session:
        flask.session.pop('logged_in')
    return flask.redirect(flask.url_for('hello'))


# AJAX
@app.route('/post')
def show_post():
    post_body = jinja2.utils.generate_lorem_ipsum(n=2)
    return '''
<h1>A very long post</h1>
<div class="body">%s</div>
<button id="load">Load More</button>
<script src="https://code.jquery.com/jquery-3.3.1.min.js"></script>
<script type="text/javascript">
$(function() {
    $('#load').click(function() {
        $.ajax({
            url: '/more',
            type: 'get',
            success: function(data){
                $('.body').append(data);
            }
        })
    })
})
</script>''' % post_body


@app.route('/more')
def load_post():
    return jinja2.utils.generate_lorem_ipsum(n=1)
