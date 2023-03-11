from wtforms import (
    StringField,
    PasswordField,
    BooleanField,
    IntegerField,
    DateField,
    TextAreaField,
)

from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Length, EqualTo, Email, Regexp ,Optional
import email_validator
from flask_login import current_user
from wtforms import ValidationError,validators
from models import User


class login_form(FlaskForm):
    email = StringField(validators=[InputRequired(), Email(), Length(1, 64)])
    name = StringField(
        validators=[Optional()]
    )


class register_form(FlaskForm):
    name = StringField(
        validators=[
            InputRequired(),
            Length(3, 20, message="Please provide a valid name"),
        ]
    )
    email = StringField(validators=[InputRequired(), Email(), Length(1, 64)])

    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError("Email already registered!")

    # def validate_uname(self, uname):
    #     if User.query.filter_by(username=username.data).first():
    #         raise ValidationError("Username already taken!")