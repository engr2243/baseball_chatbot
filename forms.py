from wtforms import (
    StringField,
)

from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Length, Email


class login_form(FlaskForm):
    email = StringField(validators=[InputRequired(), Email(), Length(1, 64)])