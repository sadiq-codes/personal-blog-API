from apps import db
from datetime import datetime
from flask import url_for
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

    def format_to_json(self):
        tag = {
            'url': url_for('api.get_post_by_tag', tag_slug=self.slug),
            'name': self.name,
            'description': self.description,
            # 'author_url': url_for('api.get_user', id=self.author_id),
            'post': [post.name for post in self.posts],
            "tags_url": []
        }

        return tag


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
    comments = db.relationship('Comment', backref='posts', lazy='dynamic')
    likes = db.relationship('Like', backref='posts', lazy='dynamic')

    def __repr__(self):
        return f'Post {self.title}'

    def format_to_json(self):
        post = {
            'url': url_for('api.post_detail', slug=self.slug),
            'title': self.title,
            'body': self.body,
            'created_on': self.publish_on,
            'update_on': self.updated_on,
            'author_url': url_for('api.profile', id=self.author_id),
            'tags': [tag.name for tag in self.tags],
            "tags_url": []
        }

        return post


@event.listens_for(Post.title, 'set')
def post_slugify(target, value, oldvalue, initiator):
    target.slug = slugify(value)
