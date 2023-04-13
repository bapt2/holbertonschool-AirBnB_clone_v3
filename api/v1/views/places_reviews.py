#!/usr/bin/python3
'''
Create a new view for Cities objects that handles all
default RESTFul API actions:
'''

from models.city import City
from models.place import Place
from models.user import User
from models.review import Review
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_all_reviews(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    review_list = []
    all_reviews = storage.all(Review).values()
    for reviews in all_reviews:
        review_list.append(reviews.to_dict())
    return jsonify(review_list)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_place(review_id):
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(review_id):
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    review.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_place(place_id):
    place = storage.get(Place, place_id)
    if place is None:
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

    if 'text' not in rget_json:
        abort(400, 'Missing text')

    new_review = Place(**rget_json)
    new_review.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_state(review_id):
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    rget_json = request.get_json()
    if rget_json is None:
        abort(400, 'Not a JSON')

    for key, value in rget_json.items():
        if key not in ["id", "user_id", "place_id",
                       "created_at", "updated_at"]:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict()), 200
