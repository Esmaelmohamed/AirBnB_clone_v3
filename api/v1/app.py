#!/usr/bin/python3
"""Flask server configuration and initialization.
"""

from flask import Flask, jsonify
from models import storage
from os import getenv
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)
app.url_map.strict_slashes = False

@app.teardown_appcontext
def teardown_db(exception):
    """Closes the storage on teardown.

    Args:
        exception (Exception): The exception that caused the teardown.
    """
    storage.close()

@app.errorhandler(404)
def not_found(error):
    """Handles 404 errors by returning a JSON response.

    Args:
        error (HTTPException): The exception that caused the 404 error.

    Returns:
        Response: A JSON response with a 404 status code.
    """
    return jsonify({'error': 'Not found'}), 404

if __name__ == "__main__":
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = getenv('HBNB_API_PORT', '5000')
    app.run(host=host, port=port, threaded=True)
