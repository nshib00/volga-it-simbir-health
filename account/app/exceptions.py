from fastapi import HTTPException, status


class BaseAppException(HTTPException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = ''

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class BaseUnauthorizedException(BaseAppException):
    status_code = status.HTTP_401_UNAUTHORIZED


class BaseNotFoundException(BaseAppException):
    status_code = status.HTTP_404_NOT_FOUND


class InvalidTokenTypeException(BaseUnauthorizedException):
    detail = 'Указан несуществующий тип токена.'


class InvalidCredentialsException(BaseUnauthorizedException):
    detail = 'Указан неверный логин или пароль.'


class NoTokenException(BaseUnauthorizedException):
    detail = 'Токен отсутствует.'


class TokenExpiredException(BaseUnauthorizedException):
    detail = 'Срок действия токена истек.'


class UserNotExistsException(BaseNotFoundException):
    detail = 'Пользователь с переданными данными не существует.'


class PacientNotExistsException(BaseNotFoundException):
    detail = 'Пользователь с переданными данными либо не существует, либо не является пациентом.'


class ForbiddenException(BaseAppException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = 'Нет необходимых прав для доступа.'


class InvalidTokenForRefreshException(BaseAppException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = 'Передан неверный токен для обновления.'


class DoctorNotExistsException(UserNotExistsException):
    detail = 'Доктор с переданными данными не существует.'


class GeneralAPIException(BaseAppException):
    def __init__(self, status_code: int, context: str):
        self.status_code = status_code
        self.detail = context

