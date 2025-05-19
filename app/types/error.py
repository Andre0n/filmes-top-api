from enum import Enum
from typing import Dict, List


class ApiErrorCodes(str, Enum):
    # General errors
    INTERNAL_SERVER_ERROR = 'INTERNAL_SERVER_ERROR'

    # Movie errors
    MOVIE_TITLE_ALREADY_EXISTS = 'MOVIE_TITLE_ALREADY_EXISTS'
    ERROR_CREATING_MOVIE = 'ERROR_CREATING_MOVIE'
    MOVIE_NOT_FOUND = 'MOVIE_NOT_FOUND'

    # Validation errors
    VALIDATION_ERROR = 'VALIDATION_ERROR'

    # User errors
    USER_ALREADY_EXISTS = 'USER_ALREADY_EXISTS'
    USER_NAME_ALREADY_EXISTS = 'USER_NAME_ALREADY_EXISTS'
    USER_EMAIL_ALREADY_EXISTS = 'USER_EMAIL_ALREADY_EXISTS'
    USER_NOT_FOUND = 'USER_NOT_FOUND'

    # Authentication errors
    EMAIL_OR_PASSWORD_INCORRECT = 'EMAIL_OR_PASSWORD_INCORRECT'
    USER_NOT_AUTHENTICATED = 'USER_NOT_AUTHENTICATED'


class ApiBaseError:
    def __init__(self, status: int, description: str, data: List[str]) -> None:
        self.status = status
        self.description = description
        self.data = data


UserErrors: Dict[ApiErrorCodes, ApiBaseError] = {
    ApiErrorCodes.USER_ALREADY_EXISTS: ApiBaseError(
        status=409,
        description='Um usuário com esse nome de usuário ou e-mail já existe',
        data=[],
    ),
    ApiErrorCodes.USER_NAME_ALREADY_EXISTS: ApiBaseError(
        status=409,
        description='Nome de usuário já existe',
        data=[],
    ),
    ApiErrorCodes.USER_EMAIL_ALREADY_EXISTS: ApiBaseError(
        status=409,
        description='E-mail já existe',
        data=[],
    ),
    ApiErrorCodes.USER_NOT_FOUND: ApiBaseError(
        status=404,
        description='Usuário não encontrado',
        data=[],
    ),
}

AuthErrors: Dict[ApiErrorCodes, ApiBaseError] = {
    ApiErrorCodes.EMAIL_OR_PASSWORD_INCORRECT: ApiBaseError(
        status=401,
        description='E-mail ou senha incorretos',
        data=[],
    ),
    ApiErrorCodes.USER_NOT_AUTHENTICATED: ApiBaseError(
        status=401,
        description='Usuário não autenticado',
        data=[],
    ),
}

ApiErrors: Dict[ApiErrorCodes, ApiBaseError] = {
    ApiErrorCodes.INTERNAL_SERVER_ERROR: ApiBaseError(
        status=500, description='Erro interno no servidor', data=[]
    ),
    ApiErrorCodes.MOVIE_TITLE_ALREADY_EXISTS: ApiBaseError(
        status=409,
        description='Um filme com esse título já existe',
        data=[],
    ),
    ApiErrorCodes.ERROR_CREATING_MOVIE: ApiBaseError(
        status=500,
        description='Erro ao criar filme',
        data=[],
    ),
    ApiErrorCodes.VALIDATION_ERROR: ApiBaseError(
        status=400,
        description='Ocorreu um erro de validação',
        data=[],
    ),
    ApiErrorCodes.MOVIE_NOT_FOUND: ApiBaseError(
        status=404,
        description='Filme não encontrado',
        data=[],
    ),
    **UserErrors,
    **AuthErrors,
}
