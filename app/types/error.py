from enum import Enum
from typing import Dict, List, Optional


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

    # Rental errors
    MOVIE_ALREADY_RENTED = 'MOVIE_ALREADY_RENTED'
    RENTAL_NOT_FOUND = 'RENTAL_NOT_FOUND'

    # Review errors
    TRY_REVIEW_NOT_RENTED_MOVIE = 'TRY_REVIEW_NOT_RENTED_MOVIE'
    TRY_REVIEW_ALREADY_RATED_MOVIE = 'TRY_REVIEW_ALREADY_RATED_MOVIE'


class ApiBaseError:
    def __init__(
        self, status: int, description: str, data: Optional[List[str]] = None
    ) -> None:
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
        description='Um usuário com esse e-mail já existe',
        data=[],
    ),
    ApiErrorCodes.USER_NOT_FOUND: ApiBaseError(
        status=404,
        description='Usuário não encontrado',
        data=[],
    ),
}

RentalErrors: Dict[ApiErrorCodes, ApiBaseError] = {
    ApiErrorCodes.MOVIE_ALREADY_RENTED: ApiBaseError(
        status=409,
        description='O filme já está alugado',
        data=[],
    ),
    ApiErrorCodes.RENTAL_NOT_FOUND: ApiBaseError(
        status=404,
        description='Alugel não encontrado',
        data=[],
    ),
}

ReviewErrors: Dict[ApiErrorCodes, ApiBaseError] = {
    ApiErrorCodes.TRY_REVIEW_NOT_RENTED_MOVIE: ApiBaseError(
        status=400,
        description='Tentativa de avaliar um filme que não foi alugado',
        data=[],
    ),
    ApiErrorCodes.TRY_REVIEW_ALREADY_RATED_MOVIE: ApiBaseError(
        status=409,
        description='Tentativa de avaliar um filme que já foi avaliado',
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
    **RentalErrors,
    **ReviewErrors,
}
