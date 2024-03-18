# progresso

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
