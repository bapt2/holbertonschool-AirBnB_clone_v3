#!/usr/bin/python3
'''
Create a new view for Amenities objects that handles all
default RESTFul API actions:
'''

from models.amenity import Amenity
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenity():
    amenity_list = []
    all_amenity = storage.all(Amenity).values()
    for amenity in all_amenity:
        amenity_list.append(amenity.to_dict())
    return jsonify(amenity_list)


@app_views.route('/amenities/<amenity_id>', methods=['GET'], strict_slashes=False)
def error_amenity(amenity_id):
    amenities = storage.get(Amenity, amenity_id)
    if amenities is None:
        abort(404)
    return jsonify(amenities.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    amenity.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    rget_json = request.get_json()
    if rget_json is None:
        abort(400, 'Not a JSON')
    if 'name' not in rget_json:
        abort(400, 'Missing name')

    new_amenity = Amenity(**rget_json)
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    rget_json = request.get_json()
    if rget_json is None:
        abort(400, 'Not a JSON')

    for key, value in rget_json.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(amenity, key, value)
    amenity.save()
    return jsonify(amenity.to_dict()), 200
