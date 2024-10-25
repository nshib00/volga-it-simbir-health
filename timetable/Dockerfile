FROM python:3.12.5-alpine

RUN mkdir /timetable
WORKDIR /timetable

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY pyproject.toml .

RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install

COPY . .

CMD ["gunicorn", "app.main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8083"]

