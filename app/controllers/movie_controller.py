from flask import Response
from flask.views import MethodView
from flask_jwt_extended import jwt_required  # pyright: ignore

from ..repositories import MovieRepository
from ..schemas.movie.create_movie_schema import CreateMovieRequest
from ..schemas.movie.get_movie_request_schema import GetMovieRequest
from ..services.movie_service import MovieService
from ..validators.body_validator import validate_body
from ..validators.query_validator import validate_query


class MovieController(MethodView):
    def __init__(self) -> None:
        self.movie_service = MovieService(movie_repository=MovieRepository())

    @validate_query(GetMovieRequest)
    @jwt_required()   # type: ignore
    def get(self, movie_id: str, query: GetMovieRequest) -> Response:
        if movie_id:
            return self.movie_service.get_movie(movie_id)
        return self.movie_service.get_movies(query)

    @validate_body(CreateMovieRequest, 'create_movie_request')
    @jwt_required()   # type: ignore
    def post(self, create_movie_request: CreateMovieRequest) -> Response:
        return self.movie_service.create_movie(create_movie_request)
