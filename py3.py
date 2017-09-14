from typing import Type


class suppress(object):
    def __init__(self, *exceptions):  # type: (Type) -> None
        """Stores given exception types.

        :param exceptions: Exception types to be suppressed.
        """
        self.exceptions = exceptions

    def __enter__(self):  # type: () -> None
        """Does nothing."""

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Throws if raised exception type is not a subtype of given exceptions to suppress."""
        return exc_type is None or issubclass(exc_type, self.exceptions)

