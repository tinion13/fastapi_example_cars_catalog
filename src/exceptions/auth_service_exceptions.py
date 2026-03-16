class AuthError(Exception):
    pass


class InvalidTokenError(AuthError):
    pass


class TokenExpiredError(AuthError):
    pass


class UserNotFoundError(AuthError):
    pass
