import itertools

def fallback(priority, fallback, condition=None):
    return priority if priority != condition else fallback

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

def getColorTerm(prefix, color):
    code = _rgb_to_code.get(tuple(color))
    if code is not None:
        return f"{prefix}8;5;{code}"
    return f"{prefix}8;2;{color[0]};{color[1]};{color[2]}"