"""Entrypoint for Pybuster when running as a CLI tool"""

import asyncio
import logging
from typing import Annotated

import typer
import uvloop

from pybuster.requester import Requester
from pybuster.table import display_responses
from pybuster.utils import setup_logging

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

logger = logging.getLogger()


def get_target_paths(file_path: str) -> list[str]:
    with open(file_path) as file:
        return file.read().split("\n")


def main(
    target: Annotated[str, typer.Argument(help="The target website host to enumerate")],
    filename: Annotated[
        str,
        typer.Argument(
            help="A .txt file containing directories/paths to enumerate on the target host"
        ),
    ] = "backend/common.txt",
):
    setup_logging()
    target_paths = get_target_paths(filename)
    requester = Requester(target, target_paths)
    results = asyncio.run(requester.enumerate())
    display_responses(results, target)


if __name__ == "__main__":
    typer.run(main)
