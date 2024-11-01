import uvicorn
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
import sys
from pathlib import Path

path = Path(__file__).parent.parent.parent
sys.path.insert(0, str(path))


from timetable.app.timetables.api import router as main_timetable_router
from timetable.app.timetables.doctor.api import router as doctor_timetable_router
from timetable.app.timetables.hospital.api import router as hospital_timetable_router
from timetable.app.timetables.appointments.api import router as appointments_router


app = FastAPI()

ALL_ROUTERS = (main_timetable_router, doctor_timetable_router, hospital_timetable_router, appointments_router)
for router in ALL_ROUTERS:
    app.include_router(router)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="SimbirHealth | Timetable API",
        version="1.0.0",
        summary="Работа с расписанием",
        description="Документация API микросервиса расписаний SimbirHealth.",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi


if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8083, reload=True)