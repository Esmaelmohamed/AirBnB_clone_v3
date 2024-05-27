#!/usr/bin/python3
"""cities"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City
from models.state import State

def get_city_by_id(city_id):
    """Helper function to retrieve a city by ID"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return city

def get_state_by_id(state_id):
    """Helper function to retrieve a state by ID"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return state

@app_views.route('/states/<state_id>/cities', methods=['GET'])
def list_cities_of_state(state_id):
    '''Retrieves a list of all City objects'''
    state = get_state_by_id(state_id)
    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)

@app_views.route('/states/<state_id>/cities', methods=['POST'])
def create_city(state_id):
    '''Creates a City'''
    if not request.get_json():
        abort(400, 'Not a JSON')
    data = request.get_json()
    if 'name' not in data or 'state_id' not in data:
        abort(400, 'Missing name or state_id')
    state = get_state_by_id(state_id)
    new_city = City(name=data['name'], state_id=state_id)
    storage.new(new_city)
    storage.save()
    return jsonify(new_city.to_dict()), 201

@app_views.route('/cities/<city_id>', methods=['GET'])
def get_city(city_id):
    '''Retrieves a City object'''
    city = get_city_by_id(city_id)
    return jsonify(city.to_dict())

@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    '''Deletes a City object'''
    city = get_city_by_id(city_id)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200

@app_views.route('/cities/<city_id>', methods=['PUT'])
def updates_city(city_id):
    '''Updates a City object'''
    city = get_city_by_id(city_id)
    if not request.get_json():
        abort(400, 'Not a JSON')
    data = request.get_json()
    if 'name' not in data:
        abort(400, 'Missing name')
    city.name = data['name']
    storage.save()
    return jsonify(city.to_dict()), 200
