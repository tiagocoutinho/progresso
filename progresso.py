# This file is part of the progresso project
#
# Copyright (c) 2024 Tiago Coutinho
# Distributed under the GPLv3 license. See LICENSE for more info.

"""
A simple library that aims at making hierarchical progress
iterators / generators easy.

A single point API: `progresso(it: Iterable, start: float = 0, end: float = 100) -> Iterable`

Example:

```python
>>> def task_1():
...     yield 10
...     yield 90
...     yield 100
...

>>> def task_2():
...     yield 5
...     yield 2
...     yield 99
...

>>> def task():
...     yield 30
...     yield from progresso(task_1(), 30, 60)
...     yield from progresso(task_2(), 60, 90)

>>> for i in progresso(task()):
...     print(i)
30.0
33.0
57.0
60.0
61.5
89.7
90.0
100.0
```
"""

__version__ = "0.1.0"


from collections.abc import Iterable
from typing import TypeVar

T = TypeVar("T")


def scale(value: float, start: float, end: float) -> float:
    """
    Returns the value (expected to be in [0, 100])
    scaled between the given range
    """
    if any(not 0 <= x <= 100 for x in (value, start, end)):
        raise ValueError("Expected value in range [0, 100]")
    if not start <= end:
        raise ValueError("Expected start <= end")
    return start + value * (end - start) / 100


def naive_scaled(it: Iterable[T], start: float, end: float) -> Iterable[T]:
    """
    For each value in the given *it*, scales it to the range [start, end] and
    emits that result
    The it is expected to give progressively increasing values between [0, 100]
    The start and end are expected to be in the range [0, 100] and it is expected
    that end >= start.
    """
    return (scale(value, start, end) for value in it)


def bound_scaled(it: Iterable[T]) -> Iterable[T]:
    """
    For each value in the given *it*, te yields it but first ensures that:

    * value is bound between [0, 100]
    * value is never less or equal than previous value
    * last value is 100
    """
    last = 0
    for i, value in enumerate(it):
        value = min(max(last, value), 100)
        if i and value <= last:
            continue
        yield value
        last = value
    if last < 100:
        yield 100


def safe_scaled(it: Iterable[T], start: float = 0, end: float = 100) -> Iterable[T]:
    """
    Transforms the given *it* ensuring the values are strictly progressive in
    the range [start, end]
    """
    return naive_scaled(bound_scaled(it), start, end)


progresso = safe_scaled
