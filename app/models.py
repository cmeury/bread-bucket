from sqlalchemy import func

from app import db


class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    closed = db.Column(db.Integer)
    account = db.relationship('Transaction', backref='account', lazy=True)

    def __repr__(self):
        return '<Account %r>' % self.name


class Transaction(db.Model):
    __tablename__ = 'account_transaction'
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer)
    memo = db.Column(db.Text)
    notes = db.Column(db.Text)
    posted = db.Column(db.DateTime(timezone=True), default=func.now())
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)

    def __repr__(self):
        return '<Transaction %r>' % self.id
