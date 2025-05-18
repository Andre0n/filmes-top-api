from flask import Response, jsonify

from ..dtos.movie_dto import ListMovieResponseDto, MovieResponseDto
from ..repositories.movies_repository import MovieRepository
from ..schemas.movie.get_movie_request_schema import GetMovieRequest
from ..schemas.movie.create_movie_schema import CreateMovieRequest


class MovieService:
    def __init__(self, movie_repository: MovieRepository):
        self.movie_repository = movie_repository

    def get_movies(self, get_movie_request: GetMovieRequest) -> Response:
        if get_movie_request.search:
            movies = self.movie_repository.find_by_title(
                get_movie_request.search
            )
            return jsonify(ListMovieResponseDto.from_model(movies).__dict__)

        movies = self.movie_repository.find_all(
            get_movie_request.page, get_movie_request.limit
        )
        return jsonify(ListMovieResponseDto.from_model(movies).__dict__)

    def get_movie(self, movie_id: str) -> Response:
        movie = self.movie_repository.find_by_id(movie_id)
        return jsonify(MovieResponseDto.from_model(movie).__dict__)

    def create_movie(
        self, create_movie_request: CreateMovieRequest
    ) -> Response:
        movie = self.movie_repository.create(
            title=create_movie_request.title, year=create_movie_request.year
        )
        return jsonify(MovieResponseDto.from_model(movie).__dict__)
