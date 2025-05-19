from flask import Response
from flask.views import MethodView

from ..repositories.user_repository import UserRepository
from ..schemas.user.login_user_schema import LoginUserRequest
from ..schemas.user.register_user_schema import RegisterUserRequest
from ..services import AuthService
from ..validators.body_validator import validate_body


class RegisterController(MethodView):
    def __init__(self) -> None:
        self.auth_service = AuthService(UserRepository())

    @validate_body(RegisterUserRequest)
    def post(self, body: RegisterUserRequest) -> Response:
        return self.auth_service.create_user(body)


class LoginController(MethodView):
    def __init__(self) -> None:
        self.auth_service = AuthService(UserRepository())

    @validate_body(LoginUserRequest)
    def post(self, body: LoginUserRequest) -> Response:
        return self.auth_service.login_user(body)
