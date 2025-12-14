#made with support from my dearest friend mejta
#gng twin cuh

import os, colour, numpy, math, shutil, re
from typing import Sequence, Optional, Union, TypeAlias, Tuple

os.system("")

#improvs
#Color, RichText + Align + Gradient

#to add
#decipher() - anim type thing that turns a random string step by step to the original
#typewrite() - take a guess
#progressbars
#console wraparound type sh
#look at Color and everything else once more
#finish adding hsl-smoothing and fix ColorNew
#parser that converts strings with markers like [red], [center] etc into richtext
#i guess make a more intelligent stripper LE MAO to preserve escape codes in the input text if there are any
#extend and improve Format
#add screen buffer to support underwriting (preserving text while changing color), overwriting (preserving color while changing text), positionable printing and so on
#change defaulting to not affect color (^^^ probably related to buffer ^^^)
#consider merging updateReference and the align logic
#colorsequence currently doesnt invert if input is already a colorsequence

# UNIVERSAL ########################################################################################################################################################################

def fallback(priority, fallback, condition=None): # consider replacing ts with priorityChain in the code
    return priority if priority != condition else fallback

def priorityChain(chain, fallback=None, condition=None):
    for x in tuple(chain):
        if x != condition:
            return x
    return fallback

def removeAllEscapeCodes(text:str):
    return re.sub(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])",'',text)

rgb_to_code = {} #convert rgb to colorcode
levels = [0, 95, 135, 175, 215, 255]
code = 16
for r in levels:
    for g in levels:
        for b in levels:
            rgb_to_code[(r, g, b)] = code
            code += 1
for i in range(24):
    gray = 8 + i * 10
    rgb_to_code[(gray, gray, gray)] = 232 + i #very unreadable code ‼‼‼!!!

def _getCode(prefix, color):
    code = rgb_to_code.get(tuple(color))
    if code is not None:
        return f"{prefix}8;5;{code}"
    return f"{prefix}8;2;{color[0]};{color[1]};{color[2]}"

# FORMAT ###########################################################################################################################################################################

class Fore:
    """a collection of foreground coloring ansi escape codes"""
    reset = "\033[0m"
    black = "\033[30"
    white = "\033[37m"
    red = "\033[31m"
    green = "\033[32m"
    blue = "\033[34m"
    cyan = "\033[96m"
    magenta = "\033[35m"
    yellow = "\033[33m"

class Back:
    """a collection of background coloring ansi escape codes"""
    reset = "\033[0m"
    black = "\033[40"
    white = "\033[47m"
    red = "\033[41m"
    green = "\033[42m"
    blue = "\033[44m"
    cyan = "\033[106m"
    magenta = "\033[45m"
    yellow = "\033[43m"

class Format:
    reset = "\033[0m"
    
    bold = "\033[1m"
    dim = "\033[2m"
    italic = "\033[3m"
    underline = "\033[4m"
    blink = "\033[5m"
    blink2 = "\033[6m"
    inverse = "\033[7m"
    hidden = "\033[8m"
    strikethrough = "\033[9m"
    
    _zippedProperties = dict(zip("BDIUbihs",(1,2,3,4,5,7,8,9)))
    
    def __init__(self,options:str):
        """format object, can be added together with strings to format them or be returned as a string
        
        - B: bold
        - D: dim
        - I: italic
        - U: underline
        - b: blink
        - i: inverse
        - h: hidden
        - s: strikethrough
        
        example usage:
        ```python
        print(clrflow.format("BIUs")+"hello there")  # this prints the text in bold, italic, underlined and strikethrough
        ```

        arguments:
        - s (str): characters corresponding to their formatting options
        """
        self.escape = f"\033[{';'.join(self._zippedProperties.get(option,'') for option in options)}m"
    
    def __add__(self,other):
        return self.escape+other
    
    def __str__(self):
        return self.escape

