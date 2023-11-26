import datetime
import uuid
from typing import Annotated

from fastapi import Depends
from sqlalchemy import select, cast, String, insert, update, text, desc, asc
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies.requests import client
from storages.database.database import get_session
from storages.database.models.application import Application, PDN

from storages.database.models.bki import BKIReport, BKIObligations, BKIObligationsDebt, ObligationsReport


class ApplicationRepository:
    def __init__(self, session: Annotated[AsyncSession, Depends(get_session)]):
        self.session = session

    async def get(
            self,
            application_id: uuid.UUID | str = None,
            ordering: str = None,
            one: bool = True
    ):
        queries = []
        stmt = select(Application)
        if application_id:
            queries.append(cast(Application.id, String).istartswith(str(application_id)))

        if ordering:
            method = asc

            if "-" in ordering:
                method = desc

            stmt = stmt.order_by(method(ordering[1:]))

        stmt = stmt.where(*queries)
        result = await self.session.execute(stmt)
        print(stmt.compile(compile_kwargs={"literal_binds": True}))
        scalars = result.scalars()
        if one:
            return scalars.first()

        return scalars.all()


class Service:
    def __init__(self,
                 session: Annotated[AsyncSession, Depends(get_session)],
                 applications: Annotated[ApplicationRepository, Depends()]):
        self.session = session
        self.applications = applications

    async def get_applications(self, application_id: str, order_by: str):
        return await self.applications.get(application_id=application_id, ordering=order_by, one=False)

    async def get_application(self, application_id: uuid.UUID) -> Application:
        return await self.applications.get(application_id=application_id, one=True)

    async def get_pdn(self, pass_number, pass_series):
        request = await client.get("http://placeholder:8000/pdn", params={
            "passport_number": pass_number,
            "passport_series": pass_series
        })
        return request.json()

    async def get_bki(self, pass_number, pass_series):
        request = await client.get("http://placeholder:8000/bki", params={
            "passport_number": pass_number,
            "passport_series": pass_series
        })
        return request.json()

    async def create_debt(self, interval, amount):
        stmt = insert(BKIObligationsDebt).values(
            interval=str(interval),
            debt_amount=amount
        ).returning(BKIObligationsDebt.id)
        result = await self.session.execute(stmt)
        return result.scalar()

    async def create_obligation(self, data):
        debt = await self.create_debt(
            amount=data["amount"],
            interval=data["interval"]
        )
        open_date = datetime.datetime.strptime(data["dates"]["открытия"], "%Y-%m-%d").date()

        close_date = data["dates"]["ожидаемо"]
        if close_date is not None:
            close_date = datetime.datetime.strptime(close_date, "%Y-%m-%d").date()

        planned_date = datetime.datetime.strptime(data["dates"]["ожидаемо"], "%Y-%m-%d").date()
        stmt = insert(BKIObligations).values(
            type=data["type"],
            role=data["role"],
            status=data["status"] == "завершенный",
            amount=data["amount"],
            rate=round(data["rate"], 2),
            repayment=data["repayment"] or 0,
            debt_id=debt,
            open_date=open_date,
            close_date_planned=planned_date,
            close_date_actual=close_date
        ).returning(BKIObligations.id)
        result = await self.session.execute(stmt)
        return result.scalar()

    async def create_obligationreport(self, report_id, obligation_id):
        stmt = insert(ObligationsReport).values(
            report_id=report_id,
            obligation_id=obligation_id
        )
        await self.session.execute(stmt)

    async def save_bki(self, app, bki):
        stmt = insert(BKIReport).values(score=bki["score"]).returning(BKIReport.id)
        result = await self.session.execute(stmt)
        report_id = result.scalar()

        for element in bki["obligations"]:
            obligation_id = await self.create_obligation(element)
            await self.create_obligationreport(obligation_id=obligation_id, report_id=report_id)

        stmt = update(Application).where(Application.id == app).values({Application.bki_report_id: report_id})
        await self.session.execute(stmt)
        await self.session.commit()

    async def save_pdn(self, app, pdn):
        stmt = insert(PDN).values(rate=pdn).returning(PDN.id)
        result = await self.session.execute(stmt)
        pdn_id = result.scalar()
        stmt = update(Application).where(Application.id == app).values({Application.pdn_id: pdn_id})
        await self.session.execute(stmt)
        await self.session.commit()

    async def get_obligations(self, report_id):
        stmt = select(ObligationsReport).where(ObligationsReport.report_id == report_id)
        result = await self.session.execute(stmt)
        return result.scalars().all()
