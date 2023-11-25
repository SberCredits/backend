from typing import Annotated

from fastapi import APIRouter, Depends, Form

from dependencies.logger import TimedRoute
from router.service import Service

router = APIRouter(prefix="/token", route_class=TimedRoute)


@router.post("/")
async def get_token(
        service: Annotated[Service, Depends()],
        username: str = Form(...),
        password: str = Form(...)
):
    user = await service.get_user(username, password)

    return {
        "access_token": user.access_token,
        "type": "Bearer"
    }
