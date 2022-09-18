from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, DataRequired
from wtforms import StringField, TextAreaField, FieldList


class TagForm(FlaskForm):
    name = StringField('name', validators=[InputRequired()] )
    description = TextAreaField('description, name', validators=[InputRequired()])


class PostForm(FlaskForm):
    title = StringField('title', validators=[InputRequired()])
    body = TextAreaField('what do you want to share ?', validators=[InputRequired()])
    tags = FieldList('tags')