class Color:
    assumeHsl = False

    @staticmethod
    def normalHelper(color: Sequence, isHsl: bool=False, normal: bool=None):
        #if normal is none, flip, else make it whatever normal is, in the provided color format
        
        if not (all(isinstance(o, (int, float)) for o in color) and len(color)==3):
            raise ValueError("color must be a Sequence of exactly 3 numbers")
        
        current = isinstance(color[0], float) and max(color) <= 1
        target = fallback(normal, not current)
        
        if current == target:
            return color
        
        if isHsl:
            hMultiplier = 1/360 if target else 360
            slMultiplier = 0.01 if target else 100
            h, s, l = color
            return (h*hMultiplier, s*slMultiplier, l*slMultiplier)
        else:
            rgbMultiplier = 1/255 if target else 255
            return tuple(int(val*rgbMultiplier) for val in color)
        
    @staticmethod
    def parse(x,y,z, isHsl):
        colorTable = { #yo FIX this
            "black":   "#000000",
            "white":   "#FFFFFF",
            "red":     "#FF0000",
            "green":   "#00FF00",
            "blue":    "#0000FF",
            "yellow":  "#FFFF00",
            "cyan":    "#00FFFF",
            "magenta": "#FF00FF",
            "orange":  "#FF8800",
            "purple":  "#800080",
            "gray":    "#A0A0A0", #hihihi hohoho
            "grey":    "#606060", #eeny meeny tiny toe
            "pink":    "#FFC0CB",
            "brown":   "#903A00",
        }

        if isinstance(x, Color):
            return x.rgb, x.hsl
        elif isinstance(x, str):
            x = colorTable.get(x.lower(), x)
            return colour.hex2rgb(x), colour.hex2hsl(x)
        
        if isinstance(x, Sequence): #note that str is also considered a Sequence, handle it explicitly earlier, like here
            if len(x) != 3:
                raise ValueError("if x is a Sequence, it must consist of 3 numbers")
            xyz = x
        else:
            xyz = (x, y, z)

        if not all(isinstance(o, (int, float)) for o in xyz):
            raise ValueError("x must be a str or a Sequence of 3 numbers, unless x, y, and z are all numbers")

        xyz = Color.normalHelper(xyz, isHsl, True)
        rgb = Color.normalHelper(colour.hsl2rgb(xyz) if isHsl else xyz, False, False)
        hsl = xyz if isHsl else colour.rgb2hsl(xyz)
        return rgb, hsl
    
    def __init__(self, 
        x: Union[int, float, str, Tuple[int, int, int], Tuple[float, float, float]], y: Optional[Union[int, float]] = None, z: Optional[Union[int, float]] = None, background: bool=False, isHsl: bool=None) -> str: #ts is too long
        
        self.background = background
        isHsl = fallback(isHsl, Color.assumeHsl)
        self.rgb, self.hsl = self.parse(x, y, z, isHsl)
    
    @staticmethod
    def ansi(color=None, background:bool=False):
        return f"\033[{_getCode(4 if background else 3, color)}m"
    
    def __str__(self):
        return self.ansi(self.rgb, self.background)
    def __add__(self, other):
        return str(self)+str(other)
    def __radd__(self, other):
        return str(other)+str(self)
    
    def __call__(self, as_dict=False, as_hex=False, rgb_tuple=False, hsl_tuple=False, inverted=False, complementary=False):
        r, g, b = self.rgb
        h, s, l = self.hsl
        rgb_dirty = hsl_dirty = False

        if complementary:
            h, s, l = ((h+0.5)%1, s, 1-l)
            rgb_dirty = True

        if rgb_dirty and (as_dict or as_hex or rgb_tuple or inverted):
            r, g, b = colour.hsl2rgb((h,s,l), True, False)

        if inverted:
            r, g, b = (255-r, 255-g, 255-b)
            hsl_dirty = True
        
        if hsl_dirty and (as_dict or hsl_tuple):
            h, s, l = colour.rgb2hsl(self.normalHelper((r,g,b), False, True))
                
        if rgb_tuple and hsl_tuple:
            return (r, g, b), (h, s, l)
        if rgb_tuple:
            return (r, g, b)
        if hsl_tuple:
            return (h, s, l)
        if as_dict:
            return {"r":r, "g":g, "b":b, "h":h, "s":s, "l":l, "rgb":(r,g,b), "hsl":(h,s,l)}
        if as_hex:
            return '#%02x%02x%02x' % (r, g, b)
        return self.ansi((r, g, b), self.background) # cause rgb may differ here due to inverted / complementary

# sigma ###############################################################################################################################################################################
_savedGradients = {}
_ColorSequenceType: TypeAlias = Optional[Sequence[Color]|bool]
_LenFactorType: TypeAlias = Optional[float|int]

class ColorSequence:
    def __init__(self, colors: Sequence, isHsl:bool=False, asHsl:Optional[bool]=None, inverted:bool=False):
        self.asHsl = fallback(asHsl, isHsl) or False

        if isinstance(colors, ColorSequence):
            self.rgb = colors.rgb
            self.hsl = colors.hsl
            self.asHsl = priorityChain([asHsl, colors.asHsl, isHsl], fallback=False)
        elif not colors:
            self.rgb, self.hsl = (),()
        else:
            self.rgb, self.hsl = self.computeColors(colors, isHsl, inverted, False)
    
    @staticmethod
    def computeColors(colors:Sequence=None, isHsl:bool=False, inverted:bool=False, complementary:bool=False, normalized:bool=False):
        colors = [Color(c, isHsl=isHsl) for c in colors]

        colors = [(color(rgb_tuple=True, hsl_tuple=True, inverted=inverted, complementary=complementary)) for color in colors]
        rgb, hsl = zip(*colors) # turns (1,2),(3,4),(5,6) into (1,3,5),(2,4,6)

        if normalized:
            rgb = [Color.normalHelper(c, False, True) for c in rgb]
            hsl = [Color.normalHelper(c, True, True) for c in hsl] #technically unnecessary

        return rgb, hsl
    
    def __bool__(self):
        return bool(self.rgb and self.hsl)

