from flask import Flask

from .config import config, EnvironmentType


def create_app(config_name: EnvironmentType = 'development') -> Flask:
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    return app
