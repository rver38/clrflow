from typing import TypeAlias, NamedTuple

Number = int | float
"""a single numeric value, either int or float"""

class Triplet(NamedTuple):
    """a tuple of 3 `Number`s, commonly used to represent color data"""
    x: Number
    y: Number
    z: Number