from flask import Flask, Response, jsonify
from flask_cors import CORS

from auth0_poc.errors import AuthError
from auth0_poc.views import api
from settings import settings


def create_app() -> Flask:
    app = Flask("auth0_poc")
    app.secret_key = settings.session_key
    CORS(app)

    @app.errorhandler(AuthError)
    def handle_auth_error(error: AuthError) -> Response:
        response = jsonify({"code": error.code, "message": error.message})
        response.status_code = error.status_code
        return response

    app.register_blueprint(api)

    return app
