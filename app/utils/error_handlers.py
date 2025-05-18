from flask import Response
from werkzeug.exceptions import HTTPException

from ..utils.exceptions import CustomException


def handle_exception(e: Exception) -> Response:
    if isinstance(e, CustomException):
        return e.response

    if isinstance(e, HTTPException):
        return CustomException(
            error_code=e.code,
            data={'errors': e.description},
        ).response

    return CustomException(data={'erors': str(e)}).response
