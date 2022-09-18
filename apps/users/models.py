from apps import db
from flask_jwt_extended import create_access_token, get_jwt_identity
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.orm import relationship


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, index=True)
    name = db.Column(db.String(50), nullable=True, index=True)
    email = db.Column(db.String(80), unique=True)
    is_admin = db.Column(db.Boolean, default=False)
    password = db.Column(db.String(200))
    post = relationship('Post', backref=db.backref('author'), lazy='dynamic')
    comments = db.relationship('Comment', backref=db.backref('author'), lazy='dynamic')
    likes = db.relationship('Like', backref=db.backref("author"), lazy='dynamic')

    def __repr__(self):
        return f'User {self.username}'

    @property
    def hash_password(self):
        raise AttributeError("password cannot be read")

    @hash_password.setter
    def hash_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def generate_auth_token(self, user):
        return create_access_token(identity=user)

    @property
    def validate_auth_token(token):
        return get_jwt_identity()
