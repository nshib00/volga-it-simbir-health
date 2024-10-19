from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
import uvicorn

import sys
from pathlib import Path

path = Path(__file__).parent.parent.parent
sys.path.insert(0, str(path))

from account.app.users.api import router as users_router
from account.app.users.doctors.api import router as doctors_router
from account.app.auth.api import router as auth_router


app = FastAPI()
app.include_router(users_router)
app.include_router(auth_router)
app.include_router(doctors_router)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="SimbirHealth | Account API",
        version="1.0.0",
        summary="Пользователи и авторизация",
        description="Документация API микросервиса аккаунтов SimbirHealth.",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8081, reload=True)