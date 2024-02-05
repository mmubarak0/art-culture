#!/usr/bin/python3
"""Feed views"""

from models import *
from flask import Flask, render_template, session
from api.v1.home.views import home_views


@home_views.route('/', strict_slashes=False)
def index_home():
    """display a HTML page."""
    authenticated = 'email' in session
    return render_template('index.html', authenticated=authenticated)
