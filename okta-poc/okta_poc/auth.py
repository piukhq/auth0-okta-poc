from functools import wraps
from typing import Any, Callable, TypeVar, cast

from flask import request
import okta_jwt_verifier

from okta_poc import errors
from settings import settings


jwt_verifier = okta_jwt_verifier.AccessTokenVerifier(
    issuer=f"https://{settings.okta_domain}/oauth2/default",
    audience=settings.api_audience,
)


def get_token_from_headers() -> str:
    """
    Extracts the token from the Authorization header.
    Raises an AuthError if the token cannot be extracted.
    """
    auth = request.headers.get("Authorization", "").strip()
    if not auth:
        raise errors.MissingHeaderError

    parts = auth.split()
    if parts[0].lower() != "bearer" or len(parts) != 2:
        raise errors.InvalidHeaderError

    return parts[1]


Fn = TypeVar("Fn", bound=Callable[..., Any])


def requires_auth(func: Fn) -> Fn:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        token = get_token_from_headers()
        jwt_verifier.verify(token)
        return func(*args, **kwargs)

    return cast(Fn, wrapper)
