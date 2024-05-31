#!/usr/bin/python3

from flask import Blueprint

api_views = Blueprint("api_views", __name__, url_prefix="/api/v1")


from api.v1.views.index import *
from api.v1.views.artists import *
from api.v1.views.artworks import *
from api.v1.views.categories import *
from api.v1.views.messages import *
from api.v1.views.artworks_comments import *
from api.v1.views.artworks_medias import *
