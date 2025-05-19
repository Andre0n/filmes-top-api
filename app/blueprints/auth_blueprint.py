from flask import Blueprint

from ..controllers import LoginController, RegisterController

auth_blueprint = Blueprint('auth', __name__)

auth_blueprint.add_url_rule(
    '/register',
    view_func=RegisterController.as_view('register_view'),
    methods=['POST'],
)

auth_blueprint.add_url_rule(
    '/login',
    view_func=LoginController.as_view('login_view'),
    methods=['POST'],
)
