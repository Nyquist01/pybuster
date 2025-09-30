import asyncio
import logging
from dataclasses import dataclass
from typing import Sequence

import aiohttp

from .utils import Timer

logger = logging.getLogger()


@dataclass
class ResponseResult:
    status_code: int
    path: str
    size: int | None
    content_type: str | None = None
    server: str | None = None


class Requester:
    def __init__(
        self,
        target_host: str,
        target_paths: Sequence[str],
        concurrency: int = 100,
        timeout: int = 3,
    ):
        self.target_host = target_host
        self.target_base_url = f"https://{target_host}"
        self.target_paths = target_paths
        self.timeout = timeout
        self.concurrency = concurrency

    def create_session(self) -> aiohttp.ClientSession:
        return aiohttp.ClientSession(
            base_url=self.target_base_url,
            connector=aiohttp.TCPConnector(limit=self.concurrency),
            conn_timeout=self.timeout,
        )

    async def run(self) -> list[ResponseResult]:
        async with self.create_session() as session:
            with Timer(self.target_host, self.target_paths):
                tasks = [self.make_request(path, session) for path in self.target_paths]
                results = await asyncio.gather(*tasks)
                return [result for result in results if result]

    async def make_request(
        self, path: str, session: aiohttp.ClientSession
    ) -> ResponseResult | None:
        path_str = f"/{path}"
        try:
            async with session.get(path) as response:
                if response.status == 404:
                    logger.info("%s returned 404", path_str)
                    return None
                return deserialize_aiohttp_response(response, path)
        except aiohttp.ClientError:  # TODO: need to handle HTTP and asyncio timeouts
            logger.error("Failed to get response for path %s", path_str)
            return None


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
