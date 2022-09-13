from apps import db
from werkzeug.security import check_password_hash, generate_password_hash


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(80), unique=True)
    is_admin = db.Column(db.Boolean, default=False)
    password = db.Column(db.String(200))

    def __repr__(self):
        return f'User {self.username}'

    @property
    def hashed_password(self):
        raise AttributeError("password cannot be read")

    @hashed_password.setter
    def hashed_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)



