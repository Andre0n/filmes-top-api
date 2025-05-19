from dataclasses import dataclass, field
from typing import List

from ..models import Movie, Rental
from .review_dto import ListReviewResponseDto


@dataclass
class MovieResponseDto:
    id: str
    title: str
    year: int
    created_at: str | None = None
    description: str | None = None
    duration_minutes: int | None = None
    genre: str | None = None
    total_reviews: int | None = None
    average_rating: float | None = None
    rented_at: str | None = None

    reviews: ListReviewResponseDto = field(
        default_factory=ListReviewResponseDto
    )

    @classmethod
    def from_model(
        cls, movie: Movie, rented_at: str | None = None
    ) -> 'MovieResponseDto':
        return cls(
            id=movie.id,
            title=movie.title,
            year=movie.year,
            created_at=movie.created_at.isoformat(),
            description=movie.description,
            duration_minutes=movie.duration_minutes,
            genre=movie.genre,
            total_reviews=movie.total_reviews,
            average_rating=movie.average_rating,
            rented_at=rented_at,
            reviews=ListReviewResponseDto.from_model(movie.reviews),
        )


@dataclass
class ListMovieResponseDto:
    data: List[MovieResponseDto]

    @classmethod
    def from_model(cls, movies: list[Movie]) -> 'ListMovieResponseDto':
        return cls(
            data=[MovieResponseDto.from_model(movie) for movie in movies]
        )


@dataclass
class ListRentedMoviesResponseDto:
    data: List[MovieResponseDto]

    @classmethod
    def from_model(
        cls, rentals: List[Rental]
    ) -> 'ListRentedMoviesResponseDto':
        return cls(
            data=[
                MovieResponseDto.from_model(
                    rental.movie, rented_at=rental.rented_at.isoformat()
                )
                for rental in rentals
            ]
        )
