from fastapi import HTTPException, status


class BaseAppException(HTTPException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = ''

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)
    

class HospitalNotFoundException(BaseAppException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = 'Больница не найдена.'