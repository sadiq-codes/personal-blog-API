import os

from flask_migrate import Migrate
from apps import create_app, db
from apps import users
from apps import posts
from apps import comments
from routes import api
import fake

app = create_app(os.getenv('FLASK_CONFIG'))
migrate = Migrate(app, db)
app.register_blueprint(api, url_prefix="/api/v1/")
User = users.models.User
Post = posts.models.Post
Tag = posts.models.Tag
Comment = comments.models.Comment


@app.route("/", methods=["GET"])
def home():
    return "Hello welcome to my blog api"


@app.shell_context_processor
def create_shell_context():
    return {"db": db, "User": User, "fake": fake,
            "Post": Post, "Tag": Tag, "Comment": Comment}


@app.cli.command("createsuperuser")
def create_user():
    user = User(username=os.environ.get("BLOG_USERNAME"), \
                email=os.environ.get("BLOG_ADMIN"),
                admin=bool(os.environ.get("IS_BLOG_ADMIN")))
    user.hash_password = os.environ.get("BLOG_PASSWORD")
    db.session.add(user)
    db.session.commit()
    print("user created successfully")


@app.cli.command()
def test():
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
