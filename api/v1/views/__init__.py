from flask import Blueprint
<<<<<<< HEAD
=======

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

>>>>>>> refs/remotes/origin/master
from api.v1.views.index import *
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
