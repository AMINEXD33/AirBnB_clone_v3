#!/usr/bin/python3xx
'''api status'''
import models
from models import storage
from flask import jsonify, request, abort
from api.v1.views import app_views
from models.amenity import Amenity
from models.base_model import BaseModel
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def states_all():
    """ returns list of all State objects """
    states_all = []
    states = storage.all(State).values()
    for state in states:
        states_all.append(state.to_dict())
    return jsonify(states_all)


@app_views.route('/states/<state_id>', strict_slashes=False, methods=["GET"])
def states_get(state_id):
    """ handles GET method  and get a specific object
        by ID
    """
    obj = storage.all(State)
    for element in obj:
        if obj[element].id == state_id:
            return jsonify(obj[element].to_dict())
    abort(404)


@app_views.route('/states/<state_id>',
                 strict_slashes=False, methods=["DELETE"])
def states_delete(state_id):
    """ handles DELETE method """
    obj = storage.all(State)
    for element in obj:
        if obj[element].id == state_id:
            storage.delete(obj[element])
            storage.save()
            return jsonify({}), 200
    abort(404)


@app_views.route('/states', strict_slashes=False, methods=['POST'])
def state_post():
    """ handles POST method """
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    if 'name' not in data:
        abort(400, "Missing name")
    state = State(**data)
    state.save()
    state = state.to_dict()
    return jsonify(state), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def state_put(state_id):
    """ handles PUT method """
    state = None
    all_ = storage.all(State)
    for element in all_:
        if all_[element].id == state_id:
            state = all_[element]
    if state is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    state_dict = state.to_dict()
    for key, value in data.items():
        ignore_keys = ["id", "created_at", "updated_at"]
        if key not in ignore_keys:
            state_dict[key] = value
    storage.delete(state)
    state = State(**state_dict)
    state.save()
    state = state.to_dict()
    return jsonify(state), 200
