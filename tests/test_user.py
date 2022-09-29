import unittest
from apps import create_app, db
from apps.users.models import User


class UserModelTest(unittest.TestCase):

    def setUp(self):
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
       
    def setDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_set(self):
        user = User(hash_password="coding")
        self.assertTrue(user.password is not None)

    def test_passwords_hash_match(self):
        user = User(hash_password="codi")
        self.assertFalse(user.password == User.check_password(user, "coding"))



