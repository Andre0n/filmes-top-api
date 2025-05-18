from flask import Blueprint

from ..controllers import MovieController

movie_blueprint = Blueprint('movies', __name__, url_prefix='/movies')

movie_view = MovieController.as_view('movie_api')

movie_blueprint.add_url_rule(
    '/', defaults={'movie_id': None}, view_func=movie_view, methods=['GET']
)
movie_blueprint.add_url_rule('/', view_func=movie_view, methods=['POST'])
movie_blueprint.add_url_rule(
    '/<string:movie_id>',
    view_func=movie_view,
    methods=['GET', 'PUT', 'DELETE', 'PATCH'],
)
