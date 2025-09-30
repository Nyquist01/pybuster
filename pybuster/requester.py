import asyncio
from dataclasses import dataclass
from typing import Sequence

import aiohttp


@dataclass
class ResponseResult:
    status_code: int
    path: str
    size: int | None
    content_type: str | None = None
    server: str | None = None


class Requester:
    def __init__(self, target_host: str, target_paths: Sequence[str]):
        self.target_base_url = f"https://{target_host}"
        self.target_paths = target_paths

    def create_aiohttp_connector(self):
        # Increase the limit param which increase the total number simultaneous
        # connections allowed by the aiohttp session
        return aiohttp.TCPConnector(limit=0)

    async def run(self) -> list[ResponseResult]:
        connector = self.create_aiohttp_connector()
        async with aiohttp.ClientSession(
            base_url=self.target_base_url, connector=connector
        ) as session:
            tasks = [self.make_request(path, session) for path in self.target_paths]
            return await asyncio.gather(*tasks)

    async def make_request(
        self, path: str, session: aiohttp.ClientSession
    ) -> ResponseResult | None:
        try:
            response = await session.get(path)
        except aiohttp.ClientError:  # TODO: need to handle HTTP and asyncio timeouts
            print(f"Unable to find response for /{path}")
            return None

        if response.status == 404:
            return None

        return deserialize_aiohttp_response(response, path)


def deserialize_aiohttp_response(
    response: aiohttp.ClientResponse, path: str
) -> ResponseResult:
    return ResponseResult(
        status_code=response.status,
        path=path,
        size=response.content_length,
        content_type=response.content_type,
        server=response.headers.get("Server"),
    )
