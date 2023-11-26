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


class PassportModel(BaseModel):
    file: str
    number: int
    series: int


class PersonModelGlobal(BaseModel):
    id: uuid.UUID
    middle_name: str
    last_name: str
    first_name: str
    marital_status: str
    birth_date: datetime
    registration_address: str
    living_address: str
    children: bool
    passport: PassportModel


class ApplicationDetailsModel(BaseModel):
    type: str
    accepted_sum: int
    max_sum: int
    accepted_term: int
    max_term: int
    monthly_payment: float
    accepted_rate: float
    max_rate: float


class EmployeeModel(BaseModel):
    salary: float
    employer: str
    file: str
    experience: int
    role: str


class AdditionalModel(BaseModel):
    salary: float
    confirmation_file: str
    source: str


class PDNModel(BaseModel):
    created_at: datetime
    rate: float


class DepositModel(BaseModel):
    amount: float


class AnalysisModel(BaseModel):
    non_payment_risk_sum: bool
    non_payment_risk_salary: bool
    non_payment_risk_salary_additional: bool
    risk_debt_upper: bool
    risk_down_payment_media: bool


class HistoryModel(BaseModel):
    status: str | None
    microloans: bool | None
    often_microloans: bool | None
    pay_by_loan: bool | None
    late_payment: bool | None
    overdue: bool | None

class ApplicationDataModel(BaseModel):
    id: uuid.UUID
    details: ApplicationDetailsModel | None
    checker: CheckerModel
    personal: PersonModelGlobal
    status: str
    message: str | None
    deposit: DepositModel | None
    history: HistoryModel | None
    analysis: AnalysisModel | None

    class Config:
        from_attributes = True


class ApplicationModel(BaseModel):
    application: ApplicationDataModel