class Gradient:
    def __init__(self, foregroundColors:_ColorSequenceType=None, backgroundColors:_ColorSequenceType=None, foreName:Optional[str]=None, backName:Optional[str]=None, vertical:Optional[bool]=None, resolution:Optional[int]=None, terminal:Optional[bool]=None, reverse:Optional[bool]=None, lengthFactor:_LenFactorType=None, foreIsHsl:bool=None, backIsHsl:bool=None, foreAsHsl:Optional[bool]=None, backAsHsl:Optional[bool]=None):
        if foreName:
            tmp = _savedGradients.get(foreName.lower())
            if tmp:
                foregroundColors = fallback(foregroundColors, tmp)
            elif foregroundColors:
                _savedGradients[foreName.lower()] = ColorSequence(foregroundColors, foreIsHsl, foreAsHsl)
                
        if backName: 
            tmp = _savedGradients.get(backName.lower())
            if tmp:
                backgroundColors = fallback(backgroundColors, tmp)
            elif backgroundColors:
                _savedGradients[backName.lower()] = ColorSequence(backgroundColors, backIsHsl, backAsHsl)
        self.foreColors = ColorSequence(foregroundColors, foreIsHsl, foreAsHsl) if foregroundColors else None
        self.backColors = ColorSequence(backgroundColors, backIsHsl, backAsHsl) if backgroundColors else None
        self.vertical = vertical
        self.resolution = resolution
        self.terminal = terminal
        self.lenFactor = lengthFactor
        self.reverse = reverse
        self.foreIsHsl = foreIsHsl
        self.backIsHsl = backIsHsl
    
    def _match(self, seq, other):
        if isinstance(seq, (ColorSequence, Sequence)):
            return seq
        elif isinstance(seq, bool):
            if isinstance(other, (ColorSequence, Sequence)):
                return ColorSequence(other, inverted=seq)
        raise ValueError("atleast one of seq or other must be a Sequence of color-like items")
    
    def __call__(self, text, foregroundColors:_ColorSequenceType=None, backgroundColors:_ColorSequenceType=None, vertical:Optional[bool]=None, resolution:Optional[int]=None, terminal:Optional[bool]=None, reverse:Optional[bool]=False, lengthFactor:_LenFactorType=None, foreIsHsl:Optional[bool]=None, backIsHsl:Optional[bool]=None,foreAsHsl:Optional[bool]=None, backAsHsl:Optional[bool]=None):
        reverse = fallback(reverse,self.reverse) or False
        vertical = fallback(vertical,self.vertical) or False
        terminal =  fallback(terminal, self.terminal) or False
        resolution = fallback(resolution,self.resolution) or 1
        lenFactor =   fallback(lengthFactor, self.lenFactor) or 1.0

        foreAsHsl = fallback(foreAsHsl, self.foreIsHsl)
        backAsHsl = fallback(backAsHsl, self.backIsHsl)
        fore = fallback(foregroundColors,self.foreColors)
        back = fallback(backgroundColors,self.backColors)
        
        if not (fore or back):
            raise ValueError(f"provide atleast one Sequence of color-like items (fore={fore}, back={back})")
        
        text = _RichText(text)
        reference = text._updateReference()
        
        width = len(max(reference,key=len))
        height = len(reference)
        
        length = lenFactor or max(width, height)
        if isinstance(lenFactor, float):
            if terminal:
                # if terminal is smaller than text (for whatever reason), use text dimensions
                dimensions = (math.ceil(max(shutil.get_terminal_size().columns+1, width)/resolution), math.ceil(max(shutil.get_terminal_size().lines+1, height)/resolution))
            else:
                dimensions = (math.ceil(width/resolution), math.ceil(height/resolution))
            length = round(dimensions[vertical]*lenFactor)
        
        data = {"length": length, "vertical": vertical, "resolution": resolution, "terminal": terminal}

        if fore:
            data["foreColors"] = ColorSequence(self._match(fore, back), foreIsHsl, foreAsHsl)
        if back:
            tmp = ColorSequence(self._match(back, fore), backIsHsl, backAsHsl)
            data["backColors"] = tmp
        
        text._update(data)
        return text
    
    def listSaved(self):
        return _savedGradients.keys()

