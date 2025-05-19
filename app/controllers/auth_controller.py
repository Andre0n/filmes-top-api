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
        """
        Register a new user
        ---
        tags:
          - Authentication
        description: Creates a new user account with the provided details
        consumes:
          - application/json
        produces:
          - application/json
        parameters:
          - in: body
            name: body
            description: User registration data
            required: true
            schema:
              $ref: '#/definitions/RegisterUserRequest'
        responses:
          201:
            description: User created successfully
            schema:
              $ref: '#/definitions/UserDto'
          400:
            $ref: '#/responses/ValidationError'
          409:
            description: User already exists
            schema:
              $ref: '#/definitions/ErrorResponse'
            examples:
              application/json:
                code: 409
                message: Um usuário com esse nome de usuário ou e-mail já existe
                data:
                  errors: USER_ALREADY_EXISTS
          500:
            $ref: '#/responses/InternalServerError'
        """
        return self.auth_service.create_user(body)


class LoginController(MethodView):
    def __init__(self) -> None:
        self.auth_service = AuthService(UserRepository())

    @validate_body(LoginUserRequest)
    def post(self, body: LoginUserRequest) -> Response:
        """
        Authenticate user
        ---
        tags:
          - Authentication
        description: Authenticates a user and returns an access token
        consumes:
          - application/json
        produces:
          - application/json
        parameters:
          - in: body
            name: body
            description: User credentials
            required: true
            schema:
              $ref: '#/definitions/LoginUserRequest'
        responses:
          200:
            description: Login successful
            schema:
              type: object
              properties:
                data:
                  type: object
                  properties:
                    access_token:
                      type: string
                      example: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
                    user:
                      $ref: '#/definitions/UserDto'
          400:
            $ref: '#/responses/ValidationError'
          401:
            description: Invalid credentials
            schema:
              $ref: '#/definitions/ErrorResponse'
            examples:
              application/json:
                code: 401
                message: E-mail ou senha incorretos
                data:
                  errors: EMAIL_OR_PASSWORD_INCORRECT
          500:
            $ref: '#/responses/InternalServerError'
        """
        return self.auth_service.login_user(body)
