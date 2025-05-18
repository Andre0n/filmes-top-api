from typing import Any, Dict, Optional

from flask import jsonify
from werkzeug.exceptions import HTTPException

from ..types.error import ApiErrorCodes, ApiErrors


class CustomException(HTTPException):
    def __init__(
        self,
        error_code: ApiErrorCodes,
        data: Optional[Dict[str, Any]] = None,
    ) -> None:
        error = ApiErrors.get(
            error_code, ApiErrors[ApiErrorCodes.INTERNAL_SERVER_ERROR]
        )
        message = error.description

        if data:
            for key, value in data.items():
                placeholder = f'{{{key}}}'
                message = message.replace(placeholder, str(value))

        self.code = error.status
        self.description = message
        self.response = jsonify(
            {'code': error_code, 'message': message, 'data': data or {}}
        )
        self.response.status_code = self.code
