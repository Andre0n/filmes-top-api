from flask import Response

from ..dtos.movie_dto import ListMovieResponseDto, MovieResponseDto
from ..repositories.movies_repository import MovieRepository
from ..schemas.movie.create_movie_schema import CreateMovieRequest
from ..schemas.movie.get_movie_request_schema import GetMovieRequest
from ..utils.api_response import ApiResponse


class MovieService:
    def __init__(self, movie_repository: MovieRepository):
        self.movie_repository = movie_repository

    def get_movies(self, get_movie_request: GetMovieRequest) -> Response:
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
        movie = self.movie_repository.create(
            title=create_movie_request.title, year=create_movie_request.year
        )
        return ApiResponse.send(
            status_code=201,
            message='Filme criado com sucesso',
            data=MovieResponseDto.from_model(movie).__dict__,
        )
