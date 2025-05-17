from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db = SQLAlchemy()
migrate = Migrate()


def register_extensions(app: Flask) -> None:
    """
    Register Flask extensions with the app.
    """
    db.init_app(app)
    migrate.init_app(app, db)
