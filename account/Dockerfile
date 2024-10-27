FROM python:3.12.5-slim

RUN mkdir /account
WORKDIR /account
RUN mkdir /docker-entrypoint-initdb.d

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY pyproject.toml .

RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install

COPY . .

RUN chmod a+x /account/docker/*.sh


