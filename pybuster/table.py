import logging
from enum import Enum

from colorama import Fore, Style
from tabulate import tabulate

from .requester import ResponseResult

logger = logging.getLogger()


class Colours(Enum):
    ORANGE = "\033[38;2;255;165;0m"
    GREEN = Fore.GREEN
    RED = Fore.RED


def display_responses(responses: list[ResponseResult], host: str):
    coloured_data = [
        [
            f"/{resp.path}",
            colour_status_codes(resp.status_code),
            resp.size,
            resp.content_type,
            resp.server,
        ]
        for resp in responses
    ]
    table = tabulate(
        coloured_data,
        headers=["Path", "HTTP Status", "Size", "Content-Type", "Server"],
        tablefmt="fancy_outline",
    )
    table_width = len(table.splitlines()[0])
    title = f"==================== {host} Directories ====================".center(
        table_width
    )
    logger.info("\n%s\n%s", title, table)


def colour_status_codes(status_code: int) -> str:
    match status_code:
        case 200 | 301 | 300:
            colour = Colours.GREEN.value
        case 403 | 401:
            colour = Colours.ORANGE.value
        case _:
            colour = Colours.RED.value
    return colour + str(status_code) + Style.RESET_ALL
