from flask import Response
from flask_jwt_extended import create_access_token  # pyright: ignore
from werkzeug.security import check_password_hash, generate_password_hash

from app.types.error import ApiErrorCodes
from app.utils.exceptions import CustomException

from ..dtos.user_dto import UserDto
from ..repositories.user_repository import UserRepository
from ..schemas.user.login_user_schema import LoginUserRequest
from ..schemas.user.register_user_schema import RegisterUserRequest
from ..utils.api_response import ApiResponse


class AuthService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def create_user(
        self, register_user_request: RegisterUserRequest
    ) -> Response:
        username = register_user_request.username
        name = register_user_request.name
        email = register_user_request.email
        password = register_user_request.password

        hashed_password = generate_password_hash(password)

        user = self.user_repository.create(
            username, name, email, hashed_password
        )

        return ApiResponse.send(
            201,
            'Usuário criado com sucesso',
            data=UserDto.from_model(user).__dict__,
        )

    def login_user(self, login_user_request: LoginUserRequest) -> Response:
        email = login_user_request.email
        password = login_user_request.password

        user = self.user_repository.find_by_email(email)

        if not user or not check_password_hash(user.password, password):
            raise CustomException(ApiErrorCodes.EMAIL_OR_PASSWORD_INCORRECT)

        access_token = create_access_token(identity=user.id)
        return ApiResponse.send(
            200,
            data={
                'access_token': access_token,
            },
        )
