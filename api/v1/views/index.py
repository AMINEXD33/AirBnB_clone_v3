#!/usr/bin/python3xx
'''api status'''
import models
from models import storage
from models.base_model import BaseModel
from flask import jsonify
from api.v1.views import app_views
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status', strict_slashes=False)
def returnstuff():
    '''return stuff'''
    return jsonify(status='OK')


@app_views.route('/stats', strict_slashes=False)
def count():
    '''Returns a count of all classes'''
    classes = {'states': State,
               'users': User,
               'amenities': Amenity,
               'cities': City,
               'places': Place,
               'reviews': Review}
    for key in classes:
        print("got in ", classes[key])
        classes[key] = storage.count(classes[key])
    return jsonify(classes)
