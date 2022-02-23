class AuthError(Exception):
    code = "auth_error"
    message = "An error occurred during authorization."
    status_code = 401


class MissingHeaderError(AuthError):
    code = "missing_header"
    message = "Authorization header is expected."


class InvalidHeaderError(AuthError):
    code = "invalid_header"
    message = "Authorization header is expected to be in the format: 'Bearer <token>'."


class TokenExpiredError(AuthError):
    code = "token_expired"
    message = "Token has expired."


class InvalidClaimsError(AuthError):
    code = "invalid_claims"
    message = "Token claims are invalid. Please check audience and issuer."


class InvalidTokenError(AuthError):
    code = "invalid_token"
    message = "Token is invalid."


class InvalidKeyError(AuthError):
    code = "invalid_key"
    message = "No valid key was found for this token."


class InsufficientScopesError(AuthError):
    code = "insufficient_scopes"
    message = "Token does not have the required scopes."

    def __init__(self, required_scopes: list[str] = None) -> None:
        if required_scopes:
            self.message = f"Token does not have the required scopes: {', '.join(required_scopes)}."

        super().__init__(required_scopes)
