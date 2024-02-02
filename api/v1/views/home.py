#!/usr/bin/python3
"""Home views"""

from models import *
from flask import Flask, render_template
from api.v1.views import app_views


@app_views.route('/home', strict_slashes=False)
def index_home():
    """display a HTML page."""
    return render_template('index.html')
