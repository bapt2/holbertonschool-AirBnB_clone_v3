#!/usr/bin/python3
"""
starts the API
"""

from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv
app = Flask(__name__)
app.register_blueprint(app_views, url_prefixe='/api/v1')

@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()

if __name__ == "__main__":
    HBNB_API_HOST = getenv('HBNB_API_HOST', '0.0.0.0')
    HBNB_API_PORT = getenv('HBNB_API_PORT', '5000')
    app.run(HBNB_API_HOST, HBNB_API_PORT, threaded=True)
