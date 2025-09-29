import time


def timer(func):
    def wrapper(*args):
        start_t = time.perf_counter()
        func(*args)
        end_t = time.perf_counter()
        duration = end_t - start_t
        print(f"Took {round(duration, 2)} seconds")

    return wrapper
