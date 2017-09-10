import builtins
from itertools import count


def sum_range(*args):
	if len(args) == 1:
		return _sum_range_limit(*args)
	elif 1 < len(args) < 4:
		return _sum_range_full(*args)
	raise TypeError("sum_range takes 1 to 3 arguments ({} given)".format(len(args)))

def _sum_range_limit(stop):
	return stop * (stop+1) / 2
	
def _sum_range_full(start, stop, step=None):
	if step:
		return _sum_range_full(start // step, stop // step) * step
	return _sum_range_limit(stop) - _sum_range_limit(start)


def enumerate(iterable, start=0, reverse=False):
    """Reverse works only for sequences."""
    return (zip(count(start or len(iterable) - 1, -1), reversed(iterable))
            if reverse else builtins.enumerate(iterable, start))


class ReversibleEnumerate(object):
    def __init__(self, iterable, start=0, reverse=False):
        self._iterable = iterable
        self._start = start
        self.iterable = iter(iterable if not reverse else reversed(iterable))
        self.counter = count(start) if not reverse else count(start or len(iterable) - 1, -1)

    def __iter__(self):
        return self

    def next(self):
        return next(self.counter), next(self.iterable)
    
    def __reversed__(self):
        return type(self)(self._iterable, self._start, reverse=True)

