import sys
try:
    from flask import Flask
    import wtforms_json
except ImportError:
    print("\n Flask and WTForm-JSON must be Installed\n")
    sys.exit(0)

def create_app():
    app_init = Flask(__name__)
    wtforms_json.init()

    from . import payment
    app_init.register_blueprint(payment.api)

    return app_init