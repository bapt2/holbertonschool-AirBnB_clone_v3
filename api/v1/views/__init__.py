#!/usr/bin/python3
"""
Blueprint of the API
"""

from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefixe='/api/v1')

from api.v1.views.index import *
