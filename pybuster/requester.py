"""
Makes HTTP requests to the target host and returns the responses
for each directory enumerated
"""

import asyncio
import logging
from dataclasses import dataclass
from typing import Sequence

import aiohttp

from .utils import Timer

logger = logging.getLogger()


@dataclass
class ResponseResult:
    """
    The HTTP response for a directory/path on the target host
    """

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
        concurrency: int = 400,
        timeout: int = 600,
        default_retry_after: int = 10,
        max_attempts: int = 3,
    ):
        """
        target_host : the target website/host.
        target_paths : a list of target directories/paths to enumerate.
        concurrency : the number of simultaneous connections the HTTP session can make.
        timeout : the amount of time in seconds before the HTTP session times out FOR ALL
            requests (not each individual request).
        max_attempts : maximum number of times to retry enumerating a single path before
            giving up.
        """
        self.target_host = target_host
        self.target_base_url = f"https://{target_host}"
        self.target_paths = target_paths
        self.timeout = timeout
        self.concurrency = concurrency
        self.default_retry_after = default_retry_after
        self.max_attempts = max_attempts

    def create_session(self) -> aiohttp.ClientSession:
        return aiohttp.ClientSession(
            base_url=self.target_base_url,
            connector=aiohttp.TCPConnector(limit=self.concurrency),
            conn_timeout=self.timeout,
        )

    async def run(self) -> list[ResponseResult]:
        """Enumerate all target paths on the target host"""
        async with self.create_session() as session:
            with Timer(self.target_host, self.target_paths):
                tasks = [self.make_request(path, session) for path in self.target_paths]
                results = await asyncio.gather(*tasks)
                return [result for result in results if result]

    async def make_request(
        self, path: str, session: aiohttp.ClientSession, attempts: int = 1
    ) -> ResponseResult | None:
        """
        Makes a request to a single path and returns a ResponseResult if it exists
        """

        path_str = f"/{path}"
        try:
            async with session.get(path, allow_redirects=True) as response:
                if response.status == 404:
                    logger.debug("%s returned 404", path_str)
                    return None
                elif response.status == 429:
                    return self.handle_rate_limit(path, session, response, attempts)
                return deserialize_aiohttp_response(response, path)
        except aiohttp.ClientError:
            logger.error("Failed to get response for path %s", path_str)
            return None

    async def handle_rate_limit(
        self,
        path: str,
        session: aiohttp.ClientSession,
        response: aiohttp.ClientResponse,
        attempts: int,
    ) -> ResponseResult | None:
        """Retries requests for paths that returned a 429 error"""

        path_str = f"/{path}"
        if attempts > self.max_attempts:
            logger.error("Max retries exceeded for path %s", path_str)
            return None

        retry_after_secs = response.headers.get("Retry-After", self.default_retry_after)
        await asyncio.sleep(retry_after_secs)
        attempts += 1
        logger.warning(
            "Rate limited reached for %s, trying again in %s seconds (attempt %s / %s)",
            path_str,
            retry_after_secs,
            attempts,
            self.max_attempts,
        )
        return await self.make_request(path, session, attempts=attempts)


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
