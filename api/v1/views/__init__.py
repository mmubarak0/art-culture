#!/usr/bin/python3

from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix="/api/v1")
# {culture feed, top}
from api.v1.views.index import *
# {register, login, logout, followers, following}
from api.v1.views.artists import *
# {artworks}
from api.v1.views.artworks import *
## {categories}
#from api.v1.views.categories import *
## {comments}
#from api.v1.views.comments import *
## {messages}
#from api.v1.views.messages import *
