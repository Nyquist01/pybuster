import asyncio
from typing import Sequence

import aiohttp


class Requester:
    def __init__(self, target_host: str, target_paths: Sequence[str]):
        self.target_host = target_host
        self.target_base_url = f"https://{self.target_host}"
        self.target_paths = target_paths

    def create_aiohttp_connector(self):
        # Increase the limit param which increase the total number simultaneous
        # connections allowed by the aiohttp session
        return aiohttp.TCPConnector(limit=0)

    async def run(self):
        connector = self.create_aiohttp_connector()
        async with aiohttp.ClientSession(
            base_url=self.target_base_url, connector=connector
        ) as session:
            tasks = [self.make_request(path, session) for path in self.target_paths]
            await asyncio.gather(*tasks)

    async def make_request(self, path: str, session: aiohttp.ClientSession):
        try:
            response = await session.get(path)
        except aiohttp.ClientError:
            print(f"Unable to find response for {path}")
            return

        if response.status == 200:
            print(f"Found {path}")
        if response.status == 302:
            print(f"{path} redirected to {response.real_url}")
        elif response.status in [403, 404]:
            print(f"Unauthorized to access {path}")
