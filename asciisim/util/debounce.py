import time


class Debounce(object):
    def __init__(self, delay: int):
        self.delay: int = delay
        self.last_executions = {}

    def __call__(self, func):
        def inner(instance, *args, **kwargs):
            milliseconds = time.time_ns() // 1000000
            key = id(instance)
            if key not in self.last_executions:
                self.last_executions[key] = 0

            if milliseconds - self.last_executions[key] < self.delay:
                return

            self.last_executions[key] = milliseconds

            return func(instance, *args, **kwargs)

        return inner