#remade from earlier clrflow
"""Gradient([Color("#ff4b4b"), Color("#ffae42"), Color("#ffee55"), Color("#6bff5f"), Color("#4dd8ff"), Color("#5b4dff"), Color("#c64dff")], foreName="rainbow")
Gradient([Color("#ff0000"), Color("#ff7b00"), Color("#ffd166")], foreName="fire")
Gradient([Color("#001f54"), Color("#005792"), Color("#00bbf0"), Color("#00f5d4")], foreName="ocean")
Gradient([Color("#2d00f7"), Color("#7b2ff7"),Color("#d100d1"),Color("#ff007f"),], foreName="fusion")
Gradient([Color("#ffff70"), Color("#ff1fe1"),Color("#33ffff")],foreName="sunset")
Gradient([Color("#2e7d32"), Color("#43a047"), Color("#26c6da"), Color("#1e88e5"), Color("#1565c0")], foreName="forest")
# new
Gradient([Color("#6a1b9a"), Color("#9c27b0"), Color("#ba68c8"), Color("#e1bee7"), Color("#edd7f3")], foreName="lavender")
Gradient([Color("#00eeb6"), Color("#00d9f5"), Color("#1c95ff"), Color("#7344ff"), Color("#b92eff")], foreName="aurora")
Gradient([Color("#ffecb3"), Color("#ffd54f"), Color("#ffb300"), Color("#ff8f00")], foreName="citrine")
Gradient([Color("#e6e200"), Color("#b3d400"), Color("#7bcb00"), Color("#4baf00")], foreName="peridot")
Gradient([Color("#ffc87c"), Color("#ffb347"), Color("#ffa07a"), Color("#6eb5ff"), Color("#4d8bff")], foreName="topaz")
Gradient([Color("#6a1b9a"), Color("#7e57c2"), Color("#8374d8"), Color("#8e99f3"), Color("#9388f1")], foreName="amethyst")
Gradient([Color("#0a5c36"), Color("#28a65c"), Color("#36c666"), Color("#33b162")], foreName="emerald")
Gradient([Color("#ff5c75"), Color("#ff2d4a"), Color("#d81d36"), Color("#9c131e")], foreName="ruby")
Gradient([Color("#1f2d6d"), Color("#263da2"), Color("#1e2592"), Color("#080f87")], foreName="sapphire")
Gradient([Color("#6dafd5"), Color("#86e5f8"), Color("#7cc3e9"), Color("#719fe3"), Color("#3768d5")], foreName="diamond")
Gradient([Color("#dbdbdb"), Color("#ffd6e7"), Color("#fdffbc"), Color("#bbf3be"), Color("#afc7ff"), Color("#c9ccfc")], foreName="opal")
Gradient([Color("#f2e2bb"), Color("#effff4"), Color("#ccffec"), Color("#91ffdc"), Color("#62dcd9"), Color("#52d0d8")], foreName="beach")"""

Gradient([
    Color(0.78, 1, 0.55, isHsl=True),
    Color(0.88, 1, 0.60, isHsl=True),
    Color(0.95, 1, 0.65, isHsl=True),
    Color(0.55, 1, 0.60, isHsl=True),
], foreName="neon", foreIsHsl=True)

_AlignArg: TypeAlias = Optional[Union[str, float]]
_valueDict = {'top':0, 'left': 0, 'center': 0.5, 'bottom':1, 'right': 1}

def _getAlignVal(a, b):
    val = fallback(a, b)
    return fallback(_valueDict.get(val,val),0.5)

class Align:
    def __init__(self, horizontal:_AlignArg=None, vertical:_AlignArg=None, relativeHorizontal:_AlignArg=None, padding:Optional[str]=None):
        self.horizontal = horizontal
        self.vertical = vertical
        self.relativeHorizontal = relativeHorizontal
        self.padding = padding
        
    def __call__(self, text:str, horizontal:_AlignArg=None, vertical:_AlignArg=None, relativeHorizontal:_AlignArg=None, padding:Optional[str]=False):
        horizontal = _getAlignVal(horizontal, self.horizontal)
        vertical = _getAlignVal(vertical, self.vertical)
        relativeHorizontal = _getAlignVal(relativeHorizontal, self.relativeHorizontal)
        
        padding = fallback(padding, self.padding, False)
        
        data = {"horizontalFactor":horizontal, "verticalFactor":vertical, "relativeFactor":relativeHorizontal, "padding":padding}
        
        text = _RichText(text)
        text._update(data)
        text._updateReference()
        
        return text

