import os

from flask import Flask
from peewee import SqliteDatabase

app = Flask(__name__)

app.config.from_mapping(
    SECRET_KEY='dev'
)

app.config['HTTP_BASIC_AUTH_USERNAME'] = os.environ.get("HTTP_BASIC_AUTH_USERNAME", default='buckets')
app.config['HTTP_BASIC_AUTH_PASSWORD'] = os.environ.get("HTTP_BASIC_AUTH_PASSWORD", default='dev')

db_file = os.environ.get("DB_FILE", default='/home/jared/Source/bread-bucket/app/db.buckets')
app.logger.warn("Connecting to SQLite Database File: %s", db_file)
db = SqliteDatabase(db_file)


from . import views
app.register_blueprint(views.views)
