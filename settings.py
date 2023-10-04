import os
from pathlib import Path
from dotenv import load_dotenv
from datetime import timedelta, datetime

load_dotenv()

BASE_DIR = Path(__file__).parent



class Config:
    BLOG_ADMIN = os.environ.get('BLOG_ADMIN')
    SECRET_KEY = os.urandom(24)
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_ACCESS_TOKEN_EXPIRES = os.environ.get('JWT_ACCESS_TOKEN_EXPIRES') or 60 * 60 * 24 * 7
    JWT_COOKIE_SECURE = True
    JWT_TOKEN_LOCATION = ["headers", "cookies"]
    UPLOADED_PHOTOS_DEST = os.path.join(str(BASE_DIR / 'static/img'))
    S3_BUCKET_NAME = os.environ.get("S3_BUCKET_NAME")
    S3_LOCATION = os.environ.get("S3_LOCATION")
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
    UNSPLASH_API_KEY = os.environ.get("UNSPLASH_ACCESS_KEY")
    UNSPLASH_API_URL = "https://api.unsplash.com/photos/random?query=technology"
    SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')


    @staticmethod
    def init_app(app):
        pass


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + str(BASE_DIR / 'test.db')


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL')


class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('PROD_DATABASE_URL')


config = {
    'testing': TestConfig,
    'development': DevConfig,
    'production': ProdConfig
}
