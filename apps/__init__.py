from flask import Flask, Blueprint
from settings import config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# from flask_login import LoginManager
from flask_jwt_extended import JWTManager
from flask_uploads import IMAGES, UploadSet, configure_uploads
from . import errors
from celery import Celery

from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()
# login_manager = LoginManager()
jwt = JWTManager()


cors = CORS()
photos = UploadSet("photos", IMAGES)


def create_app(config_name):
    app = Flask(__name__, static_folder='static')
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # register libraries
    db.init_app(app)
    migrate.init_app(app, db)
    celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)

    jwt.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}})
    configure_uploads(app, photos)


    # # register blueprints
    # from .users import models, views
    # from .posts import models, views
    return app
