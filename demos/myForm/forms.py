from flask_wtf import FlaskForm
from wtforms import Form, StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, ValidationError
from flask_wtf.file import FileRequired, FileField
from flask_ckeditor import CKEditorField

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired(), Length(8, 128)])
    remember = BooleanField("Remember me")
    submit = SubmitField("Log in")


class FortyTwoForm(FlaskForm):
    answer = IntegerField('The Number')
    submit = SubmitField()

    def validate_answer(self, field):
        if field.data != 42:
            raise ValidationError('Must be 42.')


class UploadFrom(FlaskForm):
    file = FileField("Upload Files", validators=[FileRequired()])
    submit = SubmitField()


class RichTextForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(1, 64)])
    body = CKEditorField("Body", validators=[DataRequired()])
    submit = SubmitField("Publish")
