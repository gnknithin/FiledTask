from flask import jsonify

def create_response(status_code,message):
    _response = jsonify(message)
    _response.status_code = status_code
    return _response