from fastapi import HTTPException, status


class BaseAppException(HTTPException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = ''

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class BaseNotFoundException(BaseAppException):
    status_code = status.HTTP_404_NOT_FOUND
    

class HospitalNotFoundException(BaseNotFoundException):
    detail = 'Больница не найдена.'


class NotAuthenticatedException(BaseAppException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Необходимо войти в систему.'


class ForbiddenException(BaseAppException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = 'Нет необходимых прав для доступа.'