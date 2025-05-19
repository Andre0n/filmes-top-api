from datetime import datetime
from typing import List

from sqlalchemy.exc import IntegrityError

from ..extensions import db
from ..models import Rental
from ..types.error import ApiErrorCodes
from ..utils.exceptions import CustomException


class RentalRepository:
    def create(
        self, user_id: str, movie_id: str, expiration_date: datetime
    ) -> Rental:
        try:
            rental = Rental(
                user_id=user_id,
                movie_id=movie_id,
                expires_at=expiration_date,
            )
            db.session.add(rental)
            db.session.commit()
            return rental
        except CustomException as e:
            db.session.rollback()
            raise e
        except IntegrityError as e:
            db.session.rollback()
            raise CustomException(ApiErrorCodes.USER_ALREADY_EXISTS) from e

    def find_by_user_id(self, user_id: str) -> List[Rental]:
        return db.session.query(Rental).filter_by(user_id=user_id).all()

    def find_by_movie_id(self, movie_id: str) -> List[Rental]:
        return db.session.query(Rental).filter_by(movie_id=movie_id).all()

    def find_by_user_and_movie(
        self, user_id: str, movie_id: str
    ) -> Rental | None:
        return (
            db.session.query(Rental)
            .filter_by(user_id=user_id, movie_id=movie_id)
            .first()
        )
