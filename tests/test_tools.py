import pytest
from tools import calculate

def test_add():
    assert calculate.invoke({"a": 2, "b": 3, "operation": "add"}) == 5

def test_multiply():
    assert calculate.invoke({"a": 67, "b": 89, "operation": "multiply"}) == 5963

def test_divide_by_zero():
    with pytest.raises(ValueError):
        calculate.invoke({"a": 1, "b": 0, "operation": "divide"})
