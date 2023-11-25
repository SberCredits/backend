import uuid
from datetime import datetime
from typing import Dict

from pydantic import BaseModel


class CheckerModel(BaseModel):
    username: str


class PersonModel(BaseModel):
    first_name: str
    last_name: str
    middle_name: str


class ApplicationsModel(BaseModel):
    status: str
    created_at: datetime
    id: uuid.UUID
    checker: CheckerModel
    personal: PersonModel

    class Config:
        from_attributes = True
