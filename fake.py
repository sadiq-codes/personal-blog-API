from random import randint
from sqlalchemy.exc import IntegrityError
from faker import Faker
from apps import db
from apps.users.models import User
from apps.posts.models import Post, Tag, Category
from apps.comments.models import Comment


# def users(count=100):
#     fake = Faker()
#     i = 0
#     while i < count:
#         u = User(email=fake.email(),
#                  username=fake.user_name(),
#                  password='password',
#                  confirmed=True,
#                  name=fake.name(),
#                  location=fake.city(),
#                  about_me=fake.text(),
#                  member_since=fake.past_date())
#         db.session.add(u)
#         try:
#             db.session.commit()
#             i += 1
#         except IntegrityError:
#             db.session.rollback()

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
    for i in range(count):
        tag = fake.random_sample(elements=tag_count, length=3)
        p = Post(body=fake.text(),
                 title=fake.sentence(),
                 publish_on=fake.past_date(),
                 author=user,
                 tags=tag)
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


# def reply(count=100):
#     fake = Faker()
#     post_count = Post.query.count()
#     user = User.query.filter_by(email="bbkrmuhdsaddiq@gmail.com").first()
#     for i in range(count):
#         p = Post.query.offset(randint(0, post_count - 1)).first()
#         c = Comment(body=fake.text(),
#                     created_on=fake.past_date(),
#                     post=p,
#                     author=user)
#         db.session.add(c)
#     db.session.commit()

def add_categories():
    c = Category(name="Tech", description="tech related posts")
    db.session.add(c)
    post = Post.query.all()
    category = Category.query.filter_by(name="Tech").first()
    for p in post:
        p.category = category

    db.session.commit()
