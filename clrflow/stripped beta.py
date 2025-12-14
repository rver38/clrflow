#made with support from my dearest friend mejta
#gng twin cuh

import os, colour, numpy, math, shutil, re
from typing import Sequence, Optional, Union, TypeAlias, Tuple

os.system("")

# UNIVERSAL ########################################################################################################################################################################

def fallback(priority, fallback, condition=None):
    return priority if priority != condition else fallback

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
    #print("LINE 45",color)
    if tuple(color)==(0,0,0):
        return f"{prefix}9"
    elif code is not None:
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
        #if normal is none, flip, else make it whatever normal is, in the provided color format. supports any amount of rgb values
        
        if not isinstance(color[0], (int, float)):
            raise ValueError("color must be a Sequence of numbers")
        
        current = isinstance(color[0], float) and max(color) <= 1
        target = fallback(normal, not current)
        
        if current == target:
            return color
        
        if isHsl:
            if len(color)!=3:
                raise ValueError("hsl color must be a Sequence of exactly 3 numbers")
            
            hMultiplier = 1/360 if target else 360
            slMultiplier = 0.01 if target else 100
            h, s, l = color
            return (h*hMultiplier, s*slMultiplier, l*slMultiplier)
        else:
            rgbMultiplier = 1/255 if target else 255
            return tuple(int(val*rgbMultiplier) for val in color)
    
    def __init__(self, #these annotations are SO long
        x: Union[int, float, str, Tuple[int, int, int], Tuple[float, float, float]],
        y: Optional[Union[int, float]] = None, z: Optional[Union[int, float]] = None, background: bool=False, isHsl: bool=None):
        self.background = background
        
        isHsl = fallback(isHsl, Color.assumeHsl)
        
        colorTable = {
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
        if isinstance(x, str):
            x = colorTable.get(x.lower(), x)
            xyz = colour.hex2rgb(x)
            isHsl = False
        elif isinstance(x, Sequence):
            if len(x) != 3:
                raise ValueError("if x is a Sequence, it must consist of 3 numbers")
            xyz = x
        elif all(isinstance(val, (int, float)) for val in (x, y, z)):
            xyz = (x, y, z)
        else:
            raise ValueError("x must be a str, number, or a Sequence of 3 numbers")
        
        xyz = self.normalHelper(xyz, isHsl, True)
        self.rgb = self.normalHelper(colour.hsl2rgb(xyz) if isHsl else xyz, False, False)
        self.hsl = xyz if isHsl else colour.rgb2hsl(xyz)
            
    def ansi(self, background:bool=None, color=None):
        return f"\033[{_getCode(4 if fallback(background, self.background) else 3, fallback(color, self.rgb))}m"
    
    def __str__(self):
        return self.ansi()
    def __add__(self, other):
        return self.ansi()+str(other)
    def __radd__(self, other):
        return str(other)+self.ansi()
    
    def __call__(self, as_dict=False, as_hex=False, rgb_tuple=False, hsl_tuple=False, inverted=False, complementary=False):
        r, g, b = self.rgb
        h, s, l = self.hsl
        if inverted:
            r, g, b = (255-r, 255-g, 255-b)
            if as_dict or hsl_tuple or complementary:
                h, s, l = colour.rgb2hsl(self.normalHelper((r,g,b), False, True))
        if complementary:
            h, s, l = ((h+0.5)%1, s, 1-l)
            if as_dict or as_hex or rgb_tuple or inverted:
                r, g, b = colour.hsl2rgb((h,s,l), True, False)
        
        if rgb_tuple:
            return (r, g, b)
        if hsl_tuple:
            return (h, s, l)
        if as_dict:
            return {"r":r, "g":g, "b":b, "h":h, "s":s, "l":l, "rgb":(r,g,b), "hsl":(h,s,l)}
        if as_hex:
            return '#%02x%02x%02x' % (r, g, b)
        return self.ansi(color=(r, g, b))

# sigma ###############################################################################################################################################################################
_savedGradients = {}

_ColorSequenceType: TypeAlias = Optional[Sequence[Color]|bool]
_LenFactorType: TypeAlias = Optional[float|int]

class ColorSequence:
    def __init__(self, colors: Sequence, hsl:bool=False, inverted:bool=False, reverse:bool=False, normalize:bool=True):
        if not colors:
            raise ValueError("color sequence is empty")
        if isinstance(colors, ColorSequence):
            self.colors = colors.colors
        elif normalize:
            self.colors = self.normalizeColors(colors, hsl, inverted, reverse)
        else:
            self.colors = colors
    
    def normalizeColors(self, colors:Sequence=None, hsl:bool=False, inverted:bool=False, reverse:bool=False,):
        colors = fallback(colors, getattr(self, "colors", None))
        if isinstance(colors, Sequence):
            i = reversed(colors) if reverse else colors
            return tuple(
                color(rgb_tuple=not hsl, hsl_tuple=hsl, inverted=(inverted and not hsl), complementary=(inverted and hsl))
                if isinstance(color, Color) else color
                for color in i
            )
        return ()
    
    def __bool__(self):
        return bool(self.colors)

class Gradient:
    def __init__(self, foregroundColors:_ColorSequenceType=None, backgroundColors:_ColorSequenceType=None, vertical:Optional[bool]=None, resolution:Optional[int]=None, terminal:Optional[bool]=None, name:Optional[str]=None, reverse:Optional[bool]=None, lengthFactor:_LenFactorType=None):
        if name:
            if (settings := _savedGradients.get(name)):
                foregroundColors = fallback(foregroundColors, settings[0])
                backgroundColors = fallback(backgroundColors, settings[1])
            _savedGradients[name] = (foregroundColors, backgroundColors)
        
        self.foreColors = fallback(foregroundColors, [(0,0,0),(0,0,0)])
        self.backColors = fallback(backgroundColors, [(0,0,0),(0,0,0)])
        self.vertical = vertical
        self.resolution = resolution
        self.terminal = terminal
        self.lenFactor = lengthFactor
        self.reverse = reverse
    
    def _match(self, seq, other):
        if isinstance(seq, (ColorSequence, Sequence)):
            return seq
        elif isinstance(seq, bool):
            if isinstance(other, (ColorSequence, Sequence)):
                return ColorSequence(other, inverted=True)
        raise ValueError("atleast either seq or other must be a Sequence of color values")
        
        """if not isinstance(seq, bool):
            
        
        if isinstance(seq,bool):
            return ColorSequence(other).normalizeColors(inverted=True)
            raise ValueError(f"provide atleast one Sequence of color-like items (seq={seq}, other={other}")
        return seq"""
    
    def __call__(self, text, foregroundColors:_ColorSequenceType=None, backgroundColors:_ColorSequenceType=None, vertical:Optional[bool]=None, resolution:Optional[int]=None, terminal:Optional[bool]=None, hsl:Optional[bool]=False, reverse:Optional[bool]=False, lengthFactor:_LenFactorType=None):
        vertical = fallback(vertical,self.vertical) or False
        resolution = fallback(resolution,self.resolution) or 1
        terminal = fallback(terminal, self.terminal) or False
        reverse = fallback(reverse,self.reverse) or False
        lenFactor = fallback(lengthFactor, self.lenFactor) or 1.0
        
        fore = fallback(foregroundColors,self.foreColors)
        back = fallback(backgroundColors,self.backColors)
        #print(fore, back, "# LINE 293")
        
        if not (fore or back):
            raise ValueError(f"provide atleast one Sequence of color-like items (fore={fore}, back={back})")
        
        if not isinstance(text, _RichText):
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
            data["foreColors"] = ColorSequence(self._match(fore, back), hsl).colors
        if back:
            data["backColors"] = ColorSequence(self._match(back, fore), hsl).colors
        
        text._update(data)
        return text
    
    def listSaved(self):
        return _savedGradients.keys()

#remade from earlier clrflow
Gradient([Color("#ff4b4b"), Color("#ffae42"), Color("#ffee55"), Color("#6bff5f"), Color("#4dd8ff"), Color("#5b4dff"), Color("#c64dff")], name="rainbow")
Gradient([Color("#ff0000"), Color("#ff7b00"), Color("#ffd166")], name="fire")
Gradient([Color("#001f54"), Color("#005792"), Color("#00bbf0"), Color("#00f5d4")], name="ocean")
Gradient([Color("#2d00f7"), Color("#7b2ff7"),Color("#d100d1"),Color("#ff007f"),], name="fusion")
Gradient([Color("#ffff70"), Color("#ff1fe1"),Color("#33ffff")],name="sunset")
Gradient([Color("#2e7d32"), Color("#43a047"), Color("#26c6da"), Color("#1e88e5"), Color("#1565c0")], name="forest")
# new
Gradient([Color("#6a1b9a"), Color("#9c27b0"), Color("#ba68c8"), Color("#e1bee7"), Color("#edd7f3")], name="lavender")
Gradient([Color("#00eeb6"), Color("#00d9f5"), Color("#1c95ff"), Color("#7344ff"), Color("#b92eff")], name="aurora")
Gradient([Color("#ffecb3"), Color("#ffd54f"), Color("#ffb300"), Color("#ff8f00")], name="citrine")
Gradient([Color("#e6e200"), Color("#b3d400"), Color("#7bcb00"), Color("#4baf00")], name="peridot")
Gradient([Color("#ffc87c"), Color("#ffb347"), Color("#ffa07a"), Color("#6eb5ff"), Color("#4d8bff")], name="topaz")
Gradient([Color("#6a1b9a"), Color("#7e57c2"), Color("#8374d8"), Color("#8e99f3"), Color("#9388f1")], name="amethyst")
Gradient([Color("#0a5c36"), Color("#28a65c"), Color("#36c666"), Color("#33b162")], name="emerald")
Gradient([Color("#ff5c75"), Color("#ff2d4a"), Color("#d81d36"), Color("#9c131e")], name="ruby")
Gradient([Color("#1f2d6d"), Color("#263da2"), Color("#1e2592"), Color("#080f87")], name="sapphire")
Gradient([Color("#6dafd5"), Color("#86e5f8"), Color("#7cc3e9"), Color("#719fe3"), Color("#3768d5")], name="diamond")
Gradient([Color("#dbdbdb"), Color("#ffd6e7"), Color("#fdffbc"), Color("#bbf3be"), Color("#afc7ff"), Color("#c9ccfc")], name="opal")
Gradient([Color("#f2e2bb"), Color("#effff4"), Color("#ccffec"), Color("#91ffdc"), Color("#62dcd9"), Color("#52d0d8")], name="beach")

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
        
        if not isinstance(text, _RichText):
            text = _RichText(text)
        text._update(data)
        text._updateReference()
        
        return text

Gradient([
    Color(255, 0, 0),     # Red
    Color(0, 255, 0),     # Green
    Color(0, 0, 255)     # Blue
], name="test")

class _RichText:
    def __init__(self, source):
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
    
    def _generateGradient(self, colors, length, isHsl=False):
        #this function additionally generates a last2first transition for offsetting. it is however not counted in length, so it shouldnt normally appear or impair anything.
        if not colors:
            return (), False
        
        gradients = len(colors) #number of transitions with last2first
        base, extra = divmod(length, gradients-1) #minimum steps per gradient + remainder if (length/gradients) is not an int (no last2first)
        stepsPer = [base + (i < extra) for i in range(gradients-1)] #redistribute remaining steps evenly by giving only 1 to the first remainder-many gradients
        stepsPer.append(base) #last2first
        
        ndArrays = []

        if isHsl:
            ...
        else:
            for pairIndex in range(gradients):
                ndArrays.append(numpy.linspace(
                    colors[pairIndex%len(colors)], colors[(pairIndex+1)%len(colors)],
                    num=stepsPer[pairIndex],
                    endpoint=False,
                    dtype=int
                ))

        
        return numpy.concatenate(ndArrays), True
    
    def _generateGradienthsl_(self, colors, length):
        """
        Generate a smooth gradient using HSL interpolation internally.
        Accepts and returns colors as RGB tuples (0-255).
        Adds a ping-pong last-to-first segment.
        """
        if not colors:
            return (), False

        n_stops = len(colors)
        n_segments = n_stops - 1  # forward segments only

        # Compute steps per segment
        base, extra = divmod(length, n_segments)
        steps_per_segment = [base + (i < extra) for i in range(n_segments)]
        steps_per_segment.append(steps_per_segment[-1] * 2)  # last-to-first doubled

        # Convert RGB (0-255) -> HSL (0-1)
        hsl_colors = [colorsys.rgb_to_hls(r/255, g/255, b/255) for r, g, b in colors]

        # Build gradient
        gradient_arrays = []
        for i in range(n_stops):
            start_h, start_l, start_s = hsl_colors[i % n_stops]
            end_h, end_l, end_s = hsl_colors[(i+1) % n_stops]
            steps = steps_per_segment[i]

            # Handle hue wrapping
            delta_h = end_h - start_h
            if delta_h > 0.5:
                delta_h -= 1
            elif delta_h < -0.5:
                delta_h += 1

            # Interpolate
            gradient_segment = []
            for step in range(steps):
                t = step / steps
                h = (start_h + delta_h * t) % 1.0
                l = start_l + (end_l - start_l) * t
                s = start_s + (end_s - start_s) * t
                r, g, b = colorsys.hls_to_rgb(h, l, s)
                gradient_segment.append((int(r*255), int(g*255), int(b*255)))

            gradient_arrays.append(numpy.array(gradient_segment, dtype=int))

        return numpy.concatenate(gradient_arrays), True
    
    def _generateCodeString(self, length):
        string = self.data.get("codeString", [])
        lengths = self.data.get("lastLengths")
        if string and (lengths[0] == length):
            return string, lengths[1]
        
        foreColors = self.data.get("foreColors")
        foreGradient, foreExists = self._generateGradient(foreColors,length)
        
        backColors = self.data.get("backColors")
        backGradient, backExists = self._generateGradient(backColors,length)
        
        #print("LINE 328 COLORMATRIX", width, height, len(matrix), len(matrix[0]))

        if foreExists:
            rLength = len(foreGradient)
        elif backExists:
            rLength = len(backGradient)
        else:
            raise ValueError("generateColorString() could not establish gradients")
        print("\n", rLength, "RLEN", foreGradient, backGradient, foreColors, backColors, length)
        
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
            horizontalPad, verticalPad, = 0, 0
            
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

#inplaceTest()
while True:
    g = Gradient(name=input("name: "), lengthFactor=1.0, backgroundColors=True)
    benchmarkTest()