import re, itertools, math
from collections.abc import Sequence

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
_rgb_to_code = {} #convert rgb to colorcode
_levels = [0, 95, 135, 175, 215, 255]

_rgb_to_code.update({
    (r, g, b): 16 + i
    for i, (r, g, b) in enumerate(itertools.product(_levels, repeat=3))
})
for i in range(24):
    gray = 8 + i * 10
    _rgb_to_code[(gray, gray, gray)] = 232 + i

def getAnsiTerm(prefix, color): # literal term, not an abbreviation
    code = _rgb_to_code.get(tuple(color))
    if code is not None:
        return f"{prefix}8;5;{code}"
    return f"{prefix}8;2;{color[0]};{color[1]};{color[2]}"

def ColorTypeHelper(color, isHsl, normalized, asHsl=None):
    ...
    
def shortRepr(x, lengthMax=50, lengthPer=25): # garbage collect
    match x:
        case bool():
            return str(x)
        case int():
            l = len(str(x))
            
            if l <= lengthMax:
                return str(x)
            
            math.floor(math.log10())+1
            
# 