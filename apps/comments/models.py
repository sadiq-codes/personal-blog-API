from datetime import datetime
from sqlalchemy import UniqueConstraint

from flask import url_for

from .. import db


class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    created_on = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    reply_comment_id = db.Column(db.Integer, db.ForeignKey('comments.id'), nullable=True)
    replies = db.relationship('Comment', backref=db.backref("reply", remote_side=[id]))
    disabled = db.Column(db.Boolean)

    def format_to_json(self):
        comment = {
            'id': self.id,
            'body': self.body,
            'author_id': 1,
            'created_on': self.created_on,
            # 'user_url': url_for('api.profile', id=self.author_id) if self.author_id else "",
            'reply_comment_id': self.reply_comment_id,
            'post_slug': self.post.slug,
        }
        return comment


class Like(db.Model):
    __tablename__ = 'likes'

    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))

    def like(self):
        post = self.post

    def has_liked(self):
        if self.post.likes:
            pass
