import logging
import time

logger = logging.getLogger()


class Timer:
    """
    Context manager to measure total time to enumerate all target paths
    """

    def __init__(self, target_host: str, target_paths: list[str]):
        self.target_paths = target_paths
        self.target_host = target_host

    def __enter__(self):
        self.start_t = time.perf_counter()

    def __exit__(self, exc_type, exc_value, exc_traceback):
        end_t = time.perf_counter()
        duration = end_t - self.start_t
        logger.info(
            "Took %s seconds to enumerate %s paths for %s",
            round(duration, 2),
            len(self.target_paths),
            self.target_host,
        )


def setup_logging():
    logging.basicConfig(
        format="%(asctime)s [%(levelname)s] %(message)s",
        encoding="utf-8",
        level=logging.INFO,
        handlers=[logging.FileHandler("pybuster.log"), logging.StreamHandler()],
    )


def get_target_paths(file_path: str) -> list[str]:
    with open(file_path) as file:
        return file.read().split("\n")
