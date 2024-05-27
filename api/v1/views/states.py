#!/usr/bin/python3
"""Defines routes to handle State objects"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State

@app_views.route('/states/', methods=['GET'])
def list_states():
    '''Retrieves a list of all State objects'''
    state_list = [obj.to_dict() for obj in storage.all("State").values()]
    return jsonify(state_list)

@app_views.route('/states/<state_id>', methods=['GET'])
def get_state(state_id):
    '''Retrieves a specific State object'''
    all_states = storage.all("State").values()
    state_obj = [obj.to_dict() for obj in all_states if obj.id == state_id]
    if not state_obj:
        abort(404)
    return jsonify(state_obj[0])

@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    '''Deletes a specific State object'''
    all_states = storage.all("State").values()
    state_obj = [obj.to_dict() for obj in all_states if obj.id == state_id]
    if not state_obj:
        abort(404)
    state_obj.remove(state_obj[0])
    for obj in all_states:
        if obj.id == state_id:
            storage.delete(obj)
            storage.save()
    return jsonify({}), 200

@app_views.route('/states/', methods=['POST'])
def create_state():
    '''Creates a new State'''
    if not request.get_json():
        abort(400, 'JSON data not provided')
    if 'name' not in request.get_json():
        abort(400, 'Name not provided')
    states = []
    new_state = State(name=request.json['name'])
    storage.new(new_state)
    storage.save()
    states.append(new_state.to_dict())
    return jsonify(states[0]), 201

@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    '''Updates a specific State object'''
    all_states = storage.all("State").values()
    state_obj = [obj.to_dict() for obj in all_states if obj.id == state_id]
    if not state_obj:
        abort(404)
    if not request.get_json():
        abort(400, 'JSON data not provided')
    state_obj[0]['name'] = request.json['name']
    for obj in all_states:
        if obj.id == state_id:
            obj.name = request.json['name']
    storage.save()
    return jsonify(state_obj[0]), 200
