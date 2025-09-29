from enum import Enum

from colorama import Fore, Style
from tabulate import tabulate

from .requester import ResponseResult


class Colours(Enum):
    ORANGE = "\033[38;2;255;165;0m"


def display_responses(responses: list[ResponseResult], host: str):
    coloured_data = [
        [
            f"/{resp.path}",
            colour_status_codes(resp.status_code),
            resp.size,
            resp.content_type,
        ]
        for resp in responses
    ]
    table = tabulate(
            coloured_data,
            headers=["Path", "Status", "Size", "Content-Type"],
            tablefmt="fancy_outline",
        )
    table_width = len(table.splitlines()[0])
    print("\n")
    print(f"==================== {host} Directories ====================".center(table_width))
    print(table)


def colour_status_codes(status_code: int) -> str:
    match status_code:
        case 200:
            colour = Fore.GREEN
        case 403 | 401:
            colour = Colours.ORANGE.value
        case _:
            colour = Fore.RED
    return colour + str(status_code) + Style.RESET_ALL
