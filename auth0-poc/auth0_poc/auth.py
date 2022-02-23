from functools import wraps
from typing import Any, Callable, Mapping, TypeVar, cast

from flask import request, session
from jose import jwt
import requests

from auth0_poc import errors
from settings import settings


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


def get_key_for_token(token: str) -> str:
    jwks_url = f"{settings.auth0_domain}/.well-known/jwks.json"
    resp = requests.get(jwks_url)
    resp.raise_for_status()

    try:
        header = jwt.get_unverified_header(token)
    except jwt.JWTError as ex:
        raise errors.InvalidTokenError from ex

    jwks = resp.json()
    kid = header["kid"]

    try:
        return next(key for key in jwks["keys"] if key["kid"] == kid)
    except StopIteration as ex:
        raise errors.InvalidKeyError from ex


def get_validated_token_payload(token: str) -> Mapping[str, Any]:
    key = get_key_for_token(token)

    try:
        payload = jwt.decode(
            token,
            key,
            algorithms=["RS256"],
            audience=settings.api_audience,
            issuer=f"{settings.auth0_domain}/",
        )
    except jwt.ExpiredSignatureError as ex:
        raise errors.TokenExpiredError from ex
    except jwt.JWTClaimsError as ex:
        raise errors.InvalidClaimsError from ex
    except Exception as ex:
        raise errors.InvalidTokenError from ex

    return payload


def validate_token_has_scopes(token: str, scopes: list[str]) -> None:
    claims = jwt.get_unverified_claims(token)

    if token_scopes := claims.get("scope", "").split():
        if not all(scope in token_scopes for scope in scopes):
            raise errors.InsufficientScopesError(scopes)


Fn = TypeVar("Fn", bound=Callable[..., Any])


def requires_auth(func: Fn) -> Fn:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        token = get_token_from_headers()
        payload = get_validated_token_payload(token)
        session["user"] = payload
        return func(*args, **kwargs)

    return cast(Fn, wrapper)


def requires_scopes(scopes: list[str]) -> Callable[[Fn], Fn]:
    def decorator(func: Fn) -> Fn:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            token = get_token_from_headers()
            validate_token_has_scopes(token, scopes)
            return func(*args, **kwargs)

        return cast(Fn, wrapper)

    return decorator


def requires_scope(scope: str) -> Callable[[Fn], Fn]:
    return requires_scopes([scope])
