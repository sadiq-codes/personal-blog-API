from random import randint
from sqlalchemy.exc import IntegrityError
from faker import Faker
from apps import db
from apps.users.models import User
from apps.posts.models import Post, Tag, Category
from apps.comments.models import Comment


def tags():
    tag = ['javascript', 'react', 'django', 'python', 'typescript', 'html', 'css']
    fake = Faker()
    for i in range(len(tag)):
        t = Tag(name=tag[i],
                description=fake.sentence())
        db.session.add(t)
    db.session.commit()


def posts(count=100):
    fake = Faker()
    user = User.query.filter_by(email="bbkrmuhdsaddiq@gmail.com").first()
    tag_count = Tag.query.all()
    category = Category.query.filter_by(name="tech").first()
    for i in range(count):
        tag = fake.random_sample(elements=tag_count, length=3)
        p = Post(body=fake.text(),
                 title=fake.sentence(),
                 publish_on=fake.past_date(),
                 author=user,
                 tags=tag,
                 category=category)
        db.session.add(p)
    db.session.commit()


def comments(count=100):
    fake = Faker()
    post_count = Post.query.count()
    user = User.query.filter_by(email="bbkrmuhdsaddiq@gmail.com").first()
    for i in range(count):
        p = Post.query.offset(randint(0, post_count - 1)).first()
        c = Comment(body=fake.text(),
                    created_on=fake.past_date(),
                    post=p,
                    author=user)
        db.session.add(c)
    db.session.commit()


def add_category():
    c = Category(name="tech", description="tech related posts")
    db.session.add(c)
    db.session.commit()


def update_post():
    user = User.query.filter_by(email="bbkrmuhdsaddiq@gmail.com").first()
    post = Post.query.all()
    for p in post:
        p.author = user
