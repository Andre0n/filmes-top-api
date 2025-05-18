from flask import Flask

from .blueprints.api_blueprint import api_blueprint
from .config import EnvironmentType, config
from .extensions import register_extensions
from .models import *


def create_app(config_name: EnvironmentType = 'development') -> Flask:
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    register_extensions(app)

    app.register_blueprint(api_blueprint)

    return app
