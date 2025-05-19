from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError

from ..extensions import db
from ..models import User
from ..types.error import ApiErrorCodes
from ..utils.exceptions import CustomException


class UserRepository:
    def create(
        self, username: str, name: str, email: str, password: str
    ) -> User:
        try:
            existing_user = (
                db.session.query(User)
                .filter(or_(User.username == username, User.email == email))
                .first()
            )

            if existing_user:
                if existing_user.username == username:
                    raise CustomException(
                        ApiErrorCodes.USER_NAME_ALREADY_EXISTS
                    )
                if existing_user.email == email:
                    raise CustomException(
                        ApiErrorCodes.USER_EMAIL_ALREADY_EXISTS
                    )
            user = User(
                username=username,
                name=name,
                email=email,
                password=password,
            )
            db.session.add(user)
            db.session.commit()
            return user

        except CustomException as e:
            db.session.rollback()
            raise e

        except IntegrityError as e:
            db.session.rollback()
            raise CustomException(ApiErrorCodes.USER_ALREADY_EXISTS) from e

    def find_by_email(self, email: str) -> User:
        try:
            user = db.session.query(User).filter_by(email=email).first()
            if not user:
                raise CustomException(ApiErrorCodes.USER_NOT_FOUND)
            return user
        except CustomException as e:
            db.session.rollback()
            raise e
        except Exception as e:
            db.session.rollback()
            raise CustomException(
                ApiErrorCodes.INTERNAL_SERVER_ERROR, data={'error': str(e)}
            ) from e
