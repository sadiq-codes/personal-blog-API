import os
from pathlib import Path

BASE_DIR = Path(__file__).parent


class Config:
    BLOG_ADMIN = os.environ.get('BLOG_ADMIN')
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or 'sqlite:///' + str(BASE_DIR / 'test.db')


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
                              "postgresql://postgresflask:54321qaz@localhost:5432/flaskblog"


class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('PROD_DATABASE_URL') or 'sqlite:///' + str(BASE_DIR / 'prod.db')


config = {
    'testing': TestConfig,
    'development': DevConfig,
    'production': ProdConfig
}
