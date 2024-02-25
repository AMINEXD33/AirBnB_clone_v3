#!/usr/bin/python3
"""Flask server (variable app)
"""
from flask import Flask, jsonify
from models import storage
from os import getenv
from api.v1.views import app_views
from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *
<<<<<<< HEAD
=======
from api.v1.views.amenities import *
>>>>>>> cf832e2de3146ee26eb42657148339918cc236be
from api.v1.views.users import *

app = Flask(__name__)
app.register_blueprint(app_views)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.url_map.strict_slashes = False
cors = CORS(app, resources={r"/api/v1/*": {"origins": "*"}})


@app.teardown_appcontext
def downtear(self):
    '''Status of your API'''
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    '''return render_template'''
    return jsonify(error='Not found'), 404


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST')
    port = getenv('HBNB_API_PORT')
    if not host:
        host = '0.0.0.0'
    if not port:
        port = '5000'
    app.run(host=host, port=port, threaded=True)
