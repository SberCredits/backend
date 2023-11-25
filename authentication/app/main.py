from fastapi import FastAPI, APIRouter
from starlette.middleware.cors import CORSMiddleware

from dependencies.lifespan import lifespan
from router.routes import router as auth_router

app = FastAPI(
    title="SberCredits",
    version="0.1.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

router = APIRouter(prefix="/api/v1")
router.include_router(auth_router)
app.include_router(router)