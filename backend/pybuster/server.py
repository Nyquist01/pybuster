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
    requester = Requester(
        enumeration_request.target_host, enumeration_request.target_directories
    )
    # response = await requester.enumerate()
    response = [
        {
            "status_code": 200,
            "path": "/path1",
            "size": 1,
            "content_type": "html",
            "server": "nginx",
            "tech": "jQuery",
        },
        {
            "status_code": 404,
            "path": "/path2",
            "size": 1,
            "content_type": "text",
            "server": "aws",
            "tech": "python",
        },
    ]
    return response