class _RichText:
    def __init__(self, source):
        if isinstance(source, _RichText):
            self.source = source.source
            self.data = source.data
            return
        
        self.source = source
        self.data = {}
        
    def _update(self, data):
        self.data.update(data)
    
    _clamp = lambda _, n, m, x: max(min(n, x), m)
    
    def _getPads(self, reference, horizontalFactor, verticalFactor, relativeFactor):
        width, height = shutil.get_terminal_size()
        
        horizontalFactor = horizontalFactor or 0 #not argument defaults cause None passed overweighs a default like 0
        verticalFactor = verticalFactor or 0
        relativeFactor = relativeFactor or 0
        
        relativeBase = len(max(reference,key=len))
        
        maxHorizontal = max(width - relativeBase, 0)
        maxVertical = max(height - len(reference), 0)
        
        horizontalPad = self._clamp(round(maxHorizontal * horizontalFactor),0,maxHorizontal)
        verticalPad = self._clamp(round(maxVertical * verticalFactor),0,maxVertical)
            
        relativePads = [int((relativeBase - len(line))*relativeFactor) for line in reference]
        
        return horizontalPad, verticalPad, relativePads
    
    def _updateReference(self):
        reference = removeAllEscapeCodes(self.source).splitlines()
        self.data["reference"] = reference
        return reference
    
    def _generateGradient(self, colors: ColorSequence, length):
        #this function additionally generates a last2first transition for offsetting. it is however not counted in length, so it shouldnt normally appear or impair anything.
        if not colors:
            return (), False
        
        gradients = len(colors.rgb) #number of transitions with last2first, ColorSequence.rgb and .hsl are equal in length
        base, extra = divmod(length, gradients-1) #minimum steps per gradient + remainder if (length/gradients) is not an int (no last2first)
        stepsPer = [base + (i < extra) for i in range(gradients-1)] #redistribute remaining steps evenly by giving only 1 to the first remainder-many gradients
        stepsPer.append(base) #last2first
        
        ndArrays = []

        if colors.asHsl:
            for pairIndex in range(gradients):
                h1,s1,l1 = colors.hsl[pairIndex % gradients]
                h2,s2,l2 = colors.hsl[(pairIndex+1) % gradients]
                
                delta = (h2 - h1) % 1.0
                if delta > 0.5:
                    delta -= 1.0
                
                t = numpy.linspace(0.0, 1.0, num=stepsPer[pairIndex], endpoint=False)
                hx = (h1 + delta * t) % 1.0
                sx = s1 + (s2 - s1) * t
                lx = l1 + (l2 - l1) * t

                ndArrays.append(numpy.array([Color.normalHelper(colour.hsl2rgb(c), False, False) for c in zip(hx, sx, lx)]))
        else:
            for pairIndex in range(gradients):
                ndArrays.append(numpy.linspace(
                    colors.rgb[pairIndex%gradients], colors.rgb[(pairIndex+1)%gradients], #gradients replaces len(colors.xxx) here
                    num=stepsPer[pairIndex],
                    endpoint=False,
                    dtype=int
                ))

        return numpy.concatenate(ndArrays), True
    
    def _generateCodeString(self, length):
        string = self.data.get("codeString", [])
        lengths = self.data.get("lastLengths")
        if string and (lengths[0] == length):
            return string, lengths[1]
        
        foreColors = self.data.get("foreColors") # oh noo looking up the colors a second time
        foreGradient, foreExists = self._generateGradient(foreColors,length)
        
        backColors = self.data.get("backColors")
        backGradient, backExists = self._generateGradient(backColors,length)

        if foreExists or backExists:
            rLength = max(len(foreGradient), len(backGradient)) # if you get rLength = 0 you are a wizard
        else:
            raise ValueError("generateColorString() was not given any gradients")
        print("\n", rLength, "RLEN generateCodeString", foreGradient, backGradient, foreColors, backColors, length)
        
        for i in range(rLength):
            codes = []
            if foreExists:
                codes.append(_getCode(3, foreGradient[i]))
            if backExists:
                codes.append(_getCode(4, backGradient[i]))
            
            string.append(f"\033[{';'.join(codes)}m" if codes else "")
        
        self.data["codeString"] = string
        self.data["lastLengths"] = (length, rLength)
        return string, rLength
    
    def _finalizeGradient(self, text, length, vertical, resolution, terminal, pads, offset):
        text = text.splitlines()
        
        codeString, rLength = self._generateCodeString(length)
        
        finalText = []
        
        horizontalPad, verticalPad, relativePads = pads
        if not terminal:
            horizontalPad = verticalPad = 0
            
        for lineIndex, line in enumerate(text):
            colorNext = True
            
            for charIndex, char in enumerate(line):
                if (charIndex - offset)%resolution == 0 and not vertical:
                    colorNext = True
                    
                if not char.isspace() and colorNext: #if is not space, resolutionth char has been seen and its color has not yet been applied, apply it now and reset colorNext
                    colorNext = False
                    if vertical: # if terminal is false, the pad variables make no difference
                        index = (lineIndex+verticalPad)//resolution
                        #print(True, lineIndex, verticalPad, index, len(codeString))
                    else:
                        index = (charIndex+horizontalPad+relativePads[lineIndex])//resolution
                        #print(False, charIndex, horizontalPad, relativePads[lineIndex], index, len(codeString))
                    
                    finalText.append(f"{codeString[(index+offset)%rLength]}{char}")
                else:
                    finalText.append(char)
            finalText.append("\n")
        finalText.pop()
        
        finalText.append("\033[0m")
        return "".join(finalText)
    
    def _finalizeAlign(self, text, padding, pads):
        text = text.splitlines()
        
        horizontalPad, verticalPad, relativePads = pads
        
        finalText = []
        
        if padding is not None:
            finalText = ["\n"] * verticalPad
            
            for index, line in enumerate(text):
                relativePad = relativePads[index]
                finalText.extend([padding] * (horizontalPad + relativePad))
                finalText.extend([line, "\n"])
            finalText.pop()
        else:
            finalText = ["\0337"] #save cursor pos
            for index, line in enumerate(text):
                relativePad = relativePads[index]
                escape = f"\033[{verticalPad+index+1};{horizontalPad+relativePad+1}H" #+1 because terminal cells start at (1,1) not (0,0)
                finalText.append(f"{escape}{line}")
            finalText.append("\0338") #load cursor pos
            
        return "".join(finalText)
    
    def finalize(self, offset):
        final = self.source
        
        reference, horizontalFactor, verticalFactor, relativeFactor, padding = [self.data.get(key) for key in ["reference", "horizontalFactor", "verticalFactor", "relativeFactor", "padding"]]
        pads = self._getPads(reference, horizontalFactor, verticalFactor, relativeFactor)
        
        foreColors, backColors, length, vertical, resolution, terminal = [self.data.get(key) for key in ["foreColors", "backColors", "length", "vertical", "resolution", "terminal"]]
        if foreColors or backColors:
            final = self._finalizeGradient(final, length, vertical, resolution, terminal, pads, offset)
        
        if all(x is not None for x in [horizontalFactor,verticalFactor,relativeFactor]): #if padding doesnt exist, resorts to ansi
            final = self._finalizeAlign(final, padding, pads)
        
        return final
    
    @property
    def final(self):
        return self.finalize(0)
    
    def __call__(self, offset):
        return self.finalize(offset)
    
    def __getattr__(self, attr): #py cant call str functions (like str.split()) on this class so it will resort to getattr(this, 'split')
        if hasattr(str, attr): #this line is because else doing sh like self.horizontal calls finalizeAlign(), where self.horizontal itself is
            return getattr(self.final, attr) #this redirects the method to the finalized version of the text, which is a str and has the method
    
    def __str__(self):
        return self.final
    
    def __repr__(self):
        return self.source

