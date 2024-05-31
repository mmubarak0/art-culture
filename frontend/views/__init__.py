#!/usr/bin/python3

from flask import Blueprint, session, redirect
from functools import wraps

app_views = Blueprint("app_views", __name__, url_prefix="/")


def login_required(func):
    @wraps(func)
    def loginwrapper(*args, **kwargs):
        if "artist_id" not in session:
            return redirect("/login")
        return func(*args, **kwargs)
    return loginwrapper


from frontend.views.main import *
from frontend.views.auth import *
