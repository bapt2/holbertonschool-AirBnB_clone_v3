#!/usr/bin/python3
'''
Create a new view for State objects that handles all
default RESTFul API actions:
'''

from models import state
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_state():
    state_list = []
    all_state = storage.all(state).value()
    for states in all_state:
        state_list.append(states.to_dict())
    return jsonify(state_list)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def error_state(state_id):
    states = storage.get(state, state_id)
    if states is None:
        abort('404')
    return jsonify(states)


@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    states = storage.get(state, state_id)
    if states is None:
        abort(404)
    states.delete()
    storage.save()
    return jsonify(), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    if not request.json:
        abort(400, 'Not a JSON')
    if 'name' not in request.json:
        abort(400, 'Missing name')
    nstate = {}
    storage.save(nstate)
    return jsonify(nstate), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    states = storage.get(state, state_id)
    if states is None:
        abort('404')
    if not request.json:
        abort(400, 'Not a JSON')
    if 'name' not in request.json:
        abort(400, 'Missing name')
    nstate = {}
    storage.save(nstate)
    return jsonify(nstate), 201
