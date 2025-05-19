from datetime import datetime, timedelta

from flask import Response

from ..dtos.movie_dto import ListMovieResponseDto, ListRentedMoviesResponseDto, MovieResponseDto
from ..dtos.review_dto import ReviewDto
from ..repositories import MovieRepository, RentalRepository, UserRepository
from ..repositories.review_repository import ReviewRepository
from ..schemas.movie.add_review_schema import AddReviewRequest
from ..schemas.movie.create_movie_schema import CreateMovieRequest
from ..schemas.movie.get_movie_request_schema import GetMovieRequest
from ..types.error import ApiErrorCodes
from ..utils.api_response import ApiResponse
from ..utils.exceptions import CustomException


class MovieService:
    def __init__(
        self,
        movie_repository: MovieRepository,
        user_repository: UserRepository,
        rental_repository: RentalRepository,
        review_repository: ReviewRepository,
    ):
        self.movie_repository = movie_repository
        self.user_repository = user_repository
        self.rental_repository = rental_repository
        self.review_repository = review_repository

    def get_movies(self, get_movie_request: GetMovieRequest) -> Response:
        if get_movie_request.search:
            movies = self.movie_repository.find_by_title(
                get_movie_request.search
            )
            return ApiResponse.send(
                status_code=200,
                data={'movies': ListMovieResponseDto.from_model(movies).__dict__},
            )

        if get_movie_request.genre:
            movies = self.movie_repository.find_by_genre(
                get_movie_request.genre
            )
            return ApiResponse.send(
                status_code=200,
                data={'movies': ListMovieResponseDto.from_model(movies).__dict__},
            )

        page = get_movie_request.page or 1
        page_size = get_movie_request.limit or 100
        movies = self.movie_repository.find_all(
            (page - 1) * page_size, page_size
        )
        return ApiResponse.send(
            data={'movies': ListMovieResponseDto.from_model(movies).__dict__}
        )

    def get_movie(self, movie_id: str) -> Response:
        movie = self.movie_repository.find_by_id(movie_id)
        return ApiResponse.send(
            data=MovieResponseDto.from_model(movie).__dict__
        )

    def create_movie(
        self, create_movie_request: CreateMovieRequest
    ) -> Response:
        movie = self.movie_repository.create(create_movie_request)
        return ApiResponse.send(
            status_code=201,
            message='Filme criado com sucesso',
            data=MovieResponseDto.from_model(movie).__dict__,
        )

    def rent_movie(self, movie_id: str, user_id: str) -> Response:
        movie = self.movie_repository.find_by_id(movie_id)
        user = self.user_repository.find_by_id(user_id)

        if not user:
            raise CustomException(ApiErrorCodes.USER_NOT_FOUND)
        if not movie:
            raise CustomException(ApiErrorCodes.MOVIE_NOT_FOUND)

        rental = self.rental_repository.find_by_user_and_movie(
            user_id=user_id, movie_id=movie_id
        )

        if rental:
            raise CustomException(
                ApiErrorCodes.MOVIE_ALREADY_RENTED,
                data={
                    'movie_id': movie_id,
                },
            )

        expiration_date = datetime.now() + timedelta(days=7)
        self.rental_repository.create(
            user_id=user_id, movie_id=movie_id, expiration_date=expiration_date
        )

        return ApiResponse.send(
            message='Filme alugado com sucesso',
        )

    def get_rented_movies(self, user_id: str) -> Response:
        user = self.user_repository.find_by_id(user_id)

        if not user:
            raise CustomException(ApiErrorCodes.USER_NOT_FOUND)

        rentals = self.rental_repository.find_by_user_id(user_id)

        return ApiResponse.send(
            message='Filmes alugados encontrados com sucesso',
            data={'movies': ListRentedMoviesResponseDto.from_model(rentals).__dict__},
        )

    def add_review(
        self, movie_id: str, user_id: str, add_review_request: AddReviewRequest
    ) -> Response:
        movie = self.movie_repository.find_by_id(movie_id)
        user = self.user_repository.find_by_id(user_id)

        if not user:
            raise CustomException(ApiErrorCodes.USER_NOT_FOUND)
        if not movie:
            raise CustomException(ApiErrorCodes.MOVIE_NOT_FOUND)

        rental = self.rental_repository.find_by_user_and_movie(
            user_id=user_id, movie_id=movie_id
        )

        if not rental:
            raise CustomException(
                ApiErrorCodes.TRY_REVIEW_NOT_RENTED_MOVIE,
                data={
                    'movie_id': movie_id,
                },
            )

        review = self.review_repository.find_by_user_and_movie(
            user_id=user_id, movie_id=movie_id
        )

        if review:
            raise CustomException(
                ApiErrorCodes.TRY_REVIEW_ALREADY_RATED_MOVIE,
                data={
                    'movie_id': movie_id,
                },
            )

        review = self.review_repository.create(
            user_id=user_id,
            movie_id=movie_id,
            rating=add_review_request.rating,
            comment=add_review_request.comment,
        )

        self.movie_repository.update_rating(movie, review.rating)

        return ApiResponse.send(
            message='Avaliação criada com sucesso',
            data=ReviewDto.from_model(review).__dict__,
        )
