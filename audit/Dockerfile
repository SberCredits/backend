FROM python:3.11-slim-buster

RUN pip install poetry
ADD app /application
WORKDIR /application
RUN poetry config virtualenvs.create false
RUN poetry install --no-root
CMD ["celery", "-A", "storages.queues.celery_app.celery_app", "worker", "-l", "info", "-Q", "audit"]