import os
from typing import Dict, Literal, Type

from dotenv import load_dotenv

load_dotenv()


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    API_TITLE = 'FilmesTop API'
    API_VERSION = 'v1'
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = 3600  # 1 hour
    JWT_REFRESH_TOKEN_EXPIRES = 604800  # 7 days


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


EnvironmentType = Literal['development', 'production', 'test']
config: Dict[EnvironmentType, Type[Config]] = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
}
