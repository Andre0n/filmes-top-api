from dataclasses import dataclass

from ..models import Movie


@dataclass
class MovieResponseDto:
    id: str
    title: str
    year: int
    created_at: str | None = None
    updated_at: str | None = None
    description: str | None = None
    duration_minutes: int | None = None

    @classmethod
    def from_model(cls, movie: Movie) -> 'MovieResponseDto':
        return cls(
            id=movie.id,
            title=movie.title,
            year=movie.year,
            created_at=movie.created_at.isoformat(),
            updated_at=movie.updated_at.isoformat(),
            description=movie.description,
            duration_minutes=movie.duration_minutes,
        )


@dataclass
class ListMovieResponseDto:
    data: list[MovieResponseDto]

    @classmethod
    def from_model(cls, movies: list[Movie]) -> 'ListMovieResponseDto':
        return cls(
            data=[MovieResponseDto.from_model(movie) for movie in movies]
        )
