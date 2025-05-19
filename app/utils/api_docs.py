from typing import Any, Dict

from flasgger import Swagger  # type: ignore
from flask import Flask

swagger_template: Dict[str, Any] = {
    'swagger': '2.0',
    'info': {
        'title': 'FimesTop API',
        'description': 'API for managing movies, reviews, and user authentication',
        'version': '1.0',
    },
    'basePath': '/api/',
    'schemes': ['http', 'https'],
    'consumes': ['application/json'],
    'produces': ['application/json'],
    'securityDefinitions': {
        'BearerAuth': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header',
            'description': 'JWT Authorization header using the Bearer scheme. Example: "Bearer {token}"',
        }
    },
    'definitions': {
        'LoginUserRequest': {
            'type': 'object',
            'required': ['email', 'password'],
            'properties': {
                'email': {
                    'type': 'string',
                    'format': 'email',
                    'example': 'john@example.com',
                    'description': 'The email of the user',
                },
                'password': {
                    'type': 'string',
                    'minLength': 8,
                    'maxLength': 20,
                    'example': 'securepassword123',
                },
            },
        },
        'RegisterUserRequest': {
            'type': 'object',
            'required': ['username', 'email', 'password', 'name'],
            'properties': {
                'username': {
                    'type': 'string',
                    'minLength': 3,
                    'maxLength': 50,
                    'example': 'johndoe',
                },
                'email': {
                    'type': 'string',
                    'format': 'email',
                    'example': 'user@example.com',
                },
                'password': {
                    'type': 'string',
                    'minLength': 8,
                    'maxLength': 128,
                    'example': 'securepassword123',
                },
                'name': {
                    'type': 'string',
                    'minLength': 3,
                    'maxLength': 50,
                    'example': 'John Doe',
                },
            },
        },
        'UserDto': {
            'type': 'object',
            'properties': {
                'id': {
                    'type': 'string',
                    'example': '550e8400-e29b-41d4-a716-446655440000',
                    'nullable': True,
                },
                'username': {'type': 'string', 'example': 'johndoe'},
                'email': {
                    'type': 'string',
                    'format': 'email',
                    'example': 'john@example.com',
                },
                'name': {'type': 'string', 'example': 'John Doe'},
                'created_at': {
                    'type': 'string',
                    'format': 'date-time',
                    'example': '2023-01-01T00:00:00Z',
                    'nullable': True,
                },
                'updated_at': {
                    'type': 'string',
                    'format': 'date-time',
                    'example': '2023-01-01T00:00:00Z',
                    'nullable': True,
                },
            },
        },
        'CreateMovieRequest': {
            'type': 'object',
            'required': ['title', 'year', 'genre', 'duration'],
            'properties': {
                'title': {
                    'type': 'string',
                    'minLength': 1,
                    'maxLength': 100,
                    'example': 'Inception',
                },
                'year': {
                    'type': 'integer',
                    'minimum': 1889,
                    'maximum': 2099,
                    'example': 2010,
                },
                'genre': {
                    'type': 'string',
                    'minLength': 1,
                    'maxLength': 50,
                    'example': 'Sci-Fi',
                },
                'duration': {'type': 'integer', 'minimum': 1, 'example': 148},
            },
        },
        'AddReviewRequest': {
            'type': 'object',
            'required': ['rating'],
            'properties': {
                'rating': {
                    'type': 'number',
                    'format': 'float',
                    'minimum': 0,
                    'maximum': 10,
                    'example': 8.5,
                },
                'comment': {
                    'type': 'string',
                    'maxLength': 500,
                    'example': 'Great movie!',
                    'nullable': True,
                },
            },
        },
        'GetMovieRequest': {
            'type': 'object',
            'properties': {
                'page': {
                    'type': 'integer',
                    'minimum': 1,
                    'default': 1,
                    'example': 1,
                },
                'limit': {
                    'type': 'integer',
                    'minimum': 1,
                    'maximum': 100,
                    'default': 100,
                    'example': 10,
                },
                'search': {
                    'type': 'string',
                    'maxLength': 100,
                    'nullable': True,
                    'example': 'Inception',
                },
                'genre': {
                    'type': 'string',
                    'maxLength': 50,
                    'nullable': True,
                    'example': 'Sci-Fi',
                },
                'rented': {
                    'type': 'boolean',
                    'nullable': True,
                    'description': 'Filter by rented status',
                    'example': True,
                },
            },
        },
        'MovieResponse': {
            'type': 'object',
            'properties': {
                'id': {
                    'type': 'string',
                    'example': '550e8400-e29b-41d4-a716-446655440000',
                },
                'title': {'type': 'string', 'example': 'Inception'},
                'year': {'type': 'integer', 'example': 2010},
                'created_at': {
                    'type': 'string',
                    'format': 'date-time',
                    'example': '2023-01-01T00:00:00Z',
                    'nullable': True,
                },
                'description': {
                    'type': 'string',
                    'example': 'A thief who steals corporate secrets...',
                    'nullable': True,
                },
                'duration_minutes': {
                    'type': 'integer',
                    'example': 148,
                    'nullable': True,
                },
                'genre': {
                    'type': 'string',
                    'example': 'Sci-Fi',
                    'nullable': True,
                },
                'total_reviews': {
                    'type': 'integer',
                    'example': 5,
                    'nullable': True,
                },
                'average_rating': {
                    'type': 'number',
                    'format': 'float',
                    'example': 8.5,
                    'nullable': True,
                },
                'rented_at': {
                    'type': 'string',
                    'format': 'date-time',
                    'example': '2023-01-01T00:00:00Z',
                    'nullable': True,
                },
                'reviews': {'$ref': '#/definitions/ListReviewResponseDto'},
            },
        },
        'ListMovieResponseDto': {
            'type': 'object',
            'properties': {
                'data': {
                    'type': 'array',
                    'items': {'$ref': '#/definitions/MovieResponse'},
                }
            },
        },
        'ListRentedMoviesResponseDto': {
            'type': 'object',
            'properties': {
                'data': {
                    'type': 'array',
                    'items': {'$ref': '#/definitions/MovieResponse'},
                }
            },
        },
        'ReviewDto': {
            'type': 'object',
            'properties': {
                'id': {'type': 'integer', 'example': 1, 'nullable': True},
                'created_at': {
                    'type': 'string',
                    'format': 'date-time',
                    'example': '2023-01-01T00:00:00Z',
                    'nullable': True,
                },
                'rating': {
                    'type': 'number',
                    'format': 'float',
                    'example': 8.5,
                },
                'comment': {
                    'type': 'string',
                    'example': 'Great movie!',
                    'nullable': True,
                },
                'user_name': {
                    'type': 'string',
                    'example': 'John Doe',
                    'nullable': True,
                },
            },
        },
        'ListReviewResponseDto': {
            'type': 'object',
            'properties': {
                'data': {
                    'type': 'array',
                    'items': {'$ref': '#/definitions/ReviewDto'},
                }
            },
        },
        'ApiResponse': {
            'type': 'object',
            'properties': {
                'code': {'type': 'integer', 'example': 200},
                'message': {'type': 'string', 'example': 'Success'},
                'data': {'type': 'object', 'additionalProperties': True},
            },
        },
        'ErrorResponse': {
            'type': 'object',
            'properties': {
                'code': {'type': 'integer', 'example': 404},
                'message': {'type': 'string', 'example': 'Movie not found'},
                'data': {
                    'type': 'object',
                    'properties': {
                        'errors': {
                            'type': 'string',
                            'example': 'MOVIE_NOT_FOUND',
                        }
                    },
                },
            },
        },
        'ErrorCodes': {
            'type': 'string',
            'enum': [
                'INTERNAL_SERVER_ERROR',
                'MOVIE_TITLE_ALREADY_EXISTS',
                'ERROR_CREATING_MOVIE',
                'MOVIE_NOT_FOUND',
                'VALIDATION_ERROR',
                'USER_ALREADY_EXISTS',
                'USER_NAME_ALREADY_EXISTS',
                'USER_EMAIL_ALREADY_EXISTS',
                'USER_NOT_FOUND',
                'EMAIL_OR_PASSWORD_INCORRECT',
                'USER_NOT_AUTHENTICATED',
                'MOVIE_ALREADY_RENTED',
                'RENTAL_NOT_FOUND',
                'TRY_REVIEW_NOT_RENTED_MOVIE',
                'TRY_REVIEW_ALREADY_RATED_MOVIE',
            ],
            'description': 'Possible error codes returned by the API',
        },
        'GeneralErrors': {
            'description': 'General error responses',
            'type': 'object',
            'properties': {
                'INTERNAL_SERVER_ERROR': {
                    'type': 'object',
                    'properties': {
                        'code': {'type': 'integer', 'example': 500},
                        'message': {
                            'type': 'string',
                            'example': 'Erro interno no servidor',
                        },
                    },
                },
                'VALIDATION_ERROR': {
                    'type': 'object',
                    'properties': {
                        'code': {'type': 'integer', 'example': 400},
                        'message': {
                            'type': 'string',
                            'example': 'Ocorreu um erro de validação',
                        },
                    },
                },
            },
        },
        'MovieErrors': {
            'description': 'Movie related error responses',
            'type': 'object',
            'properties': {
                'MOVIE_TITLE_ALREADY_EXISTS': {
                    'type': 'object',
                    'properties': {
                        'code': {'type': 'integer', 'example': 409},
                        'message': {
                            'type': 'string',
                            'example': 'Um filme com esse título já existe',
                        },
                    },
                },
                'ERROR_CREATING_MOVIE': {
                    'type': 'object',
                    'properties': {
                        'code': {'type': 'integer', 'example': 500},
                        'message': {
                            'type': 'string',
                            'example': 'Erro ao criar filme',
                        },
                    },
                },
                'MOVIE_NOT_FOUND': {
                    'type': 'object',
                    'properties': {
                        'code': {'type': 'integer', 'example': 404},
                        'message': {
                            'type': 'string',
                            'example': 'Filme não encontrado',
                        },
                    },
                },
            },
        },
        'UserErrors': {
            'description': 'User related error responses',
            'type': 'object',
            'properties': {
                'USER_ALREADY_EXISTS': {
                    'type': 'object',
                    'properties': {
                        'code': {'type': 'integer', 'example': 409},
                        'message': {
                            'type': 'string',
                            'example': 'Um usuário com esse nome de usuário ou e-mail já existe',
                        },
                    },
                },
                'USER_NAME_ALREADY_EXISTS': {
                    'type': 'object',
                    'properties': {
                        'code': {'type': 'integer', 'example': 409},
                        'message': {
                            'type': 'string',
                            'example': 'Nome de usuário já existe',
                        },
                    },
                },
                'USER_EMAIL_ALREADY_EXISTS': {
                    'type': 'object',
                    'properties': {
                        'code': {'type': 'integer', 'example': 409},
                        'message': {
                            'type': 'string',
                            'example': 'E-mail já existe',
                        },
                    },
                },
                'USER_NOT_FOUND': {
                    'type': 'object',
                    'properties': {
                        'code': {'type': 'integer', 'example': 404},
                        'message': {
                            'type': 'string',
                            'example': 'Usuário não encontrado',
                        },
                    },
                },
            },
        },
        'AuthErrors': {
            'description': 'Authentication related error responses',
            'type': 'object',
            'properties': {
                'EMAIL_OR_PASSWORD_INCORRECT': {
                    'type': 'object',
                    'properties': {
                        'code': {'type': 'integer', 'example': 401},
                        'message': {
                            'type': 'string',
                            'example': 'E-mail ou senha incorretos',
                        },
                    },
                },
                'USER_NOT_AUTHENTICATED': {
                    'type': 'object',
                    'properties': {
                        'code': {'type': 'integer', 'example': 401},
                        'message': {
                            'type': 'string',
                            'example': 'Usuário não autenticado',
                        },
                    },
                },
            },
        },
        'RentalErrors': {
            'description': 'Rental related error responses',
            'type': 'object',
            'properties': {
                'MOVIE_ALREADY_RENTED': {
                    'type': 'object',
                    'properties': {
                        'code': {'type': 'integer', 'example': 409},
                        'message': {
                            'type': 'string',
                            'example': 'O filme já está alugado',
                        },
                    },
                },
                'RENTAL_NOT_FOUND': {
                    'type': 'object',
                    'properties': {
                        'code': {'type': 'integer', 'example': 404},
                        'message': {
                            'type': 'string',
                            'example': 'Aluguel não encontrado',
                        },
                    },
                },
            },
        },
        'ReviewErrors': {
            'description': 'Review related error responses',
            'type': 'object',
            'properties': {
                'TRY_REVIEW_NOT_RENTED_MOVIE': {
                    'type': 'object',
                    'properties': {
                        'code': {'type': 'integer', 'example': 400},
                        'message': {
                            'type': 'string',
                            'example': 'Tentativa de avaliar um filme que não foi alugado',
                        },
                    },
                },
                'TRY_REVIEW_ALREADY_RATED_MOVIE': {
                    'type': 'object',
                    'properties': {
                        'code': {'type': 'integer', 'example': 409},
                        'message': {
                            'type': 'string',
                            'example': 'Tentativa de avaliar um filme que já foi avaliado',
                        },
                    },
                },
            },
        },
    },
    'responses': {
        'InternalServerError': {
            'description': 'Internal server error',
            'schema': {'$ref': '#/definitions/ErrorResponse'},
            'examples': {
                'application/json': {
                    'code': 500,
                    'message': 'Erro interno no servidor',
                    'data': {},
                }
            },
        },
        'ValidationError': {
            'description': 'Validation error',
            'schema': {'$ref': '#/definitions/ErrorResponse'},
            'examples': {
                'application/json': {
                    'code': 400,
                    'message': 'Ocorreu um erro de validação',
                    'data': {
                        'errors': [
                            {
                                'loc': ['genre'],
                                'msg': 'Field required',
                                'type': 'missing',
                            }
                        ]
                    },
                }
            },
        },
        'NotFound': {
            'description': 'Resource not found',
            'schema': {'$ref': '#/definitions/ErrorResponse'},
            'examples': {
                'application/json': {
                    'code': 404,
                    'message': 'Recurso não encontrado',
                    'data': {},
                }
            },
        },
        'Unauthorized': {
            'description': 'Unauthorized access',
            'schema': {'$ref': '#/definitions/ErrorResponse'},
            'examples': {
                'application/json': {
                    'code': 401,
                    'message': 'Usuário não autenticado',
                    'data': {},
                }
            },
        },
        'Conflict': {
            'description': 'Resource conflict',
            'schema': {'$ref': '#/definitions/ErrorResponse'},
            'examples': {
                'application/json': {
                    'code': 409,
                    'message': 'Conflito de recurso',
                    'data': {},
                }
            },
        },
    },
}


def init_swagger(app: Flask) -> Swagger:
    return Swagger(app, template=swagger_template)
