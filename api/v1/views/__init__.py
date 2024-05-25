#!/usr/bin/python3

from flask import Blueprint, session
from functools import wraps

api_views = Blueprint("api_views", __name__, url_prefix="/api/v1")


def login_required(func):
    @wraps(func)
    def loginwrapper(*args, **kwargs):
        if "email" not in session:
            return jsonify({"error": "Unauthorized access"}), 401
        return func(*args, **kwargs)

    return loginwrapper


from api.v1.views.index import *
from api.v1.views.artists import *
from api.v1.views.artworks import *
from api.v1.views.categories import *
from api.v1.views.messages import *
from api.v1.views.artworks_comments import *
