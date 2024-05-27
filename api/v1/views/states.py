#!/usr/bin/python3
"""New view for State objects"""

from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models.state import State
from models import storage

@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """Retrieves the list of all State objects"""
    states = storage.all(State)
    state_list = [state.to_dict() for state in states.values()]
    return jsonify(state_list)

@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """Retrieves a State object by id
    
    Args:
        state_id (str): The ID of the state to retrieve.

    Returns:
        Response: JSON representation of the state object or 404 if not found.
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())

@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Creates a new State object
    
    Returns:
        Response: JSON representation of the new state object and status 201.
    """
    response = request.get_json()
    if response is None:
        abort(400, description='Not a JSON')
    if "name" not in response:
        abort(400, description='Missing name')
    new_state = State(name=response['name'])
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201

@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Updates an existing State object
    
    Args:
        state_id (str): The ID of the state to update.

    Returns:
        Response: JSON representation of the updated state object and status 200.
    """
    response = request.get_json()
    if response is None:
        abort(400, description='Not a JSON')
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    ignore_keys = ['id', 'created_at', 'updated_at']
    for key, value in response.items():
        if key not in ignore_keys:
            setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict()), 200

@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """Deletes a State object
    
    Args:
        state_id (str): The ID of the state to delete.

    Returns:
        Response: Empty JSON object and status 200.
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200
