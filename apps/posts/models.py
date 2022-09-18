from apps import db
from datetime import datetime
from sqlalchemy import event
from slugify import slugify


class Tag(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(50), nullable=False)
    slug = db.Column(db.String(), index=True, unique=True)
    description = db.Column(db.String())

    def __repr__(self):
        return f'Tag {self.name}'


tag = db.Table('tag',
               db.Column('tags_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True),
               db.Column('posts_id', db.Integer, db.ForeignKey('posts.id'), primary_key=True),
               keep_existing=True,
               )


@event.listens_for(Tag.name, 'set')
def tag_slugify(target, value, oldvalue, initiator):
    target.slug = slugify(value)


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    slug = db.Column(db.String(), index=True, unique=True)
    title = db.Column(db.String, index=True)
    body = db.Column(db.Text)

    publish_on = db.Column(db.DateTime, index=True, default=datetime.utcnow, nullable=False)
    updated_on = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    tags = db.relationship('Tag', secondary=tag, backref=db.backref('posts', lazy='dynamic'),
                           lazy='dynamic')

    def __repr__(self):
        return f'Post {self.title}'


@event.listens_for(Post.title, 'set')
def post_slugify(target, value, oldvalue, initiator):
    target.slug = slugify(value)
