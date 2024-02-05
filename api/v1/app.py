#!/usr/bin/python3
"""Flask web server."""

import models
import conf
from flask import Flask
from api.v1.views import api_views
from api.v1.home.views import home_views


app = Flask(__name__)
app.register_blueprint(api_views)
app.register_blueprint(home_views)
app.secret_key = "artnculture"


@app.teardown_appcontext
def tear_down(exception=None):
    """close session"""
    models.storage.close()


if __name__ == '__main__':
    host = conf.ANC_API_HOST
    port = conf.ANC_API_PORT
    debug = conf.ANC_API_DEBUG

    app.run(host=host, port=port, debug=debug, threaded=True)
