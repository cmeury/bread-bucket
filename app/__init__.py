import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.pool import NullPool
from flask_login import LoginManager

db = SQLAlchemy(engine_options={
    'echo': False,
    'echo_pool': False,
    'poolclass': NullPool
})

login_manager = LoginManager()


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
login_manager.init_app(app)

from . import views
app.register_blueprint(views.views)
login_manager.login_view = '/login'

