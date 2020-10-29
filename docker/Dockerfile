FROM python:3.9-slim-buster

COPY ./Pipfile /Pipfile

RUN pip install pipenv && \
    pipenv lock -r --dev > /tmp/requirements-dev.txt && \
    pip install -q -r /tmp/requirements-dev.txt && \
    rm /tmp/requirements-dev.txt

COPY ./src /src
COPY ./tests /tests

ENV PYTHONPATH=/src