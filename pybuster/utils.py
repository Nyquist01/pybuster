import time


def timer(func):
    def wrapper(*args):
        start_t = time.perf_counter()
        func(*args)
        end_t = time.perf_counter()
        duration = end_t - start_t
        print(f"Took {duration}s to finish")

    return wrapper
