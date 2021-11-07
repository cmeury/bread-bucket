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

    app.config['HTTP_BASIC_AUTH_USERNAME'] = os.environ.get("HTTP_BASIC_AUTH_USERNAME", default='buckets')
    app.config['HTTP_BASIC_AUTH_PASSWORD'] = os.environ.get("HTTP_BASIC_AUTH_PASSWORD", default='dev')

    db_file = os.environ.get("DB_FILE", default='/app/db.buckets')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_file
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.logger.warn("Connecting to SQLite Database File: %s", db_file)
    db.init_app(app)

    from . import views
    app.register_blueprint(views.views)

    return app
