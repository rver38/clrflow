#made with support from my dearest friend mejta
#gng twin cuh

import os, colour, numpy, re, itertools

os.system("")

# universal ######################################################################

def fallback(priority, fallback, condition=None): # consider replacing ts with priorityChain in the code
    return priority if priority != condition else fallback

def priorityChain(chain, fallback=None, condition=None):
    for x in tuple(chain):
        if x != condition:
            return x
    return fallback

_ansiRe = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
def removeAllEscapeCodes(text:str):
    return _ansiRe.sub('',text)

# representation optimization ####################################################

# xterm 16-256 colorcode generator
rgb_to_code = {} #convert rgb to colorcode
levels = [0, 95, 135, 175, 215, 255]

rgb_to_code.update({
    (r, g, b): 16 + i
    for i, (r, g, b) in enumerate(itertools.product(levels, repeat=3))
})

for i in range(24):
    gray = 8 + i * 10
    rgb_to_code[(gray, gray, gray)] = 232 + i #very unreadable code ‼‼‼!!!

def _getColorCode(prefix, color):
    code = rgb_to_code.get(tuple(color))
    if code is not None:
        return f"{prefix}8;5;{code}"
    return f"{prefix}8;2;{color[0]};{color[1]};{color[2]}"

# simple formatting ##############################################################