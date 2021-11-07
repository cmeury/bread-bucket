import os
from datetime import datetime, timezone

from flask import request, render_template, redirect, Blueprint, current_app
from sqlalchemy import exc

from app import db
from app.forms import TransactionEntryForm
from app.models import Transaction, Account

DEFAULT_LIMIT = 10
views = Blueprint('views', __name__)


@views.app_template_filter()
def currency_format(value):
    value = float(value)
    return "$ {:,.2f}".format(value)


@views.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@views.route('/transactions/<account_id>')
def transactions_for(account_id=None):
    limit = request.args.get('limit') or DEFAULT_LIMIT
    tx = Transaction.query.filter_by(account_id=account_id).order_by(Transaction.posted.desc()).limit(limit)
    account_name = Account.query.filter_by(id=account_id).first().name
    return render_template('transactions.html', tx=tx, account=account_name, limit=limit)


@views.route('/transactions')
def transactions():
    limit = request.args.get('limit') or DEFAULT_LIMIT
    tx = Transaction.query.order_by(Transaction.posted.desc()).limit(limit)
    return render_template('transactions.html', tx=tx, limit=limit)


@views.errorhandler(exc.SQLAlchemyError)
def handle_db_exceptions(error):
    current_app.logger.error(error)
    db.session.rollback()


@views.route('/transaction', methods=['GET', 'POST'])
def new_transaction():

    # instantiate new entry form
    form = TransactionEntryForm()

    # get non-closed accounts
    accounts = Account.query.filter_by(closed=0).order_by('name')

    # populate drop-down with accounts
    form.account.choices = [(acc.id, acc.name) for acc in accounts]

    # processing a validated POST request
    if form.validate_on_submit():
        account = Account.query.filter_by(id=form.account.data).first()
        now = datetime.now()
        now.replace(tzinfo=timezone.utc)
        tx = Transaction(amount=form.amount.data, account=account,
                         memo=form.memo.data, notes=form.notes.data)

        db.session.add(tx)
        db.session.commit()

        account_name = account.name
        current_app.logger.warn('New Transaction Inserted: Account=%s, Amount=%d', account_name, form.amount.data)

        # touching the sqlite file, otherwise synology sync will not pick up the changes..
        os.close(os.open(current_app.config['DB_FILE'], os.O_CREAT))

        return redirect('/transaction/success')

    return render_template('transaction.html', form=form)


@views.route('/transaction/success')
def transaction_success():
    return render_template('transaction-success.html')
