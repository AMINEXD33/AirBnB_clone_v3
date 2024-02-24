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
    print(state)
    state.save()
    state = state.to_dict()
    return jsonify(state), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def state_put(state_id):
    """ handles PUT method """
    # see if already exists
    obj = storage.all(State)
    for element in obj:
        if obj[element].id == state_id:
            storage.delete(obj[element])
            storage.save()
            return jsonify({}), 200
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    if state_id is None:
        abord(404)
    for key, value in data.items():
        ignore_keys = ["id", "created_at", "updated_at"]
        if key not in ignore_keys:
            obj[element].bm_update(key, value)
    obj[element].save()
    obj[element] = obj[element].to_dict()
    return jsonify(obj[element]), 200
