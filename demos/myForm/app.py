import flask
import forms
import uuid
import os
from flask_ckeditor import CKEditor

app = flask.Flask(__name__)
app.secret_key = "this is a secret key."
ckeditor = CKEditor(app)


@app.route("/index")
def index():
    return flask.render_template("index.html")

# ================
# ===== from =====
# ================

@app.route('/pure_html_form', methods=['GET', 'POST'])
def pure_html_form():
    if flask.request.method == 'POST':
        username = flask.request.form.get('username')
        flask.flash('Welcome home, %s' % username)
        return flask.redirect(flask.url_for('index'))
    return flask.render_template('pure_html.html')


@app.route("/basic_form", methods=['GET', 'POST'])
def basic_form():
    form = forms.LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        flask.flash('Welcome home, %s!' % username)
        return flask.redirect(flask.url_for('index'))
    return flask.render_template('basic.html', form=form)


# =======================
# ===== netdisk app =====
# =======================

FILENAMES_KEY = "FILENAMES"
MAX_CONTENT_LENGTH_KEY = "MAX_CONTENT_LENGTH"
UPLOAD_PATH_KEY = "UPLOAD_PATH"

MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5M
UPLOAD_PATH = os.path.join(app.root_path, 'uploads')

app.config[MAX_CONTENT_LENGTH_KEY] = MAX_CONTENT_LENGTH
app.config[UPLOAD_PATH_KEY] = UPLOAD_PATH


@app.route('/netdisk', methods=["GET", "POST"])
def netdisk():
    form = forms.UploadFrom()
    if FILENAMES_KEY not in flask.session:
        flask.session[FILENAMES_KEY] = {}
    if form.validate_on_submit():
        f = form.file.data
        random_name = uuid.uuid4().hex
        f.save(os.path.join(app.config[UPLOAD_PATH_KEY], random_name))
        flask.session[FILENAMES_KEY][random_name] = f.filename
        flask.session.modified = True
        return flask.redirect(flask.url_for('netdisk'))
    return flask.render_template('netdisk.html', files=flask.session[FILENAMES_KEY], form=form)


@app.route('/uploads/<path:filename>')
def uploads(filename):
    return flask.send_from_directory(app.config[UPLOAD_PATH_KEY], filename)


@app.route('/netdisk_clear')
def netdisk_clear():
    flask.session[FILENAMES_KEY] = {}
    return flask.redirect(flask.url_for('netdisk'))

# =======================
# ===== text editor =====
# =======================

K_CKEDITOR_LANGUAGE = "CKEDITOR_LANGUAGE"

app.config[K_CKEDITOR_LANGUAGE] = "zh-cn"


@app.route('/rich_text_editor', methods=['GET', 'POST'])
def rich_text_editor():
    form = forms.RichTextForm()
    if form.validate_on_submit():
        print("===== title =====")
        print(form.title.data)
        print("===== body =====")
        print(form.body.data)
        return flask.redirect(flask.url_for("rich_text_editor"))
    return flask.render_template('ckeditor.html', form=form)
