"""Entrypoint code"""

import asyncio
import logging
from argparse import ArgumentParser

import uvloop

from pybuster.requester import Requester
from pybuster.table import display_responses
from pybuster.utils import setup_logging

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

logger = logging.getLogger()


def get_target_paths(file_path: str) -> list[str]:
    with open(file_path) as file:
        return file.read().split("\n")


def get_args():
    args_parser = ArgumentParser()
    args_parser.add_argument("-t", "--target", required=True)
    args_parser.add_argument(
        "-f",
        "--filename",
        help="Optional path to a file containing paths to enumerate, separate by a newline",
        required=False,
        default="common.txt",
    )
    return args_parser.parse_args()


def main():
    setup_logging()
    args = get_args()
    target_host = args.target
    filename = args.filename
    logger.info("Starting directory enumeration for %s", target_host)
    target_paths = get_target_paths(filename)
    requester = Requester(target_host, target_paths)
    results = asyncio.run(requester.enumerate())
    display_responses(results, target_host)


if __name__ == "__main__":
    main()
