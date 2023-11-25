from fastapi import FastAPI, APIRouter

from dependencies.lifespan import lifespan
from router.routes import router as auth_router

app = FastAPI(
    title="SberCredits",
    version="0.1.0",
    lifespan=lifespan
)


router = APIRouter(prefix="/api/v1")
router.include_router(auth_router)
app.include_router(router)