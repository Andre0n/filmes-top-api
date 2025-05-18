from enum import Enum
from typing import Dict, List


class ApiErrorCodes(str, Enum):
    INTERNAL_SERVER_ERROR = 'INTERNAL_SERVER_ERROR'
    MOVIE_TITLE_ALREADY_EXISTS = 'MOVIE_TITLE_ALREADY_EXISTS'
    ERROR_CREATING_MOVIE = 'ERROR_CREATING_MOVIE'


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
        status=400,
        description='Um filme com esse título já existe',
        data=[],
    ),
    ApiErrorCodes.ERROR_CREATING_MOVIE: ApiBaseError(
        status=500,
        description='Erro ao criar filme',
        data=[],
    ),
}
