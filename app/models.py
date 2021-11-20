from sqlalchemy import func, Column, Integer, String, DateTime, Text, ForeignKey, or_
from sqlalchemy.orm import relationship

from app import db

class Account(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True, nullable=False)
    closed = Column(Integer)
    account = relationship('Transaction', backref='account', lazy=True)

    @staticmethod
    def by_id(id):
        return Account.query.filter_by(id=id).first()

    @staticmethod
    def name_by_id(id):
        return Account.by_id(id).name

    @staticmethod
    def active_accounts():
        return (Account
                .query
                .outerjoin(Transaction)
                .group_by(Account.id)
                .where(Account.closed==0)
                .order_by(func.count(Transaction.id).desc(), Account.name))

    def __repr__(self):
        return '<Account %r>' % self.name


class Transaction(db.Model):
    __tablename__ = 'account_transaction'
    id = Column(Integer, primary_key=True)
    amount = Column(Integer)
    memo = Column(Text)
    notes = Column(Text)
    posted = Column(DateTime(timezone=True), default=func.now())
    account_id = Column(Integer, ForeignKey('account.id'), nullable=False)

    @staticmethod
    def top(limit, account=None):
        tx = (Transaction
                .query
                .where(
                    or_(((account is not None) and (Transaction.account_id==account))
                        ,(account is None)))
                .order_by(Transaction.posted.desc())
                .limit(limit))
        print(tx)
        return tx

    def __repr__(self):
        return '<Transaction %r>' % self.id

class User():
    authenticated = False
    id = None
    password_hash = None

    def __init__(self, id, password_hash):
        self.id = id
        self.password_hash = password_hash

    def is_active(self):
        return True

    def get_id(self):
        return self.id

    def is_authenticated(self):
        return self.authenticated

    def is_anonymous(self):
        return False
