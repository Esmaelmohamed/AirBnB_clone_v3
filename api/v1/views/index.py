#!/usr/bin/python3
'''API for status and statistics of various models'''

from flask import Flask, jsonify
from api.v1.views import app_views
from models import storage
from models.state import State
from models.user import User
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review


@app_views.route('/status', strict_slashes=False)
def get_status():
    '''Return the API status'''
    return jsonify(status='OK')


@app_views.route('/stats', strict_slashes=False)
def get_stats():
    '''Return the count of all objects by type'''
    model_classes = {
        'states': State,
        'users': User,
        'amenities': Amenity,
        'cities': City,
        'places': Place,
        'reviews': Review
    }
    counts = {key: storage.count(model) for key, model in model_classes.items()}
    return jsonify(counts)
