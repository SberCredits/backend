from sqlalchemy import insert

from storages.database.database import get_session
from storages.database.models import AuditLog


class Service:
    def __init__(self):
        self.session = get_session()

    def save_log(self, **data):
        with self.session as sess:
            stmt = insert(AuditLog).values(**data)
            sess.execute(stmt)
            sess.commit()
