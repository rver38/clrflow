#i am really weak
import re, itertools, math
from collections.abc import Sequence
from typing import TypeAlias

# add ansi container or some typa thing

def fallback(priority, fallback, condition=None):
    return priority if priority != condition else fallback

def priorityChain(chain, fallback=None, condition=None):
    for x in tuple(chain):
        if x != condition:
            return x
    return fallback

_ansiRe = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
def removeAllEscapeCodes(text:str):
    return _ansiRe.sub('',text)

# xterm 16-256 colorcode generator
_rgb_to_code = {}
_levels = [0, 95, 135, 175, 215, 255]

_rgb_to_code.update({
    (r, g, b): 16 + i
    for i, (r, g, b) in enumerate(itertools.product(_levels, repeat=3)) # yes vibecoded
})
for i in range(24):
    gray = 8 + i * 10
    _rgb_to_code[(gray, gray, gray)] = 232 + i

def getColorTerm(prefix, color): # not an abbreviation
    code = _rgb_to_code.get(tuple(color))
    if code is not None:
        return f"{prefix}8;5;{code}"
    return f"{prefix}8;2;{color[0]};{color[1]};{color[2]}"

#temp
def rv_DEBUG(*args, wait:bool=False):
    import sys
    frame = sys._getframe()
    f_back = frame.f_back
    debugStr = f"LINE[{f_back.f_lineno}] FUNC[{f_back.f_code.co_name}] | {args}"
    if wait:
        input(debugStr)
    else:
        print(debugStr)

type Number = int | float
"""a single number; typically an integer between 0-360 or a float between 0.0-1.0"""

XYZ: TypeAlias = tuple[Number, Number, Number]
"""a number triplet; typically used for representing colors:

three integers between 0-255 for **RGB colors**, and

three integers in the ranges [0-360, 0-100, 0-100] or three floats between 0.0-1.0 for **HSL colors**"""