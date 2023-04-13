#!/usr/bin/python3
'''

'''

from models import state
from models import storage
from api.v1.views import app_views
from flask import Flask, jsonify, abort, make_responce, request
state = Flask(__name__)


@app_views.route('/states', methods=['GET'])
def get_state():
    state_list = []
    all_state = storage.all(state).value()
    for states in all_state:
        state_list.append(states.to_dict())
    return jsonify(state_list)

@app_views.route('/states/<state_id>', methods=['GET'])
def error_state(state_id):
    states = storage.get(state, state_id)
    if states is None:
        abort('404')
    return jsonify(states)


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    states = storage.get(state, state_id)
    if states is None:
        abort(404)
    states.delete()
    return jsonify(), 200


@app_views.route('/states', methods=['POST'])
def create_state():
    if not request.json:
        abort(400, 'Not a JSON')
    if not 'name' in request.json:
        abort(400, 'Missing name')
    nstate = 
    return


@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    states = storage.get(state, state_id)
    if states is None:
        abort('404')
