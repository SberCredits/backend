from storages.queues.celery_app import celery_app


class Queue:
    """
    Класс для удобного управления очередями celery
    """
    def __init__(self, queue_name: str):
        self.queue = queue_name
        self.task = None
        self.celery = celery_app

    def __getattr__(self, item):
        self.task = item
        return self

    def __call__(self, *args, **kwargs):
        self.celery.send_task(
            name=self.task,
            queue=self.queue,
            kwargs=kwargs
        )


audit = Queue("audit")
