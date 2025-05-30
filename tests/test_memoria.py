import os
import sys
import pytest

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from memoria import comparar_nombres


def test_comparar_nombres_similares():
    assert comparar_nombres("Ace Hardware", "ACE hardware") is True


def test_comparar_nombres_diferentes():
    assert comparar_nombres("Ace Hardware", "Home Depot") is False
