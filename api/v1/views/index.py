#!/usr/bin/python3
"""API status endpoints.
"""

from models import storage
from models.state import State
from models.user import User
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from flask import jsonify
from api.v1.views import app_views

@app_views.route('/status', strict_slashes=False)
def get_status():
    """Returns the status of the API.

    Returns:
        Response: A JSON response indicating the API status.
    """
    return jsonify({'status': 'OK'})

@app_views.route('/stats', strict_slashes=False)
def get_stats():
    """Retrieves the count of each object type.

    Returns:
        Response: A JSON response with the count of each object type.
    """
    models = {
        'states': State,
        'users': User,
        'amenities': Amenity,
        'cities': City,
        'places': Place,
        'reviews': Review
    }
    counts = {key: storage.count(value) for key, value in models.items()}
    return jsonify(counts)
