from typing import TypeAlias, Sequence

Number = int | float
"""a single numeric value, either int or float"""

Triplet: TypeAlias = Sequence[Number, Number, Number]
"""a sequence of 3 `Number`s, commonly used to represent color data"""
