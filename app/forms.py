from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SelectField
from wtforms.validators import DataRequired, Optional


class TransactionEntryForm(FlaskForm):
    account = SelectField(u'Account', coerce=int)
    amount = FloatField(u'Amount', validators=[DataRequired()])
    memo = StringField(u'Memo', validators=[Optional()])
    notes = StringField(u'Notes', validators=[Optional()])
