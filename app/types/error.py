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


class ApiBaseError:
    def __init__(self, status: int, description: str, data: List[str]) -> None:
        self.status = status
        self.description = description
        self.data = data


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
}
