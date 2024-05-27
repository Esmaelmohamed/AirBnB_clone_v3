#!/usr/bin/python3
"""Defines routes to handle Place objects"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City
from models.place import Place
from datetime import datetime
import uuid

@app_views.route('/cities/<city_id>/places', methods=['GET'])
@app_views.route('/cities/<city_id>/places/', methods=['GET'])
def list_places_of_city(city_id):
    '''Retrieves a list of all Place objects in a city'''
    all_cities = storage.all("City").values()
    city_obj = [obj.to_dict() for obj in all_cities if obj.id == city_id]
    if not city_obj:
        abort(404)
    list_places = [obj.to_dict() for obj in storage.all("Place").values()
                   if city_id == obj.city_id]
    return jsonify(list_places)

@app_views.route('/places/<place_id>', methods=['GET'])
def get_place(place_id):
    '''Retrieves a specific Place object'''
    all_places = storage.all("Place").values()
    place_obj = [obj.to_dict() for obj in all_places if obj.id == place_id]
    if not place_obj:
        abort(404)
    return jsonify(place_obj[0])

@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    '''Deletes a specific Place object'''
    all_places = storage.all("Place").values()
    place_obj = [obj.to_dict() for obj in all_places if obj.id == place_id]
    if not place_obj:
        abort(404)
    place_obj.remove(place_obj[0])
    for obj in all_places:
        if obj.id == place_id:
            storage.delete(obj)
            storage.save()
    return jsonify({}), 200

@app_views.route('/cities/<city_id>/places', methods=['POST'])
def create_place(city_id):
    '''Creates a new Place'''
    if not request.get_json():
        abort(400, 'JSON data not provided')
    if 'user_id' not in request.get_json():
        abort(400, 'User ID not provided')
    if 'name' not in request.get_json():
        abort(400, 'Name not provided')
    all_cities = storage.all("City").values()
    city_obj = [obj.to_dict() for obj in all_cities if obj.id == city_id]
    if not city_obj:
        abort(404)
    places = []
    new_place = Place(name=request.json['name'],
                      user_id=request.json['user_id'], city_id=city_id)
    all_users = storage.all("User").values()
    user_obj = [obj.to_dict() for obj in all_users if obj.id == new_place.user_id]
    if not user_obj:
        abort(404)
    storage.new(new_place)
    storage.save()
    places.append(new_place.to_dict())
    return jsonify(places[0]), 201

@app_views.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    '''Updates a specific Place object'''
    all_places = storage.all("Place").values()
    place_obj = [obj.to_dict() for obj in all_places if obj.id == place_id]
    if not place_obj:
        abort(404)
    if not request.get_json():
        abort(400, 'JSON data not provided')
    for field in ['name', 'description', 'number_rooms', 'number_bathrooms',
                  'max_guest', 'price_by_night', 'latitude', 'longitude']:
        if field in request.get_json():
            place_obj[0][field] = request.json[field]
    for obj in all_places:
        if obj.id == place_id:
            for field in ['name', 'description', 'number_rooms', 'number_bathrooms',
                          'max_guest', 'price_by_night', 'latitude', 'longitude']:
                if field in request.get_json():
                    setattr(obj, field, request.json[field])
    storage.save()
    return jsonify(place_obj[0]), 200
