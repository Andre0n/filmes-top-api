from flask import Blueprint

from .movie_blueprint import movie_blueprint

api_blueprint = Blueprint('api', __name__, url_prefix='/api')
api_blueprint.register_blueprint(movie_blueprint)
