from flask import Flask
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()


def register_extensions(app: Flask) -> None:
    """
    Register Flask extensions with the app.
    """
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
