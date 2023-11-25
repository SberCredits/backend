import os

from celery import Celery


redis_password = os.getenv("REDIS_PASSWORD")
redis_host = os.getenv("REDIS_HOST")
redis_database = os.getenv("REDIS_DATABASE")

redis_url = f"redis://:{redis_password}@{redis_host}/{redis_database}"
celery_app = Celery(backend=redis_url, broker=redis_url, include=["tasks.tasks"])
