#!/usr/bin/python3

from flask import Blueprint, session
from functools import wraps

api_views = Blueprint('api_views', __name__, url_prefix="/api/v1")

def login_required(func):
    @wraps(func)
    def loginwrapper(*args, **kwargs):
        if 'email' not in session:
            return jsonify({"error": "Unauthorized access"}), 401
        return func(*args, **kwargs)
    return loginwrapper

# {culture feed, top}
from api.v1.views.index import *
# {register, login, logout, followers, following}
from api.v1.views.artists import *
#    api_login_view, login_view, logout, register_view, get_artists,
#    get_artist_by_id, alter_artist_by_id, list_artworks_from_artist,
#    create_artist, delete_artist_by_id
# {artworks}
from api.v1.views.artworks import *
## {categories}
#from api.v1.views.categories import *
## {comments}
#from api.v1.views.comments import *
## {messages}
#from api.v1.views.messages import *

