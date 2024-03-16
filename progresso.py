#
# This file is part of the progresso project
#
# Copyright (c) 2024 Tiago Coutinho
# Distributed under the GPLv3 license. See LICENSE for more info.

__version__ = "0.1.0"


from typing import TypeVar
from collections.abc import Iterable

T = TypeVar("T")


def scale(value: float, start: float, end: float) -> float:
    """
    Returns the value (expected to be in [0, 100])
    scaled between the given range
    """
    if any (not 0 <= x <= 100 for x in (value, start, end)):
        raise ValueError("Expected value in range [0, 100]")
    if not start <= end:
        raise ValueError("Expected start <= end")
    return start + value * (end - start) / 100


def naive_scaled(it: Iterable[T], start: float, end: float) -> Iterable[T]:
    return (scale(value, start, end) for value in it)


def bound_scale(it: Iterable[T]) -> Iterable[T]:
    """
    Ensures that:
    * values are bound between [0, 100]
    * value is never less than previous value
    * last value is 100
    """
    last = 0
    for value in it:
        value = min(max(last, value), 100)
        yield value
        last = value
    if last < 100:
        yield 100


def safe_scaled(it: Iterable[T], start: float, end: float) -> Iterable[T]:
    return naive_scaled(bound_scale(it), start, end)


scaled = safe_scaled

# ---------------------

def sub_task_1():
    yield 1
    yield 30
    yield 75
    yield 100


def sub_task_2():
    yield from range(10, 100, 21)


def sub_task_3():
    yield -5
    yield 55
    yield 23
    yield 98


def task_1():
    yield 10

    yield from safe_scaled(sub_task_1(), 10, 30)

    yield from safe_scaled(sub_task_2(10, 100, 25), 30, 45)

    yield from safe_scaled(sub_task_3(), 45, 80)
    yield 80
    yield 99


def main():
    for i in safe_scaled(main(), 0, 100):
        print(i)
    

if __name__ == "__main__":
    main()