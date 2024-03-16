from math import isclose


import pytest
from hypothesis import assume, given, strategies as st

from progresso import scale
    

@given(st.floats(0, 100))
def test_scale_nothing(x):
    assert isclose(scale(x, 0, 100), x)


@given(st.floats(0, 100))
def test_scale(x):
    assert isclose(scale(x, 0, 100), x)


@given(st.floats())
def test_scale_out_of_range(x):
    assume(not 0 <= x <= 100)
    with pytest.raises(ValueError):
        scale(x, 0, 100)

    with pytest.raises(ValueError):
        scale(0, x, 0)

    with pytest.raises(ValueError):
        scale(0, 0, x)


@given(st.floats(0, 100), st.floats(), st.floats())
def test_scale_wrong_range(value, start, end):
    assume(end < start)
    with pytest.raises(ValueError):
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