# MISC #############################################################################################################################################################################
print("Exiting")
#exit()

"""class Empty: #especially used in RichText.generateCodeMatrix. check there to understand why #not anymore lololo
    def __getitem__(self, *_):
        return self
    def __iter__(self): #'for i in Empty' == 'for i in ()', an empty iterable
        return iter(())
    def __bool__(self): #this makes the whole class falsy
        return False
    def __repr__(self):
        return "Empty"
    def __add__(self, other):
        return other
    def __radd__(self,  other):
        return other
Empty = Empty()"""

text = "yo cuz you wanna kiss? sure gng come over here bro\nbro damn you black as hell dont talk to me\nloser lamo wanna be like oh\ntotally my digga\none last time i need to be the one that rapes you home gng twin yo"
text2 = """     ||
     ||
    |==|
   |####|
   |####|
   |####|
    |==|
     ||
     ||
     ||
     ||
     ||
    /||\\
   /_||_\\"""
text3 = """██╗   ██╗ ██████╗ ██╗   ██╗██████╗     ██████╗  █████╗ ██████╗ 
╚██╗ ██╔╝██╔═══██╗██║   ██║██╔══██╗    ██╔══██╗██╔══██╗██╔══██╗
 ╚████╔╝ ██║   ██║██║   ██║██████╔╝    ██║  ██║███████║██║  ██║
  ╚██╔╝  ██║   ██║██║   ██║██╔══██╗    ██║  ██║██╔══██║██║  ██║
   ██║   ╚██████╔╝╚██████╔╝██║  ██║    ██████╔╝██║  ██║██████╔╝
   ╚═╝    ╚═════╝  ╚═════╝ ╚═╝  ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚═════╝"""
