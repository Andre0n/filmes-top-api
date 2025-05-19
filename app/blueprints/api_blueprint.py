from flask import Blueprint

from .auth_blueprint import auth_blueprint
from .movie_blueprint import movie_blueprint

api_blueprint = Blueprint('api', __name__, url_prefix='/api')
api_blueprint.register_blueprint(movie_blueprint)
api_blueprint.register_blueprint(auth_blueprint)
