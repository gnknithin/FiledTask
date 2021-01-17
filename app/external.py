from flask import jsonify



def get_sucess_and_message():
    import random
    # _sucess = random.choice([True, False])
    _sucess = True
    _message = None
    if _sucess:
        _message = 'Ok'
    else:
        _message = 'Error in Processing'
    return (_sucess,_message)

def _CheapPaymentGateway(data):
    return get_sucess_and_message()

def _ExpensivePaymentGateway(data):
    return get_sucess_and_message()

def _PremiumPaymentGateway(data):
    return get_sucess_and_message()

def PaymentGateWay(data):
    _Amount = data['Amount']
    _processed = None
    if(_Amount > 500):
        for each_time in [1,2,3]:
            _processed, _message = _PremiumPaymentGateway(data)
            if _processed:
                break
            # End-If
        # End-For
    elif (_Amount >20 and _Amount <= 500):
        _processed, _message = _ExpensivePaymentGateway(data)
        if not _processed:
            _processed, _message = _CheapPaymentGateway(data)
        # End-If
    elif(_Amount <= 20):
        _processed, _message = _CheapPaymentGateway(data)
    # End-If-Elif-Elif
    if _processed:
        return _processed,_message
    else:
        return False,'Failed'
    # End-If-Else