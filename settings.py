import os
from pathlib import Path

BASE_DIR = Path(__file__).parent


class Config:
    BLOG_ADMIN = os.environ.get('BLOG_ADMIN')
    SECRET_KEY = os.environ.get('SECRET_KEY')
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_ACCESS_TOKEN_EXPIRES = os.environ.get('JWT_ACCESS_TOKEN_EXPIRES') or 3600
    JWT_COOKIE_SECURE = True
    JWT_TOKEN_LOCATION = ["headers", "cookies"]

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
