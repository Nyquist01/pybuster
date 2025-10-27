from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .consts import SHORT_DIRECTORIES
from .requester import Requester, ResponseResult

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class EnumerationRequest(BaseModel):
    target_host: Any
    target_directories: list[str] = SHORT_DIRECTORIES


@app.post("/enumerate")
async def enumerate_website(
    enumeration_request: EnumerationRequest,
) -> list[ResponseResult]:
    """Enumerate the target host against all target directories."""
    requester = Requester(
        enumeration_request.target_host, enumeration_request.target_directories
    )
    return await requester.enumerate()
