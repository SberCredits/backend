from fastapi import FastAPI, APIRouter

from dependencies.lifespan import lifespan
from routers.applications.routes import router as app_router
from routers.status.routes import router as status_router

app = FastAPI(
    title="SberCredits",
    version="0.1.0",
    lifespan=lifespan
)
api_router = APIRouter(prefix='/api/v1')
api_router.include_router(app_router)
api_router.include_router(status_router)
app.include_router(api_router)