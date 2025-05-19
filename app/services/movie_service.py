from datetime import datetime, timedelta

from flask import Response

from app.types.error import ApiErrorCodes
from app.utils.exceptions import CustomException

from ..dtos.movie_dto import ListMovieResponseDto, MovieResponseDto
from ..repositories.movies_repository import MovieRepository
from ..repositories.rental_repository import RentalRepository
from ..repositories.user_repository import UserRepository
from ..schemas.movie.create_movie_schema import CreateMovieRequest
from ..schemas.movie.get_movie_request_schema import GetMovieRequest
from ..utils.api_response import ApiResponse


class MovieService:
    def __init__(
        self,
        movie_repository: MovieRepository,
        user_repository: UserRepository,
        rental_repository: RentalRepository,
    ):
        self.movie_repository = movie_repository
        self.user_repository = user_repository
        self.rental_repository = rental_repository

    def get_movies(
        self, get_movie_request: GetMovieRequest, user_id: str = ''
    ) -> Response:
        if get_movie_request.search:
            movies = self.movie_repository.find_by_title(
                get_movie_request.search
            )
            return ApiResponse.send(
                status_code=200,
                data=ListMovieResponseDto.from_model(movies).__dict__,
            )

        if get_movie_request.genre:
            movies = self.movie_repository.find_by_genre(
                get_movie_request.genre
            )
            return ApiResponse.send(
                status_code=200,
                data=ListMovieResponseDto.from_model(movies).__dict__,
            )

        page = get_movie_request.page or 1
        page_size = get_movie_request.limit or 100
        movies = self.movie_repository.find_all(
            (page - 1) * page_size, page_size
        )
        return ApiResponse.send(
            data=ListMovieResponseDto.from_model(movies).__dict__
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
            status_code=200,
            message='Filme alugado com sucesso',
        )

    def get_rented_movies(self, user_id: str) -> Response:
        user = self.user_repository.find_by_id(user_id)

        if not user:
            raise CustomException(ApiErrorCodes.USER_NOT_FOUND)

        rentals = self.rental_repository.find_by_user_id(user_id)
        if not rentals:
            return ApiResponse.send(
                status_code=200,
                message='Nenhum filme alugado encontrado',
                data=[],
            )

        rented_movies = [
            MovieResponseDto.from_model(rental.movie).__dict__
            for rental in rentals
        ]

        return ApiResponse.send(
            status_code=200,
            message='Filmes alugados encontrados com sucesso',
            data=rented_movies,
        )
