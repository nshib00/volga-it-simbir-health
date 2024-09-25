from account.app.service.base import BaseAddService, BaseGetService, BaseUpdateService, BaseDeleteService
from account.app.users.models import User

class UserService(BaseGetService, BaseAddService, BaseUpdateService, BaseDeleteService):
    model = User


    
            
