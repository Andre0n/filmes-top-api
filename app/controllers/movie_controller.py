from flask import Response
from flask.views import MethodView

from ..repositories import MovieRepository
from ..repositories.rental_repository import RentalRepository
from ..repositories.review_repository import ReviewRepository
from ..repositories.user_repository import UserRepository
from ..schemas.movie.add_review_schema import AddReviewRequest
from ..schemas.movie.create_movie_schema import CreateMovieRequest
from ..schemas.movie.get_movie_request_schema import GetMovieRequest
from ..services.movie_service import MovieService
from ..utils.auth_mixin import AuthMixin
from ..validators.body_validator import validate_body
from ..validators.query_validator import validate_query


class MovieBaseController(MethodView, AuthMixin):
    def __init__(self) -> None:
        self.movie_service = MovieService(
            movie_repository=MovieRepository(),
            user_repository=UserRepository(),
            rental_repository=RentalRepository(),
            review_repository=ReviewRepository(),
        )


class MovieController(MovieBaseController):
    def __init__(self) -> None:
        super().__init__()

    @validate_query(GetMovieRequest)
    def get(self, movie_id: str, query: GetMovieRequest) -> Response:

        user_id = self.user_id

        if movie_id:
            return self.movie_service.get_movie(movie_id, user_id)

        if query.rented:
            return self.movie_service.get_rented_movies(user_id)

        return self.movie_service.get_movies(query)

    @validate_body(CreateMovieRequest, 'create_movie_request')
    def post(self, create_movie_request: CreateMovieRequest) -> Response:
        return self.movie_service.create_movie(create_movie_request)


class MovieRentalController(MovieBaseController):
    def __init__(self) -> None:
        super().__init__()

    def post(self, movie_id: str) -> Response:
        return self.movie_service.rent_movie(movie_id, self.user_id)


class MovieReviewController(MovieBaseController):
    def __init__(self) -> None:
        super().__init__()

    @validate_body(AddReviewRequest, 'add_review_request')
    def post(
        self, movie_id: str, add_review_request: AddReviewRequest
    ) -> Response:
        return self.movie_service.add_review(
            movie_id, self.user_id, add_review_request
        )
