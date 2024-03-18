# This file is part of the progresso project
#
# Copyright (c) 2024 Tiago Coutinho
# Distributed under the GPLv3 license. See LICENSE for more info.

from math import isclose

import pytest
from hypothesis import assume, given, strategies as st

from progresso import progresso, scale


@given(st.floats(0, 100))
def test_scale_nothing(x):
    assert isclose(scale(x, 0, 100), x)


@given(st.floats(0, 100))
def test_scale(x):
    assert isclose(scale(x, 0, 100), x)


@given(st.floats())
def test_scale_out_of_range(x):
    assume(not 0 <= x <= 100)
    matches = r"Expected value in range \[0, 100\]"
    with pytest.raises(ValueError, match=matches):
        scale(x, 0, 100)

    with pytest.raises(ValueError, match=matches):
        scale(0, x, 0)

    with pytest.raises(ValueError, match=matches):
        scale(0, 0, x)


@given(st.floats(0, 100), st.floats(0, 100), st.floats(0, 100))
def test_scale_wrong_range(value, start, end):
    assume(end < start)
    with pytest.raises(ValueError, match="Expected start <= end"):
        scale(value, start, end)


@given(st.floats(), st.floats(), st.floats())
def test_scale_all(value, start, end):
    if any(not 0 <= x <= 100 for x in (value, start, end)):
        with pytest.raises(ValueError):
            scale(value, start, end)
    elif end < start:
        with pytest.raises(ValueError):
            scale(value, start, end)
    else:
        expected = start + value * (end - start) / 100
        assert isclose(scale(value, start, end), expected)


def assert_progress(it, expected):
    assert list(progresso(it)) == list(expected)


def test_progresso_basic():
    it = [0, 10, 100]
    assert_progress(it, it)
    assert_progress(iter(it), it)

    def gen():
        yield from it

    assert_progress(gen(), it)


def test_progresso_negative():
    assert_progress([-1, 10, 100], [0, 10, 100])


def test_progresso_doesnt_reach_100():
    assert_progress([0, 10, 90], [0, 10, 90, 100])


def test_progresso_goes_back():
    assert_progress([0, 10, 9, 100], [0, 10, 100])
    assert_progress([-5, -10, 10, 9, 100], [0, 10, 100])


def test_progresso_repeated_values():
    assert_progress([0, 10, 10, 100], [0, 10, 100])
    assert_progress([0, 0, 10, 10, 100], [0, 10, 100])
    assert_progress([-1, 0, 10, 10, 100], [0, 10, 100])
    assert_progress([-1, 0, 10, 10, 100, 100], [0, 10, 100])
    assert_progress([-3, -5, 0, 10, 10, 100, 100, 109, 105], [0, 10, 100])


def test_progresso_hierarchical():
    def task():
        yield 10
        yield from progresso(range(0, 100, 20), 10, 20)
        yield 90

    assert_progress(task(), [10] + [12, 14, 16, 18, 20] + [90, 100])
