#!/usr/bin/python3
"""Flask web server."""

import models
import conf
from flask import Flask, jsonify, session
from api.v1.views import app_views
from functools import wraps


app = Flask(__name__)
app.register_blueprint(app_views)
app.secret_key = "artnculture"


@app.teardown_appcontext
def tear_down(exception=None):
    """close session"""
    models.storage.close()


def login_required(func):
    @wraps(func)
    def loginwrapper(*args, **kwargs):
        if 'email' not in session:
            return jsonify({"error": "Unauthorized access"}), 401
        return func(*args, **kwargs)
    return loginwrapper


if __name__ == '__main__':
    host = conf.ANC_API_HOST
    port = conf.ANC_API_PORT
    debug = conf.ANC_API_DEBUG

    app.run(host=host, port=port, debug=debug, threaded=True)
