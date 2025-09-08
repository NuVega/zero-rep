import pytest
from main import count_vowels

def test_only_vowels():
    assert count_vowels("aeiouAEIOUаеёиоуыэюяАЕЁИОУЫЭЮЯ") == len("aeiouAEIOUаеёиоуыэюяАЕЁИОУЫЭЮЯ")

def test_no_vowels():
    assert count_vowels("bcdfgBCDFGйцкншщзхфвпрлджчсмт") == 0

def test_mixed_string():
    assert count_vowels("Hello, Привет!") == 4

def test_empty_string():
    assert count_vowels("") == 0