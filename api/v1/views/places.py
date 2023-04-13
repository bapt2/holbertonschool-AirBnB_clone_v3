#!/usr/bin/python3
'''
Create a new view for Cities objects that handles all
default RESTFul API actions:
'''

from models.city import City
from models.place import Place
from models.user import User
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route('/places/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_all_places(city_id):
    cities = storage.get(City, city_id)
    if cities is None:
        abort(404)
    places_list = []
    all_places = storage.all(Place).values()
    for city in all_places:
        places_list.append(city.to_dict())
    return jsonify(places_list)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    place = storage.get(City, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    rget_json = request.get_json()

    if rget_json is None:
        abort(400, 'Not a JSON')

    if 'user_id' not in rget_json:
        abort(400, 'Missing user_id')

    user_id = rget_json['user_id']
    user = storage.get(User, user_id)

    if user is None:
        abort(404)

    if 'name' not in rget_json:
        abort(400, 'Missing name')

    new_place = Place(**rget_json)
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_state(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    rget_json = request.get_json()
    if rget_json is None:
        abort(400, 'Not a JSON')

    for key, value in rget_json.items():
        if key not in ["id", "user_id", "city_id", "created_at", "updated_at"]:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200
