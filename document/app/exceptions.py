from fastapi import HTTPException, status


class BaseAppException(HTTPException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = ''

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class APIExceptionWithContext(BaseAppException):
    def __init__(self, status_code: int, context: str):
        self.status_code = status_code
        self.detail = context


class BaseUnauthorizedException(BaseAppException):
    status_code = status.HTTP_401_UNAUTHORIZED


class BaseBadRequestException(BaseAppException):
    status_code = status.HTTP_400_BAD_REQUEST


class ForbiddenException(BaseAppException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = 'Нет необходимых прав для доступа.'


class UserNotExistsException(BaseUnauthorizedException):
    detail = 'Пользователь с переданными данными не существует.'


class NotAuthenticatedException(BaseUnauthorizedException):
    detail = 'Необходимо войти в систему.'


class TimetableNotExistsException(UserNotExistsException):
    detail = 'Такой записи нет в расписании.'


class BaseNotFoundException(BaseAppException):
    status_code = status.HTTP_404_NOT_FOUND


class BaseConflictException(BaseAppException):
    status_code = status.HTTP_409_CONFLICT


class HospitalNotFoundException(BaseNotFoundException):
    detail = 'Такой больницы нет в системе.'


class UserNotFoundException(BaseNotFoundException):
    detail = 'Такого пользователя больницы нет в системе.'


class FutureDatetimeException(BaseBadRequestException):
    detail = 'Для создания записи в истории указана дата из будущего.'


class RoomNotExistException(APIExceptionWithContext):
    def __init__(self, room: str):
        room_not_exist_context = f'Комната {room} отсутствует в больнице.'
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            context=room_not_exist_context
        )

class UserIsNotPacientException(BaseBadRequestException):
    detail = 'Данный пользователь не является пациентом.'


class UserIsNotPacientOrDoctorException(ForbiddenException):
    pass


class HistoryNotExistsException(BaseNotFoundException):
    detail = 'Такой записи нет в системе.'


class HistoryInvalidDatetimeException(BaseBadRequestException):
    detail = 'Введено неверное время записи. Количество минут должно быть кратно 30, количество секунд - равно 0.'


class DatetimeIsAlreadyTakenException(BaseConflictException):
    detail = 'На переданное время уже существует запись в истории для данного пользователя.'
