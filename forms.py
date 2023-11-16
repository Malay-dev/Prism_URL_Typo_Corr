from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


class UrlForm(FlaskForm):
    url = StringField("Enter URL")
    submit = SubmitField()
