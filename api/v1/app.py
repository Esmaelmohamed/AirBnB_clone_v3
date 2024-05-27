#!/usr/bin/python3
"""Main application script"""

from flask import Flask, make_response, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})

# Ensure routes don't require trailing slashes
app.url_map.strict_slashes = False

# Register blueprint for API endpoints
app.register_blueprint(app_views)

# Teardown context to close storage engine
@app.teardown_appcontext
def teardown_db(exception):
    """Closes the storage engine"""
    storage.close()

# Error handler for 404 Not Found
@app.errorhandler(404)
def not_found(error):
    """Handles 404 error and returns JSON-formatted response"""
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    # Get host and port from environment variables or use default values
    host = getenv("HBNB_API_HOST", '0.0.0.0')
    port = int(getenv("HBNB_API_PORT", 5000))
    # Run the Flask application
    app.run(host=host, port=port, threaded=True)
