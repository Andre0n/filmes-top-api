from functools import wraps
from typing import Any, Callable, Type, TypeVar

from flask import Response, request
from pydantic import BaseModel, ValidationError

from ..types.error import ApiErrorCodes
from ..utils.exceptions import CustomException

T = TypeVar('T', bound=BaseModel)


def validate_body(
    model_class: Type[T],
    body_key: str = 'body',
) -> Callable[[Callable[..., Response]], Callable[..., Response]]:
    def decorator(func: Callable[..., Response]) -> Callable[..., Response]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Response:
            try:
                data = request.get_json(force=True)
                validated_data = model_class(**data)
                kwargs[body_key] = validated_data
                return func(*args, **kwargs)
            except ValidationError as e:
                raise CustomException(
                    ApiErrorCodes.VALIDATION_ERROR,
                    data={
                        'errors': e.errors(
                            include_context=False,
                            include_input=False,
                            include_url=False,
                        ),
                    },
                ) from e

        return wrapper

    return decorator
