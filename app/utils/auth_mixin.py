from flask_jwt_extended import get_jwt_identity, jwt_required  # pyright: ignore


class AuthMixin:
    @property
    @jwt_required()
    def user_id(self) -> str:
        return get_jwt_identity()
