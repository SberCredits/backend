import uuid
from datetime import datetime
from typing import Annotated, List

from fastapi import APIRouter, Depends, Form, HTTPException
from starlette.status import HTTP_404_NOT_FOUND

from routers.applications.pydantic_models import ApplicationsModel
from routers.applications.service import Service

router = APIRouter()


@router.get("/", response_model=List[ApplicationsModel])
async def get_applications(
        service: Annotated[Service, Depends()],
        application_id__istartswith: uuid.UUID = Form(None)
):
    return await service.get_applications(application_id__istartswith)


@router.get("/pdn/{application_uuid}")
async def get_pdn(
        application_uuid: uuid.UUID,
        service: Annotated[Service, Depends()],
):
    application = await service.get_application(application_uuid)
    if not application:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Application not found!")

    if application.pdn and (datetime.now() - application.pdn.created_at).days <= 5:
        return {
            "pdn": application.pdn
        }

    passport = application.personal.passport
    pdn = await service.get_pdn(passport.number, passport.series)
    await service.save_pdn(application_uuid, pdn)

    return {
        "pdn": pdn
    }


@router.get("/bki/{application_uuid}")
async def get_bki(
        application_uuid: uuid.UUID,
        service: Annotated[Service, Depends()],
):
    application = await service.get_application(application_uuid)
    if not application:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Application not found!")

    if application.bki_report and (datetime.now() - application.bki_report.created_at).days <= 14:
        obligations = await service.get_obligations(application.bki_report.id)
        return {
            "report": application.bki_report,
            "obligations": [obligation.obligation for obligation in obligations]
        }

    passport = application.personal.passport
    bki = await service.get_bki(passport.number, passport.series)
    if not bki:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Application not found!")

    await service.save_bki(application_uuid, bki)

    application = await service.get_application(application_uuid)
    return {
        "report": application.bki_report,
        "obligations": bki["obligations"]
    }
