import datetime
import uuid

from storages.queues.celery_app import celery_app
from tasks.service import Service

"""
                "type": response.status_code,
                "detail": f"{request.url} {response}",
                "created_at": datetime.datetime.now(),
                "ip_address": ip_address"""


@celery_app.task(name="log")
def log(type: str, detail: str, created_at: datetime.datetime, ip_address: str, application: uuid.UUID = None):
    service = Service()
    service.save_log(**{
        "type": type,
        "detail": detail,
        "created_at": created_at,
        "ip_address": ip_address,
        "application": application
    })
