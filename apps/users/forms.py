from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, BooleanField
from wtforms.validators import Length, InputRequired, EqualTo, Regexp
from wtforms import ValidationError

from .models import User


class LoginForm(FlaskForm):
    email = EmailField('email', validators=[InputRequired(), Length(1, 80)])
    password = PasswordField('password', validators=[InputRequired()])
    remember_me = BooleanField("remember me", default=False)


class SignUp(FlaskForm):
    username = StringField('username',
                           validators=[InputRequired(), Length(5, 50),
                                       Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                              'Usernames must have only letters, numbers, dots or '
                                              'underscores'),
                                       ]
                           )
    name = StringField('name', validators=[InputRequired(), Length(5, 80)])
    email = EmailField('email', validators=[InputRequired(), Length(5, 80)])
    password = PasswordField('password 1', validators=[InputRequired()])
    password2 = PasswordField('Confirm password', validators=[InputRequired(),
                                                              EqualTo('password2', message='Passwords miss match.')])

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already existed.')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first().lower():
            raise ValidationError('Email already registered.')
