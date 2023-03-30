FROM python:3.10.5-slim-buster

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

RUN pip install poetry
RUN apt-get update && apt-get install make
