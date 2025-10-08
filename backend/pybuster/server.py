from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .consts import DEFAULT_DIRECTORIES
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
    target_directories: list[str] = DEFAULT_DIRECTORIES


@app.post("/enumerate")
async def enumerate_website(
    enumeration_request: EnumerationRequest,
) -> list[ResponseResult]:
    requester = Requester(
        enumeration_request.target_host, enumeration_request.target_directories
    )
    response = await requester.enumerate()
    return response
