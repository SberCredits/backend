import uuid
from datetime import datetime

from sqlalchemy import String, Float, DateTime, Boolean, UUID, ForeignKey, Integer, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from storages.database._models import Base


class BKIObligationsDebt(Base):
    """
    interval - период просрочки
    debt_amount - задолженность
    """
    __tablename__ = "bki_obligations_debt"

    interval: Mapped[str] = mapped_column(String)
    debt_amount: Mapped[float] = mapped_column(Float)


class BKIObligations(Base):
    """
    тип - вид обязательства
    open_date - дата открытия
    close_planned - дата закрытия (планируемая)
    close_actual - дата закрытия (настоящая)
    amount - сумма
    role - Заемщик, поручитель, со-заемщик
    status - Текущий (False) / Завершенный (True)
    rate - ставка в процентах
    repayment - остаток к выплате
    """
    __tablename__ = "bki_obligations"

    type: Mapped[str] = mapped_column(String)
    open_date: Mapped[datetime] = mapped_column(DateTime)
    close_date_planned: Mapped[datetime] = mapped_column(DateTime)
    close_date_actual: Mapped[datetime] = mapped_column(DateTime)
    amount: Mapped[float] = mapped_column(Float)
    role: Mapped[str] = mapped_column(String)
    status: Mapped[bool] = mapped_column(Boolean, default=False)
    rate: Mapped[float] = mapped_column(Float)
    repayment: Mapped[float] = mapped_column(Float)
    debt_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("bki_obligations_debt.id"))
    debt = relationship("BKIObligationsDebt")


class ObligationsReport(Base):
    __tablename__ = "obligations_report"

    report_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("bki_report.id"))
    obligation_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("bki_obligations.id"))
    report = relationship("BKIReport", lazy="selectin")
    obligation = relationship("BKIObligations", lazy="selectin")


class BKIReport(Base):
    """
    score: Скор от 300 до 900
    created_at: до 14 дней
    """
    __tablename__ = "bki_report"

    score: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
