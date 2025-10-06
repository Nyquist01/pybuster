from fastapi import FastAPI, WebSocket
from pydantic import BaseModel

from .consts import DEFAULT_DIRECTORIES
from .requester import Requester

app = FastAPI()


class EnumerationRequest(BaseModel):
    target_host: str
    target_directories: list[str] = DEFAULT_DIRECTORIES


@app.websocket("/enumerate")
async def enumerate_website(websocket: WebSocket):
    await websocket.accept()
    while True:
        command = await websocket.receive_text()
        command = EnumerationRequest.model_validate(command)
        requester = Requester(command.target_host, command.target_directories)
        results = requester.enumerate()
        await websocket.send_json(results)
