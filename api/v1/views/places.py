#!/usr/bin/python3xx
'''api status'''
import models
from models import storage
from flask import jsonify, request, abort
from api.v1.views import app_views
from models.base_model import BaseModel
from models.place import Place


@app_views.route('/places', methods=['GET'], strict_slashes=False)
def place_all():
    """ returns list of all State objects """
    place_all = []
    places = storage.all(Place).values()
    for place in places:
        place_all.append(place.to_dict())
    return jsonify(states_all)


@app_views.route('/places/<place_id>', strict_slashes=False, methods=["GET"])
def place_get(place_id):
    """ handles GET method  and get a specific object
        by ID
    """
    if place_id is None:
        abort(404)
    obj = storage.all(Place)
    for element in obj:
        if obj[element].id == place_id:
            return jsonify(obj[element].to_dict())
    abort(404)


@app_views.route('/places/<place_id>',
                 strict_slashes=False, methods=["DELETE"])
def states_delete(place_id):
    """ handles DELETE method """
    if place_id is None:
        abort(404)
    obj = storage.all(Place)
    for element in obj:
        if obj[element].id == place_id:
            storage.delete(obj[element])
            storage.save()
            return jsonify({}), 200
    abort(404)


@app_views.route('/places', strict_slashes=False, methods=['POST'])
def state_post():
    """ handles POST method """
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    if 'name' not in data:
        abort(400, "Missing name")
    place = Place(**data)
    place.save()
    place = place.to_dict()
    return jsonify(place), 201


@app_views.route('/places/<place_id>', methods=['PUT'])
def state_put(place_id):
    """ handles PUT method """
    place = None
    all_ = storage.all(State)
    for element in all_:
        if all_[element].id == place_id:
            place = all_[element]
    if place is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    place_dict = place.to_dict()
    for key, value in data.items():
        ignore_keys = ["id", "created_at", "updated_at", "city_id", "user_id"]
        if key not in ignore_keys:
            place_dict[key] = value
    storage.delete(place)
    place = State(**place_dict)
    place.save()
    place = place.to_dict()
    return jsonify(place), 200
