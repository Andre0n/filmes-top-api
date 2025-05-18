from dataclasses import dataclass

from ..models import Movie


@dataclass
class MovieResponseDto:
    id: str
    title: str
    year: int

    @classmethod
    def from_model(cls, movie: Movie) -> 'MovieResponseDto':
        return cls(id=movie.id, title=movie.title, year=movie.year)


@dataclass
class ListMovieResponseDto:
    data: list[MovieResponseDto]

    @classmethod
    def from_model(cls, movies: list[Movie]) -> 'ListMovieResponseDto':
        return cls(
            data=[MovieResponseDto.from_model(movie) for movie in movies]
        )
