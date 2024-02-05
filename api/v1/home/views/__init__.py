from flask import Blueprint, session
from functools import wraps

home_views = Blueprint('home_views', __name__, url_prefix="/")

def login_required(func):
    @wraps(func)
    def loginwrapper(*args, **kwargs):
        if 'email' not in session:
            return render_template("unauthorized.html"), 401
        return func(*args, **kwargs)
    return loginwrapper

# {culture feed, top}
from api.v1.home.views.feed import *