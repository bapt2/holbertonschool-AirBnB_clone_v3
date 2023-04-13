#!/usr/bin/python3
"""
starts the API
"""

from flask import Flask, jsonify, make_response
from api.v1.views import app_views
from os import getenv
from models import storage


app = Flask(__name__)
app.register_blueprint(app_views, url_prefix='/api/v1')


@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    return make_response(jsonify({"error": "Not found"}), 404)

if __name__ == "__main__":
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = getenv('HBNB_API_PORT', '5050')
    app.run(host=host, port=int(port), threaded=True)
