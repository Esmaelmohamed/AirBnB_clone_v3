#!/usr/bin/python3
"""Flask application setup"""

from flask import Flask, make_response, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})

app.url_map.strict_slashes = False
app.register_blueprint(app_views)

@app.teardown_appcontext
def teardown_db(exception):
    '''Closes the storage engine on teardown'''
    storage.close()

@app.errorhandler(404)
def not_found(error):
    '''Handles 404 errors and returns a JSON response'''
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    host = getenv("HBNB_API_HOST", '0.0.0.0')
    port = int(getenv("HBNB_API_PORT", 5000))
    app.run(host=host, port=port, threaded=True)