text4 = """▄▄▄   ▌ ▐·▄▄▄ .▄▄▄  
▀▄ █·▪█·█▌▀▄.▀·▀▄ █·
▐▀▀▄ ▐█▐█•▐▀▀▪▄▐▀▀▄ 
▐█•█▌ ███ ▐█▄▄▌▐█•█▌
.▀  ▀. ▀   ▀▀▀ .▀  ▀"""
text5 = """.▄▄ · ▄• ▄▌ ▄▄▄·▄▄▄ .▄▄▄      ▄▄▄▄▄▄▄▌ ▐ ▄▌▪  ▄▄▄▄▄▄▄▄▄▄▄▄▄ .▄▄▄       ▄▄ • ▄▄▄   ▄▄▄·  ▐ ▄ ·▄▄▄▄  • ▌ ▄ ·.  ▄▄▄· 
▐█ ▀. █▪██▌▐█ ▄█▀▄.▀·▀▄ █·    •██  ██· █▌▐███ •██  •██  ▀▄.▀·▀▄ █·    ▐█ ▀ ▪▀▄ █·▐█ ▀█ •█▌▐███▪ ██ ·██ ▐███▪▐█ ▀█ 
▄▀▀▀█▄█▌▐█▌ ██▀·▐▀▀▪▄▐▀▀▄      ▐█.▪██▪▐█▐▐▌▐█· ▐█.▪ ▐█.▪▐▀▀▪▄▐▀▀▄     ▄█ ▀█▄▐▀▀▄ ▄█▀▀█ ▐█▐▐▌▐█· ▐█▌▐█ ▌▐▌▐█·▄█▀▀█ 
▐█▄▪▐█▐█▄█▌▐█▪·•▐█▄▄▌▐█•█▌     ▐█▌·▐█▌██▐█▌▐█▌ ▐█▌· ▐█▌·▐█▄▄▌▐█•█▌    ▐█▄▪▐█▐█•█▌▐█ ▪▐▌██▐█▌██. ██ ██ ██▌▐█▌▐█ ▪▐▌
 ▀▀▀▀  ▀▀▀ .▀    ▀▀▀ .▀  ▀     ▀▀▀  ▀▀▀▀ ▀▪▀▀▀ ▀▀▀  ▀▀▀  ▀▀▀ .▀  ▀    ·▀▀▀▀ .▀  ▀ ▀  ▀ ▀▀ █▪▀▀▀▀▀• ▀▀  █▪▀▀▀ ▀  ▀ """
text6 = """\\ `/ |
 \\__`!
 / ,' `-.__________________
'-'\\_____                LI`-.
   <____()-=O=O=O=O=O=[]====--)
     `.___ ,-----,_______...-'
          /    .'
         /   .'
        /  .'         
        `-'"""
text7 = """            ▓       
     ▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓      
   ▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓       
  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓        
 ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓       
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒      
      ░▓▓░▓▓▓▓▓▓▓▓▓▓▓▓▓▓      
        ▓▓  ▓▓▓▓▓ ▓▓▓▓▓▓▓     
                   ▓▓▓▓▓▓░    
                     ▓▓▓▓▓    
                      ▓▓▓▓    
                       ▓▓▓    
                      ░▓▓▓▓▓  
                     ▓▓▓▓▓▓▓▓▓
                     ▓  ░▓▓░▓▓"""
text8 = "▪ ▪ ▪ \n ▪ ▪ ▪\n▪ ▪ ▪ \n ▪ ▪ ▪"
text9 = "██████\n██████\n██████\n██████"
textA = """                                        

    made by rver made by rver made by rver  
    rver                              rver  
    rver    ▄▄▄   ▌ ▐·▄▄▄ .▄▄▄        rver  
    rver    ▀▄ █·▪█·█▌▀▄.▀·▀▄ █·      rver  
    rver    ▐▀▀▄ ▐█▐█•▐▀▀▪▄▐▀▀▄       rver  
    rver    ▐█•█▌ ███ ▐█▄▄▌▐█•█▌      rver  
    rver    .▀  ▀. ▀   ▀▀▀ .▀  ▀      rver  
    rver                              rver  
    made by rver made by rver made by rver  
                                            """
textB = """  made by rver made by rver made  
                               
      ▄▄▄   ▌ ▐·▄▄▄ .▄▄▄         
      ▀▄ █·▪█·█▌▀▄.▀·▀▄ █·       
      ▐▀▀▄ ▐█▐█•▐▀▀▪▄▐▀▀▄         
      ▐█•█▌ ███ ▐█▄▄▌▐█•█▌       
      .▀  ▀. ▀   ▀▀▀ .▀  ▀       
                              
  made by rver made by rver made  """
resolution = 1


"""# Main test loop
for horizontal in align_args:
    for vertical_align in align_args:
        # Gradient step
        output = g(text, None, None, True, resolution, True, True)
        # Align step (note: relativeHorizontal = horizontal)
        output = a(output, horizontal, vertical_align, horizontal)
        # Print or save results as needed
        #print(f"\n--- h={horizontal}, v_align={vertical_align} ---")
        input(output)
        os.system("cls")"""

import os, time, math, shutil, random

#ghi = "\033[38;5;240mmade by rver    "*800

