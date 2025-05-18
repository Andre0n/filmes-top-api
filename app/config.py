import os
from typing import Dict, Literal, Type

from dotenv import load_dotenv

load_dotenv()


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    API_TITLE = 'FilmesTop API'
    API_VERSION = 'v1'


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


EnvironmentType = Literal['development', 'production', 'test']
config: Dict[EnvironmentType, Type[Config]] = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
}
