from flask import Blueprint, Response, jsonify

from okta_poc.auth import requires_auth


api = Blueprint("api", __name__, url_prefix="/api")


@api.route("/public")
def public() -> Response:
    msg = (
        "Hello from a public endpoint! You don't need to be authenticated to see this."
    )
    return jsonify(message=msg)


@api.route("/private")
@requires_auth
def private() -> Response:
    msg = "Hello from a private endpoint! You need to be authenticated to see this."
    return jsonify(message=msg)
