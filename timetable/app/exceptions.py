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


class TimetableInvalidFromDatetimeException(BaseBadRequestException):
    detail = 'Передано неверное время начала рабочего дня. Количество минут должно быть кратно 30, количество секунд - равно 0.'


class TimetableInvalidToDatetimeException(BaseBadRequestException):
    detail = 'Передано неверное время окончания рабочего дня. Количество минут должно быть кратно 30, количество секунд - равно 0.'


class TimetableDateToSmallerDateFromException(BaseBadRequestException):
    detail = 'Ошибка: неверное переданное время. Конец рабочего дня не может быть раньше, чем начало.'


class TooBigDateIntervalException(BaseBadRequestException):
    detail = 'Ошибка: интервал между временем конца и начала работы слишком большой (больше 12 часов).'


class UserNotExistsException(BaseUnauthorizedException):
    detail = 'Пользователь с переданными данными не существует.'


class NotAuthenticatedException(BaseAppException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Необходимо войти в систему.'


class TimetableNotExistsException(UserNotExistsException):
    detail = 'Такой записи нет в расписании.'


class BaseNotFoundException(BaseAppException):
    status_code = status.HTTP_404_NOT_FOUND


class BaseConflictException(BaseAppException):
    status_code = status.HTTP_409_CONFLICT


class DoctorNotFoundException(BaseNotFoundException):
    detail = 'Такого доктора нет в системе.'


class HospitalNotFoundException(BaseNotFoundException):
    detail = 'Такой больницы нет в системе.'


class TimeAlreadyTakenException(BaseConflictException):
    detail = 'На переданное время нельзя назначить запись, оно уже занято.'


class AppointmentsExistException(BaseConflictException):
    detail = 'Расписание нельзя изменить, в нем уже есть записи на прием.'


class TimetableNotFoundException(BaseNotFoundException):
    detail = 'Расписание с переданными данными не найдено.'