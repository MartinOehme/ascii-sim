import time


class Debounce(object):
    def __init__(self, delay: int):
        self.delay: int = delay
        self.last_execution = 0

    def __call__(self, func):
        def inner(*args, **kwargs):
            milliseconds = time.time_ns() // 1000000
            if milliseconds - self.last_execution < self.delay:
                return

            self.last_execution = milliseconds

            return func(*args, **kwargs)

        return inner
