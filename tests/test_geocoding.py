import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from geocoding import distancia_millas


def test_distancia_millas():
    # Distancia aproximada entre Nueva York (40.7128, -74.0060)
    # y Los Ángeles (34.0522, -118.2437) ~ 2445 millas
    d = distancia_millas(40.7128, -74.0060, 34.0522, -118.2437)
    assert 2400 < d < 2500
