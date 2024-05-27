#!/usr/bin/python3
"""Define routes for status and statistics endpoints"""

from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review

# Dictionary mapping object types to their corresponding classes
classes = {
    "users": "User",
    "places": "Place",
    "states": "State",
    "cities": "City",
    "amenities": "Amenity",
    "reviews": "Review"
}

@app_views.route('/status', methods=['GET'])
def status():
    '''Endpoint to check the status of the API'''
    return jsonify({'status': 'OK'})

@app_views.route('/stats', methods=['GET'])
def count():
    '''Endpoint to retrieve the count of objects by type'''
    count_dict = {}
    for cls_name, cls in classes.items():
        count_dict[cls_name] = storage.count(cls)
    return jsonify(count_dict)
