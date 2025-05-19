from __future__ import annotations

from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from ..extensions import db
from ..models.movie import Movie
from ..types.error import ApiErrorCodes
from ..utils.exceptions import CustomException


class MovieRepository:
    def find_all(
        self, skip: int | None = 0, limit: int | None = 100
    ) -> list[Movie]:
        try:
            movies = db.session.query(Movie).offset(skip).limit(limit).all()
            return movies
        except SQLAlchemyError as e:
            raise CustomException(
                ApiErrorCodes.INTERNAL_SERVER_ERROR, data={'errors': str(e)}
            ) from e
        except Exception as e:
            raise CustomException(
                ApiErrorCodes.INTERNAL_SERVER_ERROR, data={'errors': str(e)}
            ) from e

    def find_by_id(self, movie_id: str) -> Movie:
        try:
            movie = db.session.query(Movie).filter_by(id=movie_id).first()
            if not movie:
                raise CustomException(
                    ApiErrorCodes.MOVIE_NOT_FOUND, data={'movie_id': movie_id}
                )
            return movie
        except SQLAlchemyError as e:
            raise CustomException(
                ApiErrorCodes.INTERNAL_SERVER_ERROR, data={'errors': str(e)}
            ) from e
        except CustomException as e:
            raise e

    def find_by_title(
        self, title: str, skip: int | None = 0, limit: int | None = 100
    ) -> list[Movie]:
        try:
            query = db.session.query(Movie).filter(
                Movie.title.ilike(f'%{title}%')
            )
            movies = query.offset(skip).limit(limit).all()
            return movies
        except SQLAlchemyError as e:
            raise CustomException(
                ApiErrorCodes.INTERNAL_SERVER_ERROR, data={'errors': str(e)}
            ) from e
        except CustomException as e:
            raise e

    def find_by_genre(
        self, genre: str, skip: int | None = 0, limit: int | None = 100
    ) -> list[Movie]:
        try:
            query = db.session.query(Movie).filter(
                Movie.genre.ilike(f'%{genre}%')
            )
            movies = query.offset(skip).limit(limit).all()
            return movies
        except SQLAlchemyError as e:
            raise CustomException(
                ApiErrorCodes.INTERNAL_SERVER_ERROR, data={'errors': str(e)}
            ) from e

    def create(self, title: str, year: int) -> Movie:
        try:
            movie = Movie(title=title, year=year)
            db.session.add(movie)
            db.session.commit()
            return movie
        except IntegrityError as e:
            raise CustomException(
                ApiErrorCodes.MOVIE_TITLE_ALREADY_EXISTS, data={'title': title}
            ) from e
        except SQLAlchemyError as e:
            raise CustomException(
                ApiErrorCodes.ERROR_CREATING_MOVIE, data={'errors': str(e)}
            ) from e
