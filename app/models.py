from peewee import Model, IntegerField, CharField, DateTimeField, datetime, ForeignKeyField
from datetime import datetime

from app import db

class BaseModel(Model):
    class Meta:
        database = db

class FormattedDateTimeField(DateTimeField):
    def db_value(self, value):
        return value

    def python_value(self, value):
        return datetime.strptime(value[0:19], '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')


class Account(BaseModel):
    id = IntegerField(primary_key=True)
    name = CharField()
    closed = IntegerField()

    def __repr__(self):
        return '<Account %r>' % self.name

class Transaction(BaseModel):
    id = IntegerField(primary_key=True)
    amount = IntegerField()
    memo = CharField()
    notes = CharField()
    posted = FormattedDateTimeField(default=datetime.now)
    account = ForeignKeyField(Account, column_name='account_id', backref='transactions')

    def __repr__(self):
        return '<Transaction %r>' % self.id

    class Meta:
        table_name = 'account_transaction'
