from flask import Flask, flash, redirect, url_for, render_template, abort
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy import Model

from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired

import os
import click

app = Flask(__name__)

K_SQLALCHEMY_DATABASE_URI = "SQLALCHEMY_DATABASE_URI"
V_SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///" + os.path.join(app.root_path, "data.sqlite3"))
K_SQLALCHEMY_TRACK_MODIFICATIONS = "SQLALCHEMY_TRACK_MODIFICATIONS"
V_SECRET_KEY = "QWERASDFZXCV"

app.config[K_SQLALCHEMY_DATABASE_URI] = V_SQLALCHEMY_DATABASE_URI
app.config[K_SQLALCHEMY_TRACK_MODIFICATIONS] = False
app.secret_key = V_SECRET_KEY

db = SQLAlchemy(app)


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)

    def __repr__(self):
        return '<Note %r>' % self.body
    
    def to_string(self):
        return '<note id:{}, body:{}>'.format(self.id, self.body)


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    phone = db.Column(db.String(32))
    articles = db.relationship('Article', backref="singer")


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), index=True)
    body = db.Column(db.Text)
    author_id = db.Column(db.Integer, db.ForeignKey("author.id"))


class NewNoteForm(FlaskForm):
    body = TextAreaField("Body")
    submit = SubmitField("Save")


class DeleteNoteForm(FlaskForm):
    submit = SubmitField("Delete")


@app.route('/new_note', methods=['GET', 'POST'])
def new_note():
    new_note_form = NewNoteForm()
    del_note_form = DeleteNoteForm()

    if new_note_form.validate_on_submit():
        db.session.add(Note(body=new_note_form.body.data))
        db.session.commit()
        flash("Your note is saved.")
        return redirect(url_for('new_note'))
    else:
        return render_template(
            'new_note.html',
            new_note_form=new_note_form,
            del_note_form=del_note_form,
            notes=Note.query.all())


@app.route('/edit_note/<int:note_id>', methods=["GET", "POST"])
def edit_note(note_id):
    form = NewNoteForm()
    note = Note.query.get(note_id)
    if form.validate_on_submit():
        note.body = form.body.data
        db.session.commit()
        flash("Your note is updated.")
        return redirect(url_for("new_note"))
    else:
        form.body.data = note.body
        return render_template("edit.html", form=form)


@app.route('/delete_note/<int:note_id>', methods=("POST",))
def delete_note(note_id):
    form = DeleteNoteForm()
    if form.validate_on_submit():
        note = Note.query.get(note_id)
        db.session.delete(note)
        db.session.commit()
        return redirect(url_for("new_note"))
    else:
        abort(400)


# ===== modify db in command line =====
@app.cli.command()
def initdb():
    db.create_all()
    print("Initialized database.")


@app.cli.command()
def test_create():
    note1 = Note(body="Remenber him.")
    note2 = Note(body="Brave Shine")
    note3 = Note(body="We Always believe.")

    db.session.add(note1)
    db.session.add_all((note2, note3))
    db.session.commit()

    foo = Author(name="Foo")
    spam = Article(title="Spam")
    ham = Article(title="ham")

    db.session.add_all((foo, spam, ham))
    db.session.commit()


@app.cli.command()
def test_print_db():
    for record in Note.query.all():
        print(record.to_string())


@app.cli.command()
@click.argument("record_id")
def test_get_by_id(record_id):
    print(Note.query.get(int(record_id)).to_string())


@app.cli.command()
@click.argument("record_id", type=int)
def test_delete_by_id(record_id):
    db.session.delete(Note.query.get(record_id))
    db.session.commit()


@app.cli.command()
@click.argument("keyword")
def test_get_by_keyword(keyword):
    print([q.to_string() for q in Note.query.filter(Note.body.like('%%%s%%' % keyword))])


@app.cli.command()
@click.argument("record_id", type=int)
@click.argument("body", type=str)
def test_modify_body(record_id, body):
    obj = Note.query.get(record_id)
    obj.body = body
    db.session.commit()


@app.shell_context_processor
def make_shell_context():
    return {"db": db, "Note": Note}
