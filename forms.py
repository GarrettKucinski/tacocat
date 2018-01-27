from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, TextAreaField, BooleanField)
from wtforms.validators import (DataRequired, ValidationError,
                                Email, Length, EqualTo)
from models import User


def email_exists(form, field):
    if User.select().where(User.email == field.data).exists():
        raise ValidationError("User with that name already exists")


class RegisterForm(FlaskForm):
    email = StringField(
        u'Email',
        validators=[
            Email(),
            DataRequired(),
            email_exists
        ]
    )
    password = PasswordField(
        u'Password',
        validators=[
            DataRequired(),
            Length(min=4),
            EqualTo('password2', message="You're passwords must match!")
        ]
    )
    password2 = PasswordField(
        u'Confirm Password',
        validators=[
            DataRequired()
        ]
    )


class TacoCatForm(FlaskForm):
    protein = StringField(u"Protein")
    shell = StringField(u"Shell")
    cheese = BooleanField(u"Cheese?")
    extras = TextAreaField(u"Extras")


class LoginForm(FlaskForm):
    email = StringField(u"Email", validators=[Email(), DataRequired()])
    password = PasswordField(u"Password", validators=[DataRequired()])
