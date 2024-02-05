#!/usr/bin/python3
"""
set up route for status endpoint
"""


from api.v1.views import api_views
from flask import jsonify
from models.engine.db_storage import classes
import models


@api_views.route('/status')
def get_status():
    """ send status api"""
    return jsonify({"status": "OK"})


@api_views.route('/stats')
def get_count():
    """Frequency list of the database objects."""
    classes_counts = dict(
        (
            cls.__tablename__, models.storage.count(cls)
        ) for cls in classes.values()
    )
    return jsonify(classes_counts)


@api_views.app_errorhandler(404)
def handle_404(err):
    """Handle 404 page not found error."""
    return jsonify({"error": "Not found"}), 404
