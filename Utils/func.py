import time


def wait(val: int) -> None:
    start = time.time()
    while (time.time() - start < val):
        pass
