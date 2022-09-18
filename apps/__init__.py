from flask import Flask
from settings import config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# from flask_login import LoginManager
from flask_jwt_extended import JWTManager
# from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()
# login_manager = LoginManager()
jwt = JWTManager()
# cors = CORS()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # register libraries
    db.init_app(app)
    migrate.init_app(app, db)
    # login_manager.init_app(app)
    jwt.init_app(app)
    # cors.init_app(app, resources={r"/api/*": {"origins": "*"}})

    # register blueprints
    from .users import users
    app.register_blueprint(users)

    from .posts import posts
    app.register_blueprint(posts)

    from .api import api
    app.register_blueprint(api, url_prefix="/api/v1")

    return app
