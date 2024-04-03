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


def scale(step: float, start: float, end: float) -> float:
    """
    Returns the step (expected to be in [0, 100])
    scaled between the given range
    """
    if any(not 0 <= x <= 100 for x in (step, start, end)):
        raise ValueError("Expected value in range [0, 100]")
    if not start <= end:
        raise ValueError("Expected start <= end")
    return start + step * (end - start) / 100


def progresso(it: Iterable[T], start: float = 0, end: float = 100) -> Iterable[T]:
    """
    Transforms the given *it* ensuring the values are strictly progressive in
    the range [start, end]
    """
    last = 0
    for i, step in enumerate(it):
        step = min(max(last, step), 100)
        if i and step <= last:
            continue
        yield scale(step, start, end)
        last = step
    if last < 100:
        yield scale(100, start, end)
