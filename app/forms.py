from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SelectField, PasswordField
from wtforms.validators import DataRequired, Optional


class TransactionEntryForm(FlaskForm):
    account = SelectField(u'Account', coerce=int)
    amount = FloatField(u'Amount', validators=[DataRequired()])
    memo = StringField(u'Memo', validators=[Optional()])
    notes = StringField(u'Notes', validators=[Optional()])

class LoginForm(FlaskForm):
    username = StringField(u'Username', validators=[DataRequired()])
    password = PasswordField(u'Password', validators=[DataRequired()])
