from fastapi import FastAPI
from pydantic import BaseModel

from .consts import DEFAULT_DIRECTORIES
from .requester import Requester, ResponseResult

app = FastAPI()


class EnumerationRequest(BaseModel):
    target_host: str
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
