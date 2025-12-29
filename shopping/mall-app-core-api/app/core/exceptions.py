from fastapi import HTTPException, status


class AppException(HTTPException):
    """Base application exception."""

    def __init__(
        self,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail: str = "Internal server error",
        code: str | None = None,
    ):
        super().__init__(status_code=status_code, detail=detail)
        self.code = code


class NotFoundException(AppException):
    def __init__(self, detail: str = "Resource not found", code: str | None = None):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail, code=code)


class BadRequestException(AppException):
    def __init__(self, detail: str = "Bad request", code: str | None = None):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail, code=code)


class UnauthorizedException(AppException):
    def __init__(self, detail: str = "Unauthorized", code: str | None = None):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail, code=code)


class ForbiddenException(AppException):
    def __init__(self, detail: str = "Forbidden", code: str | None = None):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail, code=code)


class ConflictException(AppException):
    def __init__(self, detail: str = "Conflict", code: str | None = None):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail, code=code)
