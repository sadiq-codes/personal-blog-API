from flask import Flask
from settings import config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db = SQLAlchemy()
migrate = Migrate()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    #register libraries
    db.init_app(app)
    migrate.init_app(app, db)


    #register blueprints
    from .users import users
    app.register_blueprint(users)

    from .api import api
    app.register_blueprint(api, url_prefix="/api/v1")

    return app
