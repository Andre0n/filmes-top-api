from flasgger import Swagger  # pyright: ignore
from flask import Flask

from .blueprints.api_blueprint import api_blueprint
from .config import config
from .extensions import register_extensions
from .models import *
from .utils.api_docs import init_swagger
from .utils.error_handlers import handle_exception


def create_app(config_name: str = 'development') -> Flask:
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    register_extensions(app)
    init_swagger(app)

    app.register_blueprint(api_blueprint)
    app.register_error_handler(Exception, handle_exception)

    return app
