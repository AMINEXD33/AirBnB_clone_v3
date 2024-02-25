#!/usr/bin/python3
""" objects that handles all default RestFul API actions for cities """
from models.city import City
from models.place import Place
from models.state import State
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from


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


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """
    Retrieves the list of all cities objects
    of a specific State, or a specific city
    """
    list_place = []
    city = get_stuff(City, city_id)
    if not city:
        abort(404)
    places = storage.all(Place)
    for place in places:
        if places[place].city_id == city.id:
            list_place.append(places[place].to_dict())
    return jsonify(list_place)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """
    Retrieves a specific city based on id
    """
    place = get_stuff(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """
    Deletes a place based on id provided
    """
    place = get_stuff(Place, place_id)

    if not place:
        abort(404)
    storage.delete(place)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def post_place(city_id):
    """
    Creates a Place
    """
    city = get_stuff(City, city_id)
    if not city:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'name' not in request.get_json():
        abort(400, description="Missing name")
    if 'user_id' not in request.get_json():
        abort(400, description="Missing user_id")
    data = request.get_json()
    all_users = storage.all(User)
    flag = False
    for user in all_users:
        if data["user_id"] in all_users[user]:
            flag = True
    if flag is False:
        abort(400)
    instance = Place(**data)
    instance.city_id = city.id
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('places/<place_id>', methods=['PUT'], strict_slashes=False)
def put_place(place_id):
    """
    Updates a City
    """
    place = get_stuff(Place, place_id)
    if not place:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(place, key, value)
    storage.save()
    return make_response(jsonify(place.to_dict()), 200)
