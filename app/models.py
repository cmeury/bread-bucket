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
        return (Transaction
                .query
                .where(
                    or_(((account is not None) and (Transaction.account_id==account))
                        ,(account is None)))
                .order_by(Transaction.posted.desc())
                .limit(limit))

    @staticmethod
    def memo_contains(limit, text):
        return (Transaction
                .query
                .where(Transaction.memo.contains(text))
                .group_by(Transaction.memo)
                .order_by(func.count(Transaction.id).desc())
                .limit(limit)
                .all())

    def __repr__(self):
        return '<Transaction %r>' % self.id

class BucketGroup(db.Model):
    __tablename__ = 'bucket_group'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    ranking = Column(Text)
    bucket = relationship('Bucket', backref='bucket_group', lazy=True)

    @staticmethod
    def get_all_buckets(session):
        return (session.query(BucketGroup, Bucket)
                .where(BucketGroup.id==Bucket.group_id and Bucket.kicked==0)
                .order_by(BucketGroup.ranking, Bucket.ranking)
                .all())

class Bucket(db.Model):
    __tablename__ = 'bucket'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    balance = Column(Integer)
    kicked = Column(Integer)
    ranking = Column(Text)
    group_id = Column(Integer, ForeignKey('bucket_group.id'), nullable=False)

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
