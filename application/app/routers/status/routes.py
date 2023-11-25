import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, Form, HTTPException
from starlette.status import HTTP_400_BAD_REQUEST

from dependencies.logger import TimedRoute
from routers.status.service import Service

router = APIRouter(prefix="/status/{application_uuid}", route_class=TimedRoute)


@router.get("/check")
async def status(
        application_uuid: uuid.UUID,
        service: Annotated[Service, Depends()]
):
    app = await service.get_application(application_id=application_uuid)
    return {'status': app.status}


@router.post("/set")
async def status(
        application_uuid: uuid.UUID,
        service: Annotated[Service, Depends()],
        status: str = Form(...)
):
    statuses = ["new", "work", "modification", "request"]
    if status not in statuses:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"status can be {''.join(statuses)}")

    app = await service.get_application(application_id=application_uuid)
    await service.set_status(app, status)
    return {'status': app.status}