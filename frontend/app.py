#!/usr/bin/python3
"""Flask web application """
from models import storage
from flask import Flask
from frontend.views import app_views

app = Flask(__name__, static_url_path="/static", static_folder="static")
app.config["UPLOAD_FOLDER"] = "frontend/static/images/upload"

app.register_blueprint(app_views)
app.secret_key = "artandculture"


@app.teardown_appcontext
def close_db(error):
    """ Remove the current SQLAlchemy Session """
    storage.close()


if __name__ == "__main__":
    """ Main Function """
    app.run(host='0.0.0.0', port=5006)
