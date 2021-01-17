import warnings
warnings.filterwarnings("ignore",category=DeprecationWarning)
from flask import Blueprint, request,abort, make_response, jsonify
from .forms import ProcessPaymentForm
from .external import PaymentGateWay
from .utility import create_response

api = Blueprint('api', __name__)

@api.errorhandler(500)
def handle_internal_server_error(error_obj):
    return create_response(500,'Handle Internal Server Error')

@api.errorhandler(405)
def handle_method_not_allowed(error_obj):
    return create_response(405,'Method Not Allowed')

@api.errorhandler(404)
def handle_not_found(error_obj):
    return create_response(404,'URL Not Found')

@api.errorhandler(400)
def handle_bad_request(error_obj):
    return create_response(400,'Bad Request')

@api.route('/',methods=['POST'])
def ProcessPayment():
    if request.content_type == 'application/json':
        if request.method == 'POST':
            _form = ProcessPaymentForm()
            _form.from_json(request.json)
            if _form.validate():
                _sucess, _message = PaymentGateWay(_form.data) 
                if _sucess: # Processed and Successful Payment
                    return create_response(200,_message)
                else: # Processed but Failed Payment
                    return create_response(400,_message)
                # End-If-Else
            else:
                resp_errors = {}
                for each in _form.errors:
                    resp_errors[each] = _form.errors[each][0]
                # End-For
                return make_response(jsonify(resp_errors),400)
            # End-If-Else
        else:
            abort(405)
        # End-If-Else
    else:
        abort(400)
    # End-If-Else        
    abort(500)
    # End