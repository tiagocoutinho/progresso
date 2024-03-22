# progresso

[![progresso][pypi-version]](https://pypi.python.org/pypi/progresso)
[![Python Versions][pypi-python-versions]](https://pypi.python.org/pypi/progresso)
![License][license]
[![CI][CI]](https://github.com/tiagocoutinho/progresso/actions/workflows/ci.yml)


A simple library that aims at making hierarchical progress
iterators / generators easy.

A single point API: `progresso(it: Iterable, start: float = 0, end: float = 100) -> Iterable`

I'll use the term task to mean any python iterable or generator.

Rules of the game:

1. Each task is responsible of generating (yielding) incremental progress between [0, 100].
2. The task is free to generate any number of steps (min 1)
3. The task is free to start at any point as long as the value is between [0,100]
4. Value is truncated to max(value, 0)
5. Value is truncated to min(value, 100)
6. If a value is less than previous it is discarded (I can be convinced otherwise to emulate
   progress regressing)
7. If the task last value is less than 100, an extra value 100 is generated

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

[pypi-python-versions]: https://img.shields.io/pypi/pyversions/progresso.svg
[pypi-version]: https://img.shields.io/pypi/v/progresso.svg
[pypi-status]: https://img.shields.io/pypi/status/progresso.svg
[license]: https://img.shields.io/pypi/l/progresso.svg
[CI]: https://github.com/tiagocoutinho/progresso/actions/workflows/ci.yml/badge.svg
