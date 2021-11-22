from flask import request, render_template, redirect, Blueprint, current_app
from flask_login import login_user, login_required
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from sqlalchemy import exc
from werkzeug.security import check_password_hash, generate_password_hash

from app import db, login_manager
from app.forms import TransactionEntryForm, LoginForm
from app.models import Transaction, Account, User

DEFAULT_LIMIT = 10

views = Blueprint('views', __name__)
limiter = Limiter(current_app, key_func=get_remote_address)

@login_manager.user_loader
def user_loader(_):
    user = User(current_app.config['HTTP_BASIC_AUTH_USERNAME'], generate_password_hash(current_app.config['HTTP_BASIC_AUTH_PASSWORD']))
    return user

def verify_password(user, username, password):
    if username == user.id and check_password_hash(user.password_hash, password):
        return username


@views.app_template_filter()
def currency_format(value):
    value = float(value)
    return "$ {:,.2f}".format(value)


@views.errorhandler(exc.SQLAlchemyError)
def handle_db_exceptions(error):
    current_app.logger.error(error)
    db.session.rollback()


# --- ROUTES ---------------------------------------------------------------------------------------------------------
@views.route('/')
@limiter.limit("10/minute")
def root():
    return redirect("/transaction")

@views.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    user = User(current_app.config['HTTP_BASIC_AUTH_USERNAME'], generate_password_hash(current_app.config['HTTP_BASIC_AUTH_PASSWORD']))

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        if verify_password(user, username, password) is not None:
            login_user(user)
            return redirect("/transaction")

        error = "Invalid credentials. Please try again."

    return render_template('login.html', form=form, error=error, login=True)

@views.route('/about')
@limiter.limit("10/minute")
def about():
    return render_template('about.html')


@views.route('/transactions/<account_id>')
@login_required
@limiter.limit("10/minute")
def transactions_for(account_id=None):
    limit = request.args.get('limit') or DEFAULT_LIMIT
    tx = Transaction.top(limit, account_id)
    account_name = Account.name_by_id(account_id)
    return render_template('transactions.html', tx=tx, account=account_name, limit=limit)


@views.route('/transactions')
@login_required
@limiter.limit("10/minute")
def transactions():
    limit = request.args.get('limit') or DEFAULT_LIMIT

    accounts = Account.active_accounts()
    tx = Transaction.top(limit)

    return render_template('transactions.html', tx=tx, limit=limit, accounts=accounts)


@views.route('/transaction', methods=['GET', 'POST'])
@login_required
@limiter.limit("10/minute")
def new_transaction():

    # instantiate new entry form
    form = TransactionEntryForm()

    # get non-closed accounts
    accounts = Account.active_accounts()

    # populate drop-down with accounts
    form.account.choices = [(acc.id, acc.name) for acc in accounts]

    # processing a validated POST request
    if form.validate_on_submit():
        account = Account.by_id(form.account.data)
        amount = form.amount.data * 100  # amounts are stored in cents in the database
        tx = Transaction(amount=amount, account=account,
                         memo=form.memo.data, notes=form.notes.data)
        db.session.add(tx)
        db.session.commit()
        current_app.logger.warn('New Transaction Inserted: Account=%s, Amount=%d', account.name, amount)
        return redirect('/transaction/success')

    return render_template('transaction.html', form=form)


@views.route('/transaction/success')
@login_required
@limiter.limit("10/minute")
def transaction_success():
    return render_template('transaction-success.html')

@views.route('/transactions/memos/<memotext>', methods=['GET'])
@login_required
@limiter.limit("100/minute")
def get_memos(memotext=''):
    limit = request.args.get('limit') or DEFAULT_LIMIT
    returnVal = {
        "memos": []
    }
    if memotext is None or memotext == '':
        return returnVal

    transactions = Transaction.memo_contains(limit, memotext)
    for transaction in transactions:
        returnVal['memos'].append(transaction.memo)

    return returnVal
