from typing import Any

from flask import Response, make_response


class ApiResponse:
    @staticmethod
    def send(
        status_code: int = 200, message: str = '', data: Any = None
    ) -> Response:
        return make_response(
            {
                'code': status_code,
                'message': message,
                'data': data,
            },
            status_code,
        )
