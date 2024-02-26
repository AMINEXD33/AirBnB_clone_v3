#!/usr/bin/python3
"""
View for Reviews that handles all RESTful API actions
"""

from flask import jsonify, request, abort
from models import storage
from models.place import Place
from models.city import City
from models.state import State
from models.user import User
from models.review import Review
from api.v1.views import app_views


def get_stuff(class_, id):
    """
       a function to replace the one in the storage,
       since it has some kinda bug
    """
    all_ = storage.all(class_)
    for element in all_:
        if all_[element].id == id:
            return all_[element]
    return None


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def reviews_all(place_id):
    """ returns list of all Review objects """
    place = get_stuff(Place, place_id)
    if place is None:
        abort(404)
    reviews_all = []
    reviews = storage.all(Review).values()
    for review in reviews:
        if review.place_id == place_id:
            reviews_all.append(review.to_json())
    return jsonify(reviews_all)


@app_views.route('/reviews/<review_id>',
                 methods=['GET'], strict_slashes=False)
def review_get(review_id):
    """ handles GET method """
    review = get_stuff(Review, review_id)
    if review is None:
        abort(404)
    review = review.to_json()
    return jsonify(review)


@app_views.route('/reviews/<review_id>',
                 methods=['DELETE'], strict_slashes=False)
def review_delete(review_id):
    """ handles DELETE method """
    empty_dict = {}
    review = get_stuff(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify(empty_dict), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def review_post(place_id):
    """ handles POST method """
    place = get_stuff(Place, place_id)
    if place is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    if 'user_id' not in data:
        abort(400, "Missing user_id")
    user = get_stuff(User, data['user_id'])
    if user is None:
        abort(404)
    if 'text' not in data:
        abort(400, "Missing text")
    review = Review(**data)
    review.place_id = place_id
    review.save()
    review = review.to_json()
    return jsonify(review), 201


@app_views.route('/reviews/<review_id>',
                 methods=['PUT'], strict_slashes=False)
def review_put(review_id):
    """ handles PUT method """
    review = get_stuff(Review, review_id)
    if review is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    for key, value in data.items():
        ignore_keys = ["id", "user_id", "place_id", "created_at", "updated_at"]
        if key not in ignore_keys:
            review.bm_update(key, value)
    review.save()
    review = review.to_json()
    return jsonify(review), 200
