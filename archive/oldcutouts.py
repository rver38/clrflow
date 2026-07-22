def _generateColorString(self, dimensions, vertical): #GARBAGE###########################################################################################################
        width, height = dimensions #check Gradient
        
        string = []
        
        length = height if vertical else width
        
        foreColors = self.data.get("foreColors")
        foreGradient, fore = self._generateGradient(foreColors,length)
        
        backColors = self.data.get("backColors")
        backGradient, back = self._generateGradient(backColors,length)
        
        ##print("LINE 328 COLORMATRIX", width, height, len(matrix), len(matrix[0]))
        
        if fore:
            length = len(fore)
        elif back:
            length = len(back)
        else:
            raise ValueError("generateColorString() could not establish gradients")
        
        for i in range(length):
            foreColor = foreGradient[i] if fore else None
            backColor = backGradient[i] if back else None
            string.append((foreColor, backColor))
        return string, fore, back
    
    def _generateCodeMatrix(self, dimensions, vertical): #GARBAGE###########################################################################################################
        colorMatrix = self._generateColorString(dimensions, vertical)
        
        codeMatrix = []
        width, height = dimensions()
        
        for y in colorMatrix: #replaced math.ceil(dimension/resolution)
            row = []
            for fore, back in y:
                codes = []
                
                if fore.any():
                    codes.append(_getCode(3, fore))
                if back.any():
                    codes.append(_getCode(4, back))
                
                ansi = f"\033[{';'.join(codes)}m" if codes else ""
                row.append(ansi)
            codeMatrix.append(row)
        self.data["codeMatrix"] = codeMatrix
        self.data["lastDimensions"] = (width, height)
        return codeMatrix
    
    def _generateCodeList(self, length, vertical, resolution, terminal): #GARBAGE###########################################################################################################
        codeList = self.data.get("codeList")
        if (self.data["lastLength"] != length) or (codeList is None):
            foreGradient, useFore = self._generateGradient(self.data.get("foreColors"), length)
            backGradient, useBack = self._generateGradient(self.data.get("backColors"), length)
            
            codeList = []
            for i in range(length):
                codes = []
                if useFore:
                    codes.append(f"38;{self._getCode(foreGradient[i])}")
                if useBack:
                    codes.append(f"48;{self._getCode(backGradient[i])}")
                codeList.append(f"\033[{';'.join(codes)}m")
            self.data["codeList"] = codeList
            self.data["lastLength"] = length
        
        return codeList  
    
    def _finalizeGradientold(self, text, length, vertical, resolution, terminal, lastDimensions, pads): #GARBAGE###########################################################################################################
        text = text.splitlines()
        
        codeString = self._generateCodeString(length, vertical)
        
        finalText = []
        
        horizontalPad, verticalPad, relativePads = pads
        if not terminal:
            horizontalPad, verticalPad, = 0, 0
        
        for lineIndex, line in enumerate(text):
            colorNext = True
            
            for charIndex, char in enumerate(line):
                if charIndex%resolution==0:
                    colorNext = True
                
                if not char.isspace() and colorNext: #if is not space, resolutionth char has been seen and its color has not yet been applied, apply it now and reset colorNext
                    colorNext = False
                    row = (lineIndex+verticalPad)//resolution
                    column = (charIndex+horizontalPad+relativePads[lineIndex])//resolution
                    
                    index = (row*length) + column
                    
                    finalText.append(f"{codeString[0]}{char}") # if terminal is false, the pad variables make no difference
                else:
                    finalText.append(char)
            finalText.append("\n")
        finalText.pop()
        finalText.append("\033[0m")
        
        return "".join(finalText)
    
"""ColorNew
xyz = (x, y, z)
if isinstance(x, str):
    rgb = colour.hex2rgb(x)
    self.rgb = self.normalHelper(rgb, normal=False)
    self.hsl = colour.rgb2hsl(rgb)
elif isinstance(x, Sequence):
    if isinstance(x[0], float):
        self.hsl = x
        self.rgb = self.normalHelper(x, normal=False)
    elif isinstance(x[0], int):
        self.rgb = x
        self.hsl = colour.rgb2hsl(x)
    else:
        raise ValueError("Only int and float objects are supported")
elif isinstance(x, float):
    self.hsl = xyz
    self.rgb = self.normalHelper(colour.hsl2rgb(xyz), normal=False)
elif isinstance(x, int):
    self.rgb = xyz
    self.hsl = colour.rgb2hsl(self.normalHelper(xyz, normal=True))
else:
    raise ValueError("x may only be a str, int, float, or a sequence of ints/floats")"""
    
class Color:
    def __init__(self,color:Union[tuple[int,int,int],str,int],g_or_s:Optional[int]=None,b_or_l:Optional[int]=None,isHsl:bool=False,background:bool=False):
        """color object, supports rgb, hex and hsl, and includes some predefined colors.
        
        can be added together with strings to color them, can return 

        arguments:
        - color (tuple[int,int,int]|str|int): a tuple of rgb/hsl values, a hex color value or color name as a string, or the red/hue value of an rgb/hsl color
        - g_or_s (int, optional): green/saturation value of an rgb/hsl trio. defaults to None.
        - b_or_l (int, optional): blue/lightness value of an rgb/hsl trio. defaults to None.
        - isHsl (bool, optional): if true, treats given color values as hsl values. defaults to False.
        - background (bool, optional): if this object is used to color a string, this is used to set whether it applies to the background. defaults to False.
        """
        self.background = background
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
        
        match color:
            case str():
                color = colorTable.get(color,color)
                self.color = tuple(round(value*255) for value in colour.hex2rgb(color))
            case color if isinstance(color, Sequence): #dont look at this
                if isHsl:
                    temp_color = colour.hsl2rgb((color[0]/360,color[1]/100,color[2]/100))
                    self.color = tuple(round(value*255) for value in temp_color)
                else:
                    self.color = tuple(color)
            case _:
                if isHsl:
                    temp_color = colour.hsl2rgb((color/360,g_or_s/100,b_or_l/100))
                    self.color = tuple(round(value*255) for value in temp_color)
                else:
                    self.color = (color,g_or_s,b_or_l)
    
    @property
    def ansi(self):
        return f"\033[{_getCode(4 if self.background else 3, self.color)}m"
    
    def __call__(self, as_dict=False, as_hex=False, as_tuple=False, inverted=False) -> str|tuple|dict:
        if as_tuple:
            if inverted:
                r, g, b = self.color
                return (255-r, 255-g, 255-b)
            return self.color
        if as_dict:
            return {'r': self.color[0], 'g': self.color[1], 'b': self.color[2]}
        if as_hex:
            return '#%02x%02x%02x' % self.color
        return self.ansi
    
    def __str__(self):
        return self.ansi
     
    def __add__(self,other):
        return self.ansi+str(other)
    def __radd__(self,other):
        return str(other)+self.ansi