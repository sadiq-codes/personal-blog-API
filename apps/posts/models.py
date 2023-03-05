from sqlalchemy.orm import relationship

from apps import db
from datetime import datetime
from flask import url_for, current_app
from sqlalchemy import event
from slugify import slugify
from markdown import markdown
import bleach
from ..helpers import show_image


class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(50), nullable=False)
    slug = db.Column(db.String(), index=True, unique=True)
    description = db.Column(db.String())
    post = relationship('Post', backref=db.backref('category'), lazy='dynamic')

    def __repr__(self):
        return f'Category {self.name}'

    def format_to_json(self, add_post=True):
        category = {
            'url': url_for('api.get_post_by_category', category_slug=self.slug),
            "slug": self.slug,
            'name': self.name,
            'description': self.description,
        }
        if add_post:
            category['post'] = [p.title for p in self.post]
        return category


@event.listens_for(Category.name, 'set')
def category_slugify(target, value, oldvalue, initiator):
    target.slug = slugify(value)


class Tag(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(50), nullable=False)
    slug = db.Column(db.String(), index=True, unique=True)
    description = db.Column(db.String())

    def __repr__(self):
        return f'Tag {self.name}'

    # @property
    # def tag_posts(self):
    #     return Post.query.join(Tag, Tag.tags_id == Post.tags_id) \
    #         .filter(Tag.follower_id == self.id)

    def format_to_json(self, add_post=True):
        tag = {
            'url': url_for('api.get_post_by_tags', tag_slug=self.slug),
            "slug": self.slug,
            'name': self.name,
            'description': self.description,
        }
        if add_post:
            tag['post'] = [post.title for post in self.posts]
        return tag


tag = db.Table('tag',
               db.Column('tags_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True),
               db.Column('posts_id', db.Integer, db.ForeignKey('posts.id'), primary_key=True),
               keep_existing=True,
               )


@event.listens_for(Tag.name, 'set')
def tag_slugify(target, value, oldvalue, initiator):
    target.slug = slugify(value)


# def get_file(filename):
#     return [current_app.config["UPLOADED_PHOTOS_DEST"], secure_filename(filename)]

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)

    slug = db.Column(db.String(), index=True, unique=True)
    title = db.Column(db.String, index=True)
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    image = db.Column(db.String())

    publish_on = db.Column(db.DateTime, index=True, default=datetime.utcnow, nullable=False)
    updated_on = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    tags = db.relationship('Tag', secondary=tag, backref=db.backref('posts', lazy='dynamic'),
                           lazy='dynamic')
    comments = db.relationship('Comment', backref='post', lazy='dynamic')
    likes = db.relationship('Like', backref='post', lazy='dynamic')

    def __repr__(self):
        return f'Post {self.title}'

    def format_to_json(self):
        post = {
            'url': url_for('api.post_detail', post_slug=self.slug),
            'title': self.title,
            'slug': self.slug,
            'body': self.body,
            'body_html': self.body_html,
            'category': self.category.format_to_json(add_post=False) if self.category is not None else "",
            # 'image': url_for('api.get_file', filename=self.image) if self.image is not None else "",
            'image': self.image if self.image is not None else "",
            'created_on': self.publish_on,
            'update_on': self.updated_on,
            'author_url': url_for('api.profile', user_id=self.author_id),
            'author': self.author.username,
            'tags': [t.format_to_json(add_post=False) for t in self.tags],
            'comments': [c.format_to_json() for c in self.comments],
            'comments_count': self.comments.count(),
            'likes_count': self.likes.count(),
        }

        return post


@event.listens_for(Post.title, 'set')
def post_slugify(target, value, oldvalue, initiator):
    target.slug = slugify(value)


@event.listens_for(Post.body, 'set')
def on_changed_body(target, value, oldvalue, initiator):
    allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                    'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                    'h1', 'h2', 'h3', 'p']
    target.body_html = bleach.linkify(bleach.clean(
        markdown(value, output_format='html'),
        tags=allowed_tags, strip=True))

# @event.listens_for(Post.image, 'set')
# def post_slugify(target, value, oldvalue, initiator):
#     target.image_url = show_image(value)
