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
        """
        Get movies or a specific movie
        ---
        tags:
          - Movies
        description: |
          Get a list of movies with optional filtering or a specific movie by ID.
          When movie_id is provided, returns details for that specific movie.
          When rented=true query parameter is provided, returns movies rented by the authenticated user.
        security:
          - BearerAuth: []
        parameters:
          - name: movie_id
            in: path
            type: string
            required: false
            description: ID of the movie to retrieve
          - name: page
            in: query
            type: integer
            required: false
            default: 1
            minimum: 1
            description: Page number for pagination
          - name: limit
            in: query
            type: integer
            required: false
            default: 100
            minimum: 1
            maximum: 100
            description: Number of items per page
          - name: search
            in: query
            type: string
            required: false
            maxLength: 100
            description: Search term to filter movies by title
          - name: genre
            in: query
            type: string
            required: false
            maxLength: 50
            description: Filter movies by genre
          - name: rented
            in: query
            type: boolean
            required: false
            description: Filter movies rented by the current user
        responses:
          200:
            description: Successful operation
            schema:
              oneOf:
                - $ref: '#/definitions/MovieResponse'
                - $ref: '#/definitions/ListMovieResponseDto'
                - $ref: '#/definitions/ListRentedMoviesResponseDto'
          401:
            $ref: '#/responses/Unauthorized'
          404:
            $ref: '#/responses/NotFound'
          500:
            $ref: '#/responses/InternalServerError'
        """
        user_id = self.user_id

        if movie_id:
            return self.movie_service.get_movie(movie_id, user_id)

        if query.rented:
            return self.movie_service.get_rented_movies(user_id)

        return self.movie_service.get_movies(query)

    @validate_body(CreateMovieRequest, 'create_movie_request')
    def post(self, create_movie_request: CreateMovieRequest) -> Response:
        """
        Create a new movie
        ---
        tags:
          - Movies
        description: Create a new movie entry
        security:
          - BearerAuth: []
        consumes:
          - application/json
        produces:
          - application/json
        parameters:
          - in: body
            name: body
            description: Movie data
            required: true
            schema:
              $ref: '#/definitions/CreateMovieRequest'
        responses:
          201:
            description: Movie created successfully
            schema:
              $ref: '#/definitions/MovieResponse'
          400:
            $ref: '#/responses/ValidationError'
          409:
            description: Movie title already exists
            schema:
              $ref: '#/definitions/ErrorResponse'
            examples:
              application/json:
                code: 409
                message: Um filme com esse título já existe
                data:
                  errors: MOVIE_TITLE_ALREADY_EXISTS
          500:
            $ref: '#/responses/InternalServerError'
        """
        return self.movie_service.create_movie(create_movie_request)


class MovieRentalController(MovieBaseController):
    def __init__(self) -> None:
        super().__init__()

    def post(self, movie_id: str) -> Response:
        """
        Rent a movie
        ---
        tags:
          - Movies
        description: Rent a movie for the authenticated user
        security:
          - BearerAuth: []
        parameters:
          - name: movie_id
            in: path
            type: string
            required: true
            description: ID of the movie to rent
        responses:
          201:
            description: Movie rented successfully
            schema:
              $ref: '#/definitions/MovieResponse'
          401:
            $ref: '#/responses/Unauthorized'
          404:
            description: Movie not found
            schema:
              $ref: '#/definitions/ErrorResponse'
            examples:
              application/json:
                code: 404
                message: Filme não encontrado
                data:
                  errors: MOVIE_NOT_FOUND
          409:
            description: Movie already rented by user
            schema:
              $ref: '#/definitions/ErrorResponse'
            examples:
              application/json:
                code: 409
                message: O filme já está alugado
                data:
                  errors: MOVIE_ALREADY_RENTED
          500:
            $ref: '#/responses/InternalServerError'
        """
        return self.movie_service.rent_movie(movie_id, self.user_id)


class MovieReviewController(MovieBaseController):
    def __init__(self) -> None:
        super().__init__()

    @validate_body(AddReviewRequest, 'add_review_request')
    def post(
        self, movie_id: str, add_review_request: AddReviewRequest
    ) -> Response:
        """
        Add a review to a movie
        ---
        tags:
          - Movies
        description: Add a review and rating to a movie
        security:
          - BearerAuth: []
        consumes:
          - application/json
        produces:
          - application/json
        parameters:
          - name: movie_id
            in: path
            type: string
            required: true
            description: ID of the movie to review
          - in: body
            name: body
            description: Review data
            required: true
            schema:
              $ref: '#/definitions/AddReviewRequest'
        responses:
          201:
            description: Review added successfully
            schema:
              $ref: '#/definitions/MovieResponse'
          400:
            description: Invalid input data
            schema:
              $ref: '#/definitions/ErrorResponse'
            examples:
              application/json:
                code: 400
                message: Tentativa de avaliar um filme que não foi alugado
                data:
                  errors: TRY_REVIEW_NOT_RENTED_MOVIE
          401:
            $ref: '#/responses/Unauthorized'
          404:
            $ref: '#/responses/NotFound'
          409:
            description: User already reviewed this movie
            schema:
              $ref: '#/definitions/ErrorResponse'
            examples:
              application/json:
                code: 409
                message: Tentativa de avaliar um filme que já foi avaliado
                data:
                  errors: TRY_REVIEW_ALREADY_RATED_MOVIE
          500:
            $ref: '#/responses/InternalServerError'
        """
        return self.movie_service.add_review(
            movie_id, self.user_id, add_review_request
        )
