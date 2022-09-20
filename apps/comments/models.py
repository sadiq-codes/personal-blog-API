from datetime import datetime
from flask import url_for

from .. import db


class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    created_on = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    disabled = db.Column(db.Boolean)

    def format_to_json(self):
        comment = {
            'body': self.body,
            'created_on': self.created_on,
            'user_url': url_for('api.profile', id=self.author_i) if self.author_id else "",
        }
        return comment


class Like(db.Model):
    __tablename__ = 'likes'

    id = db.Column(db.Integer, primary_key=True)
    num_likes = db.Column(db.Integer)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))

    def like(self):
        post = self.post

    def has_liked(self):
        if self.post.likes:
            pass



