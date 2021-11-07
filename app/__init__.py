import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.pool import NullPool

db = SQLAlchemy(engine_options={'echo': True, 'echo_pool': True, 'poolclass': NullPool})


def create_app():
    app = Flask(__name__)

    app.config.from_mapping(
        SECRET_KEY='dev'
    )

    app.config['DB_FILE'] = os.environ.get("DB_FILE", default='/app/db.buckets')
    app.logger.warn("Connecting to SQLite Database File: %s", app.config['DB_FILE'])
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + app.config['DB_FILE']
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from . import views
    app.register_blueprint(views.views)

    return app
