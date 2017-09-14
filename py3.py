class suppress(object):
    def __init__(self, *exceptions):
        self.exceptions = set(exceptions)

    def __enter__(self):
        """Does nothing."""

    def __exit__(self, exc_type, exc_val, exc_tb):
        return exc_type is None or exc_type in self.exceptions

