from flask import Blueprint, Response, jsonify, g

from auth0_poc.auth import requires_auth, requires_scope

api = Blueprint("api", __name__, url_prefix="/api")


def user_info() -> dict:
    return {
        "sub": g.user["sub"],
        "org_id": g.user["org_id"],
        "permissions": g.user["permissions"],
    }


@api.route("/public")
def public() -> Response:
    msg = (
        "Hello from a public endpoint! You don't need to be authenticated to see this."
    )
    return jsonify(message=msg)


@api.route("/read-mids")
@requires_auth
@requires_scope("read:mids")
def read_mids() -> Response:
    msg = {
        "message": (
            "Hello from a read-mids endpoint! "
            "You need to be authenticated and have the read:mids scope to see this."
        ),
        "user": user_info(),
    }
    return jsonify(msg)


@api.route("/write-mids")
@requires_auth
@requires_scope("write:mids")
def write_mids() -> Response:
    msg = {
        "message": (
            "Hello from a write-mids endpoint! "
            "You need to be authenticated and have the write:mids scope to see this."
        ),
        "user": user_info(),
    }
    return jsonify(msg)
