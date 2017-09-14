from itertools import chain
from functools import partial
from collections import deque

from .py3 import suppress

globals_ = globals()


def unhashable_isdisjoint(iterable1, iterable2):
    return _is_iterator_empty(unhashable_intersection(iterable1, iterable2))


def unhashable_issubset(iterable1, iterable2):
    return _is_iterator_empty(unhashable_difference(iterable1, iterable2))


def unhashable_issuperset(iterable1, iterable2):
    """"""


def unhashable_union(*iterables):
    for item in unhashable_unique(chain(*iterables)):
        yield item


def unhashable_intersection(*iterables):
    """"""


def unhashable_difference(iterable, *iterables):
    items = list(unhashable_union(*iterables))

    for item in unhashable_unique(iterable):
        if item not in items:
            yield item


def unhashable_symmetric_difference(iterable1, iterable2):
    others = list(unhashable_unique(iterable2))

    for item in unhashable_unique(iterable1):
        if item not in others:
            yield item
        else:
            others.remove(item)

    for item in others:
        yield item


def unhashable_symmetric_difference_deque(iterable1, iterable2):
    queue2 = deque(unhashable_unique(iterable2))

    for item in unhashable_unique(iterable1):
        if item not in queue2:
            yield item
        else:
            queue2.remove(item)

    for item in queue2:
        yield item


def __unhashable_symmetric_difference(iterable1, iterable2):
    queue2 = deque(unique(iterable2))

    for item in unique(iterable1):
        try:
            queue2.remove(item)
        except ValueError:
            pass
        else:
            yield item

    for item in queue2:
        yield item


def __unhashable_symmetric_difference_2(iterable1, iterable2):
    queue2 = deque(unique(iterable2))
    type_value_suppressor = suppress(ValueError)

    for item in unique(iterable1):
        with type_value_suppressor:
            queue2.remove(item)
            yield item  # Not executed when exception occurs.

    for item in queue2:
        yield item


def __unhashable(unhashable_function, operation, *iterables):
    """
    def symmetric_difference(iterable1, iterable2):
        return (_try_set_operation(iterable1, iterable2, set.symmetric_difference)
                or unhashable_symmetric_difference(iterable1, iterable2))
    """
    return (_try_set_operation(operation=operation, *iterables)
            or unhashable_function(*iterables))


# SET_OPERATIONS = {
#     'isdisjoint': set.isdisjoint,
#     'issubset': set.issubset,
#     'issuperset': set.issuperset,
#     'union *': set.union, # *
#     'intersection *': set.intersection, # *
#     'difference *': set.difference, # *
#     'symmetric_difference': set.symmetric_difference
# }
# for func_name, operation in SET_OPERATIONS.iteritems():
#     unhashable_function = globals_['unhashable_' + func_name]
#     globals_[func_name] = partial(__unhashable, unhashable_function, operation)


isdisjoint = partial(__unhashable, unhashable_isdisjoint, set.isdisjoint)
issubset = partial(__unhashable, unhashable_issubset, set.issubset)
issuperset = partial(__unhashable, unhashable_issuperset, set.issuperset)
union = partial(__unhashable, unhashable_union, set.union)
intersection = partial(__unhashable, unhashable_intersection, set.intersection)
difference = partial(__unhashable, unhashable_difference, set.difference)
symmetric_difference = partial(__unhashable, unhashable_symmetric_difference,
                               set.symmetric_difference)


def are_equal():



def unique(iterable):
    for item in _try_set(iterable) or unhashable_unique(iterable):
        yield item


def unhashable_unique(iterable):
    seen = deque()
    for item in iterable:
        if item not in seen:
            seen.append(item)
            yield item


def _try_set_operation(iterable1, iterable2, operation):
    return _try_unhashable_type(operation, iterable1, iterable2)


def _try_set(iterable):
    return _try_unhashable_type(set, iterable)


def _try_unhashable_type(func, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except TypeError as ex:
        if 'unhashable type' not in ex:
            raise


def _is_iterator_empty(iterator):
    try:
        next(iterator)
    except StopIteration:
        return True
    return False

