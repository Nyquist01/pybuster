from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes.scan import router as scan_router

app = FastAPI(
    title="PyBuster",
    summary="API for PyBuster, a tool like GoBuster but written in Python",
    version="0.0.1",
)

# Allow requests from browsers
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

root_router = APIRouter(prefix="/api")
root_router.include_router(scan_router)

app.include_router(root_router)
