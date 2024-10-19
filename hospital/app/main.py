from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
import uvicorn

import sys
from pathlib import Path

path = Path(__file__).parent.parent.parent
sys.path.insert(0, str(path))

from hospital.app.hospitals.api import router as hospitals_router


app = FastAPI()
app.include_router(hospitals_router)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="SimbirHealth | Hospital API",
        version="1.0.0",
        summary="Работа с больницами",
        description="Документация API микросервиса больниц SimbirHealth.",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi


if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8082, reload=True)