# Lissajous movement
def lissajous(t, a=3.14, b=2.18, delta=math.pi/2):
    h = 0.5 + 0.5 * math.sin(a * t + delta)
    v = 0.5 + 0.5 * math.sin(b * t)
    return h, v
global t
t = 0
# Benchmark function
def benchmark(text1, text2, gradient_obj, align_obj, colors=None, resolution=1, terminal=True, vertical=False, duration=1):
    global t
    one = gradient_obj(text1, colors, None, vertical, resolution, terminal)
    two = gradient_obj(text2, colors, None, vertical, resolution, terminal)
    frames = 0

    start = time.perf_counter()
    width, height = shutil.get_terminal_size()

    while time.perf_counter() - start < duration:
        t += 0.0007#0.0007
        h1, v1 = lissajous(t)
        h2, v2 = lissajous(t + 1.0)  # phase shift for second pattern
        
        one_aligned = align_obj(one, h1, v1)
        two_aligned = align_obj(two, h2, v2)

        # Print patterns below
        print(f"{one_aligned}{two_aligned}", end="", flush=True)
        #str(one_aligned);str(two_aligned) # print to nul
        frames += 1
        
        print(f"\033[HResolution: {resolution} | Terminal: {('False', 'True ')[terminal]} | Vertical: {('False', 'True ')[vertical]} | Frames: {frames:06}", end="")

    return frames // duration

# Example patterns: you can add or replace these
patterns = [
    (
        """████████
████████
████████
████████""",
        """▪ ▪ ▪ ▪ 
 ▪ ▪ ▪ ▪
▪ ▪ ▪ ▪ 
 ▪ ▪ ▪ ▪"""
    ),
    (
        """████████████████
████████████████
████████████████
████████████████
████████████████
████████████████
████████████████
████████████████""",
        """▪ ▪ ▪ ▪ ▪ ▪ ▪ ▪ 
 ▪ ▪ ▪ ▪ ▪ ▪ ▪ ▪
▪ ▪ ▪ ▪ ▪ ▪ ▪ ▪ 
 ▪ ▪ ▪ ▪ ▪ ▪ ▪ ▪
▪ ▪ ▪ ▪ ▪ ▪ ▪ ▪ 
 ▪ ▪ ▪ ▪ ▪ ▪ ▪ ▪
▪ ▪ ▪ ▪ ▪ ▪ ▪ ▪ 
 ▪ ▪ ▪ ▪ ▪ ▪ ▪ ▪"""
    ),
    (
        """████████████████████
████████████████████
████████████████████
████████████████████
████████████████████
████████████████████
████████████████████
████████████████████
████████████████████
████████████████████""",
        """▪ ▪ ▪ ▪ ▪ ▪ ▪ ▪ ▪ ▪ 
 ▪ ▪ ▪ ▪ ▪ ▪ ▪ ▪ ▪ ▪
▪ ▪ ▪ ▪ ▪ ▪ ▪ ▪ ▪ ▪ 
 ▪ ▪ ▪ ▪ ▪ ▪ ▪ ▪ ▪ ▪
▪ ▪ ▪ ▪ ▪ ▪ ▪ ▪ ▪ ▪ 
 ▪ ▪ ▪ ▪ ▪ ▪ ▪ ▪ ▪ ▪
▪ ▪ ▪ ▪ ▪ ▪ ▪ ▪ ▪ ▪ 
 ▪ ▪ ▪ ▪ ▪ ▪ ▪ ▪ ▪ ▪
▪ ▪ ▪ ▪ ▪ ▪ ▪ ▪ ▪ ▪ 
 ▪ ▪ ▪ ▪ ▪ ▪ ▪ ▪ ▪ ▪"""
    )
]

def benchmarkTest():
    input("START")
    
    #benchmark(textB, text6, g, a, resolution=4, duration=60) #flex

    # Run all benchmarks
    info = []
    width, height = shutil.get_terminal_size()

    for resolution in [1, 3, 8]:
        for terminal in [True, False]:
            for vertical in [False, True]:
                fps = benchmark(textB, textB, g, a, resolution=resolution, terminal=terminal, vertical=vertical)
                info.append(
                    f"res={resolution} terminal={terminal} vertical={vertical} size=({width},{height}) size=? frames={fps}"
                )

    # Clear screen and print summary
    print("\033[0m")
    os.system("cls")
    for line in info:
        print(line)

# Initialize your objects
#g = Gradient(name=input("name: "))
a = Align()

def inplaceTest():
    c = g(text5)
    #print(c, end="", flush=True)
    d = a(c)
    b = 0
    while True:
        print(d(b), end="", flush=True)
        b+=1
        time.sleep(0.01)

while True:
    g = Gradient(backName=input("name: "), lengthFactor=1.0)
    inplaceTest()
    benchmarkTest()