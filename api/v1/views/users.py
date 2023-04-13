#!/usr/bin/python3
'''
Create a new view for User objects that handles all
default RESTFul API actions:
'''

from models.user import User
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_state():
    user_list = []
    all_user = storage.all(User).values()
    for states in all_user:
        user_list.append(states.to_dict())
    return jsonify(user_list)


@app_views.route('/users/<users_id>', methods=['GET'], strict_slashes=False)
def error_state(user_id):
    users = storage.get(User, user_id)
    if users is None:
        abort(404)
    return jsonify(users.to_dict())


@app_views.route('/users/<users_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(user_id):
    users = storage.get(User, user_id)
    if users is None:
        abort(404)
    users.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_state():
    rget_json = request.get_json()
    if rget_json is None:
        abort(400, 'Not a JSON')
    if 'email' not in rget_json:
        abort(400, 'Missing email')
    if 'password' not in rget_json:
        abort(400, 'Missing password')

    nusers = User(**rget_json)
    nusers.save()
    return jsonify(nusers.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_state(user_id):
    users = storage.get(User, user_id)
    if users is None:
        abort(404)
    rget_json = request.get_json()
    if rget_json is None:
        abort(400, 'Not a JSON')

    for key, value in rget_json.items():
        if key not in ["id", "email", "created_at", "updated_at"]:
            setattr(users, key, value)
    users.save()
    return jsonify(users.to_dict()), 200
