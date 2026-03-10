import pytest
from a_maze_ing import add, divide

def test_add_basic():
    assert add(20,30) == 50

def test_add_negative():
    assert add(-1, -1) == -2

def test_add_normal():
    assert divide(20, 2) == 10

def test_divide_by_zero():
    with pytest.raises(ValueError):
        divide(10, 0)