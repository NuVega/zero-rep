import pytest
from main import safe_modulo

def test_modulo_positive_numbers():
    assert safe_modulo(10, 3) == 1

def test_modulo_negative_numbers():
    assert safe_modulo(-10, 3) == 2

def test_modulo_dividend_zero():
    assert safe_modulo(0, 5) == 0

def test_modulo_divisor_zero():
    assert safe_modulo(5, 0) is None

def test_modulo_both_zero():
    assert safe_modulo(0, 0) is None