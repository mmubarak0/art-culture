#!/usr/bin/python3
"""Flask web server."""
from models import storage
from api.v1.views import api_views
from os import environ
from flask import Flask, make_response, jsonify
from flask_cors import CORS
from flasgger import Swagger

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.register_blueprint(api_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})


@app.teardown_appcontext
def close_db(error):
    """ Close Storage """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """ 404 Error
    ---
    responses:
      404:
        description: a resource was not found
    """
    return make_response(jsonify({'error': "Not found"}), 404)

@app.errorhandler(400)
def bad_request(error):
    """ 400 Error
    ---
    responses:
      400:
        description: bad request
    """
    return make_response(jsonify({'error': "Bad request"}), 400)

app.config['SWAGGER'] = {
    'title': 'Art and Culture Restful API',
    'uiversion': 3
}

Swagger(app)

if __name__ == "__main__":
    """ Main Function """
    host = environ.get('ANC_API_HOST')
    port = environ.get('ANC_API_PORT')
    if not host:
        host = '0.0.0.0'
    if not port:
        port = '5004'
    app.run(host=host, port=port, threaded=True)
