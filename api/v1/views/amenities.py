#!/usr/bin/python3xx
'''api status'''
import models
from models import storage
from flask import jsonify, request, abort
from api.v1.views import app_views
from models.amenity import Amenity
from models.base_model import BaseModel
from models.state import State


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def amenity_all():
    """ returns list of all State objects """
    amenity_all = []
    aminities = storage.all(Amenity).values()
    for state in aminities:
        amenity_all.append(state.to_dict())
    return jsonify(amenity_all)


@app_views.route('/amenities/<amenity_id>',
                 strict_slashes=False, methods=["GET"])
def amenity_get(amenity_id):
    """ handles GET method  and get a specific object
        by ID
    """
    if amenity_id is None:
        abort(404)
    obj = storage.all(Amenity)
    for element in obj:
        if obj[element].id == amenity_id:
            return jsonify(obj[element].to_dict())
    abort(404)


@app_views.route('/amenities/<amenity_id>',
                 strict_slashes=False, methods=["DELETE"])
def amenity_delete(amenity_id):
    """ handles DELETE method """
    if amenity_id is None:
        abort(404)
    obj = storage.all(Amenity)
    for element in obj:
        if obj[element].id == amenity_id:
            storage.delete(obj[element])
            storage.save()
            return jsonify({}), 200
    abort(404)


@app_views.route('/amenities', strict_slashes=False, methods=['POST'])
def amenity_post():
    """ handles POST method """
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    if 'name' not in data:
        abort(400, "Missing name")
    amenity_obj = Amenity(**data)
    amenity_obj.save()
    amenity_obj = amenity_obj.to_dict()
    return jsonify(amenity_obj), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def amenity_put(amenity_id):
    """ handles PUT method """
    amenity = None
    all_ = storage.all(Amenity)
    for element in all_:
        if all_[element].id == amenity_id:
            amenity = all_[element]
    if amenity is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    amenity_dict = amenity.to_dict()
    for key, value in data.items():
        ignore_keys = ["id", "created_at", "updated_at"]
        if key not in ignore_keys:
            amenity_dict[key] = value
    storage.delete(amenity)
    amenity = State(**amenity_dict)
    amenity.save()
    amenity = amenity.to_dict()
    return jsonify(amenity), 200
