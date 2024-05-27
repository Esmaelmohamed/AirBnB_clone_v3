#!/usr/bin/python3
"""Index file for the Flask application"""

from flask import jsonify
from api.v1.views import app_views
from models import storage
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review

# Mapping of classes to their names
classes = {
    "users": User,
    "places": Place,
    "states": State,
    "cities": City,
    "amenities": Amenity,
    "reviews": Review
}


@app_views.route('/status', methods=['GET'])
def status():
    '''Route to check the status of the API'''
    return jsonify({'status': 'OK'})


@app_views.route('/stats', methods=['GET'])
def count():
    '''Retrieve the count of each object type'''
    count_dict = {}
    for key, cls in classes.items():
        count_dict[key] = storage.count(cls)
    return jsonify(count_dict)
