import unittest
from apps import create_app, db
from apps.users.models import User


class UserModelTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.user = User(email="sadiq@gmail.com", hash_password="coding")

    def setDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_set(self):
        self.assertTrue(self.user.password is not None)

    def test_passwords_hash_match(self):
       self.assertFalse(self.user.password == User.check_password(self.user, "coding"))



