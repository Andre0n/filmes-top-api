from typing import Any, Dict, Optional, Union

from flask import Response, jsonify
from werkzeug.exceptions import HTTPException

from ..types.error import ApiBaseError, ApiErrorCodes, ApiErrors


class CustomException(HTTPException):
    def __init__(
        self,
        error_code: Union[ApiErrorCodes, int, None] = None,
        data: Optional[Dict[str, Any]] = None,
    ) -> None:
        error = self._resolve_error(error_code)
        message = self._format_message(error.description, data)

        self.code = error.status
        self.description = message
        self.response: Response = jsonify(
            {'code': error.status, 'message': message, 'data': data or {}}
        )

        self.response.status_code = self.code

    def _resolve_error(
        self, error_code: Union[ApiErrorCodes, int, None]
    ) -> ApiBaseError:
        if isinstance(error_code, ApiErrorCodes):
            return ApiErrors.get(
                error_code, ApiErrors[ApiErrorCodes.INTERNAL_SERVER_ERROR]
            )
        elif isinstance(error_code, int):
            return ApiBaseError(
                error_code, 'Ocorreu um erro ao processar a requisição', []
            )
        return ApiErrors[ApiErrorCodes.INTERNAL_SERVER_ERROR]

    def _format_message(
        self, template: str, data: Optional[Dict[str, Any]]
    ) -> str:
        if not data:
            return template

        try:
            return template.format(**data)
        except KeyError:
            message = template
            for key, value in data.items():
                message = message.replace(f'{{{key}}}', str(value))
            return message
