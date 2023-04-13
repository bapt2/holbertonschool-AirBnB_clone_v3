#!/usr/bin/python3
"""
Blueprint of the API
"""

from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1', strict_slashes=False)

from api.v1.views.index import *
from api.v1.views.states import *