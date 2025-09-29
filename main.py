import asyncio
from argparse import ArgumentParser

import uvloop

from pybuster.requester import Requester
from pybuster.utils import timer

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def get_target_paths() -> list[str]:
    with open("wordlists/common.txt") as file:
        return file.read().split("\n")


def get_args():
    args_parser = ArgumentParser()
    args_parser.add_argument("-t", "--target", required=True)
    return args_parser.parse_args()


@timer
def main():
    args = get_args()
    target_host = args.target
    target_paths = get_target_paths()
    requester = Requester(target_host, target_paths)
    asyncio.run(requester.run())


if __name__ == "__main__":
    main()
