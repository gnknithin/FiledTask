import sys
try:
    from flask_wtf import FlaskForm
except ModuleNotFoundError:
    print("\nFlask-WTF must be Installed\n")
    sys.exit(0)
from wtforms import StringField, validators, DecimalField, FloatField
from wtforms.validators import InputRequired, DataRequired,Length, Optional
from wtforms.validators import ValidationError
from datetime import datetime

class ProcessPaymentForm(FlaskForm):
    CreditCardNumber = StringField(validators=[InputRequired(message='Please Enter Credit Card Number')])
    CardHolder = StringField(validators=[InputRequired(message='Please Enter Card Holder Name')])
    ExpirationDate = StringField(validators=[InputRequired(message='Please Enter Expiration Date')])
    SecurityCode = StringField(validators=[Optional()])
    Amount = FloatField(validators=[InputRequired(message='Please Enter Amount')])

    class Meta:
        csrf = False

    def validate_CreditCardNumber(form,field):
        if len(field.data) < 16:
            raise ValidationError('Enter a Valid Credit Card Number')
        elif len(field.data) == 16:
            pass
        elif len(field.data) == 19:
            pass
        else:
            raise ValidationError('Enter a Valid Credit Card Number')
        # End-If-Elif-Else
    
    def validate_ExpirationDate(form,field):
        try:
            _inpute_date = datetime.strptime(field.data,"%m/%y")
            _today = datetime.now()
        except ValueError as err:
            raise ValidationError("Enter Expiration Date as MM/YY")
        except Exception:
            raise ValidationError("Expiration Date Invalid Format")
        # End-Try-Exception
        if _today > _inpute_date:
            raise ValidationError('Expiration Date must be Future Dated')
        # End-If

    def validate_SecurityCode(form,field):
        if len(field.data) != 3:
            raise ValidationError('Security Code must be 3 digit number')
        # End-If
        try:
            _value = int(field.data)
        except ValueError:
            raise ValidationError('Security Code must be  number')

    def validate_Amount(form,field):
        if field.data < 0:
            raise ValidationError('Amount must be Positive')
        if field.data == 0:
            raise ValidationError('Amount must be Positive')
        # End-If