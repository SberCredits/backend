import uuid
from datetime import datetime

from sqlalchemy import Integer, String, DateTime, Boolean, Float, UUID, ForeignKey, func
from sqlalchemy.orm import mapped_column, Mapped, relationship

from storages.database._models import Base
from storages.types.files import File


class Passport(Base):
    __tablename__ = "passport"

    series: Mapped[int] = mapped_column(Integer)
    number: Mapped[int] = mapped_column(Integer)
    file: Mapped[str] = mapped_column(File(is_need_folder=True, bucket="attachments"))


class PersonalData(Base):
    __tablename__ = "personal_data"

    first_name: Mapped[str] = mapped_column(String)
    last_name: Mapped[str] = mapped_column(String)
    middle_name: Mapped[str] = mapped_column(String)
    birth_date: Mapped[datetime] = mapped_column(DateTime)
    registration_address: Mapped[str] = mapped_column(String)
    living_address: Mapped[str] = mapped_column(String)
    marital_status: Mapped[str] = mapped_column(String)
    children: Mapped[bool] = mapped_column(Boolean)
    passport_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("passport.id"))
    passport = relationship("Passport", lazy="selectin")


class AdditionalData(Base):
    __tablename__ = "additional_data"

    salary: Mapped[float] = mapped_column(Float)
    confirmation_file: Mapped[str] = mapped_column(File(is_need_folder=True, bucket="attachments"))  # File
    source: Mapped[str] = mapped_column(String)


class EmployeeData(Base):
    __tablename__ = "employee_data"

    employer: Mapped[str] = mapped_column(String)
    experience: Mapped[int] = mapped_column(Integer)  # In month
    role: Mapped[str] = mapped_column(String)
    salary: Mapped[float] = mapped_column(Float)
    file: Mapped[str] = mapped_column(File(is_need_folder=True, bucket="attachments"))


class Deposits(Base):
    __tablename__ = "deposits"

    amount: Mapped[float] = mapped_column(Float)


class Attachment(Base):
    __tablename__ = "file"

    file: Mapped[str] = mapped_column(File(is_need_folder=True, bucket="attachments"))
    application_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("application.id"))
    application = relationship("Application", lazy="selectin")


class PDN(Base):
    __tablename__ = "pdn"

    rate: Mapped[float] = mapped_column(Float)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())


class ApplicationDetails(Base):
    __tablename__ = "application_details"

    type: Mapped[str] = mapped_column(String)

    max_sum: Mapped[int] = mapped_column(Integer)
    accepted_sum: Mapped[int] = mapped_column(Integer)

    max_rate: Mapped[int] = mapped_column(Integer)
    accepted_rate: Mapped[int] = mapped_column(Integer)

    max_term: Mapped[int] = mapped_column(Integer)
    accepted_term: Mapped[int] = mapped_column(Integer)

    monthly_payment: Mapped[float] = mapped_column(Float)


class Application(Base):
    """
    personal - персональные данные
    employee - данные о работе
    additional - дополнительное
    deposit - депозит в банке (и есть ли)
    bki_report - получение репорта
    status - Новая, В работе, Дозапрос информации, На доработке, Завершена (не отображается у андеррайтера)
    """
    __tablename__ = "application"

    personal_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("personal_data.id"), nullable=True)
    employee_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("employee_data.id"), nullable=True)
    additional_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("additional_data.id"),
                                                     nullable=True)
    deposit_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("deposits.id"), nullable=True)
    bki_report_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("bki_report.id"), nullable=True)
    checker_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("account.id"), nullable=True)
    pdn_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("pdn.id"), nullable=True)
    details_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("application_details.id"),
                                                  nullable=True)
    status: Mapped[str] = mapped_column(String, default="new")
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    pdn = relationship("PDN", lazy="selectin")
    personal = relationship("PersonalData", lazy="selectin")
    employee = relationship("EmployeeData", lazy="selectin")
    additional = relationship("AdditionalData", lazy="selectin")
    deposit = relationship("Deposits", lazy="selectin")
    bki_report = relationship("BKIReport", lazy="selectin")
    checker = relationship("Account", lazy="selectin")
    details = relationship("ApplicationDetails", lazy="selectin")
