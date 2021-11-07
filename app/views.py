from flask import request, render_template, redirect, Blueprint, current_app
from flask_httpauth import HTTPBasicAuth
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from sqlalchemy import exc
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from app.forms import TransactionEntryForm
from app.models import Transaction, Account

DEFAULT_LIMIT = 10

views = Blueprint('views', __name__)
limiter = Limiter(current_app, key_func=get_remote_address)
auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username, password):
    cfg_username = current_app.config['HTTP_BASIC_AUTH_USERNAME']
    cfg_password = current_app.config['HTTP_BASIC_AUTH_PASSWORD']
    cfg_password_hash = generate_password_hash(cfg_password)
    if username == cfg_username and check_password_hash(cfg_password_hash, password):
        return username


@views.app_template_filter()
def currency_format(value):
    value = float(value)
    return "$ {:,.2f}".format(value)


@views.errorhandler(exc.SQLAlchemyError)
def handle_db_exceptions(error):
    current_app.logger.error(error)
    db.session.rollback()


@auth.error_handler
def auth_error(status):
    return render_template("access_denied.html", status=status)


# --- ROUTES ---------------------------------------------------------------------------------------------------------
@views.route('/')
@limiter.limit("10/minute")
def root():
    return redirect("/transaction")


@views.route('/about')
@limiter.limit("10/minute")
def about():
    return render_template('about.html')


@views.route('/transactions/<account_id>')
@auth.login_required
@limiter.limit("10/minute")
def transactions_for(account_id=None):
    limit = request.args.get('limit') or DEFAULT_LIMIT
    tx = Transaction.query.filter_by(account_id=account_id).order_by(Transaction.posted.desc()).limit(limit)
    account_name = Account.query.filter_by(id=account_id).first().name
    return render_template('transactions.html', tx=tx, account=account_name, limit=limit)


@views.route('/transactions')
@auth.login_required
@limiter.limit("10/minute")
def transactions():
    limit = request.args.get('limit') or DEFAULT_LIMIT

    # get non-closed accounts
    accounts = Account.query.filter_by(closed=0).order_by('name')

    tx = Transaction.query.order_by(Transaction.posted.desc()).limit(limit)
    return render_template('transactions.html', tx=tx, limit=limit, accounts=accounts)


@views.route('/transaction', methods=['GET', 'POST'])
@auth.login_required
@limiter.limit("10/minute")
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
        amount = form.amount.data * 100  # amounts are stored in cents in the database
        tx = Transaction(amount=amount, account=account,
                         memo=form.memo.data, notes=form.notes.data)
        db.session.add(tx)
        db.session.commit()
        current_app.logger.warn('New Transaction Inserted: Account=%s, Amount=%d', account.name, amount)
        return redirect('/transaction/success')

    return render_template('transaction.html', form=form)


@views.route('/transaction/success')
@auth.login_required
@limiter.limit("10/minute")
def transaction_success():
    return render_template('transaction-success.html')
