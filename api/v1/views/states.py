#!/usr/bin/python3
'''API views for managing State objects'''

from flask import Flask, abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    '''Retrieve all State objects'''
    states = storage.all('State')
    state_list = [state.to_dict() for state in states.values()]
    return jsonify(state_list)


@app_views.route('/states/<string:state_id>', methods=['GET'], strict_slashes=False)
def get_state_by_id(state_id):
    '''Retrieve a State object by its ID'''
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict()), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    '''Create a new State object'''
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    if 'name' not in data:
        abort(400, 'Missing name')
    new_state = State(name=data['name'])
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    '''Update an existing State object'''
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    ignored_keys = ['id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignored_keys:
            setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict()), 200


@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    '''Delete a State object by its ID'''
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200
