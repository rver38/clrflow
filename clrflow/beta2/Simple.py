#give me some peace
from .Universal import fallback
from collections.abc import Sequence
import colour

resetAll = "\033[0m"

colorTable = { # https://www.w3schools.com/colors/colors_names.asp / https://www.w3.org/TR/css-color-4/#named-colors
    "aliceblue": "#F0F8FF",
    "antiquewhite": "#FAEBD7",
    "aqua": "#00FFFF",
    "aquamarine": "#7FFFD4",
    "azure": "#F0FFFF",
    "beige": "#F5F5DC",
    "bisque": "#FFE4C4",
    "black": "#000000",
    "blanchedalmond": "#FFEBCD",
    "blue": "#0000FF",
    "blueviolet": "#8A2BE2",
    "brown": "#A52A2A",
    "burlywood": "#DEB887",
    "cadetblue": "#5F9EA0",
    "chartreuse": "#7FFF00",
    "chocolate": "#D2691E",
    "coral": "#FF7F50",
    "cornflowerblue": "#6495ED",
    "cornsilk": "#FFF8DC",
    "crimson": "#DC143C",
    "cyan": "#00FFFF",
    "darkblue": "#00008B",
    "darkcyan": "#008B8B",
    "darkgoldenrod": "#B8860B",
    "darkgray": "#A9A9A9",
    "darkgreen": "#006400",
    "darkgrey": "#A9A9A9",
    "darkkhaki": "#BDB76B",
    "darkmagenta": "#8B008B",
    "darkolivegreen": "#556B2F",
    "darkorange": "#FF8C00",
    "darkorchid": "#9932CC",
    "darkred": "#8B0000",
    "darksalmon": "#E9967A",
    "darkseagreen": "#8FBC8F",
    "darkslateblue": "#483D8B",
    "darkslategray": "#2F4F4F",
    "darkslategrey": "#2F4F4F",
    "darkturquoise": "#00CED1",
    "darkviolet": "#9400D3",
    "deeppink": "#FF1493",
    "deepskyblue": "#00BFFF",
    "dimgray": "#696969",
    "dimgrey": "#696969",
    "dodgerblue": "#1E90FF",
    "firebrick": "#B22222",
    "floralwhite": "#FFFAF0",
    "forestgreen": "#228B22",
    "fuchsia": "#FF00FF",
    "gainsboro": "#DCDCDC",
    "ghostwhite": "#F8F8FF",
    "gold": "#FFD700",
    "goldenrod": "#DAA520",
    "gray": "#808080",
    "green": "#008000",
    "greenyellow": "#ADFF2F",
    "grey": "#808080",
    "honeydew": "#F0FFF0",
    "hotpink": "#FF69B4",
    "indianred": "#CD5C5C",
    "indigo": "#4B0082",
    "ivory": "#FFFFF0",
    "khaki": "#F0E68C",
    "lavender": "#E6E6FA",
    "lavenderblush": "#FFF0F5",
    "lawngreen": "#7CFC00",
    "lemonchiffon": "#FFFACD",
    "lightblue": "#ADD8E6",
    "lightcoral": "#F08080",
    "lightcyan": "#E0FFFF",
    "lightgoldenrodyellow": "#FAFAD2",
    "lightgray": "#D3D3D3",
    "lightgreen": "#90EE90",
    "lightgrey": "#D3D3D3",
    "lightpink": "#FFB6C1",
    "lightsalmon": "#FFA07A",
    "lightseagreen": "#20B2AA",
    "lightskyblue": "#87CEFA",
    "lightslategray": "#778899",
    "lightslategrey": "#778899",
    "lightsteelblue": "#B0C4DE",
    "lightyellow": "#FFFFE0",
    "lime": "#00FF00",
    "limegreen": "#32CD32",
    "linen": "#FAF0E6",
    "magenta": "#FF00FF",
    "maroon": "#800000",
    "mediumaquamarine": "#66CDAA",
    "mediumblue": "#0000CD",
    "mediumorchid": "#BA55D3",
    "mediumpurple": "#9370DB",
    "mediumseagreen": "#3CB371",
    "mediumslateblue": "#7B68EE",
    "mediumspringgreen": "#00FA9A",
    "mediumturquoise": "#48D1CC",
    "mediumvioletred": "#C71585",
    "midnightblue": "#191970",
    "mintcream": "#F5FFFA",
    "mistyrose": "#FFE4E1",
    "moccasin": "#FFE4B5",
    "navajowhite": "#FFDEAD",
    "navy": "#000080",
    "oldlace": "#FDF5E6",
    "olive": "#808000",
    "olivedrab": "#6B8E23",
    "orange": "#FFA500",
    "orangered": "#FF4500",
    "orchid": "#DA70D6",
    "palegoldenrod": "#EEE8AA",
    "palegreen": "#98FB98",
    "paleturquoise": "#AFEEEE",
    "palevioletred": "#DB7093",
    "papayawhip": "#FFEFD5",
    "peachpuff": "#FFDAB9",
    "peru": "#CD853F",
    "pink": "#FFC0CB",
    "plum": "#DDA0DD",
    "powderblue": "#B0E0E6",
    "purple": "#800080",
    "rebeccapurple": "#663399",
    "red": "#FF0000",
    "rosybrown": "#BC8F8F",
    "royalblue": "#4169E1",
    "saddlebrown": "#8B4513",
    "salmon": "#FA8072",
    "sandybrown": "#F4A460",
    "seagreen": "#2E8B57",
    "seashell": "#FFF5EE",
    "sienna": "#A0522D",
    "silver": "#C0C0C0",
    "skyblue": "#87CEEB",
    "slateblue": "#6A5ACD",
    "slategray": "#708090",
    "slategrey": "#708090",
    "snow": "#FFFAFA",
    "springgreen": "#00FF7F",
    "steelblue": "#4682B4",
    "tan": "#D2B48C",
    "teal": "#008080",
    "thistle": "#D8BFD8",
    "tomato": "#FF6347",
    "turquoise": "#40E0D0",
    "violet": "#EE82EE",
    "wheat": "#F5DEB3",
    "white": "#FFFFFF",
    "whitesmoke": "#F5F5F5",
    "yellow": "#FFFF00",
    "yellowgreen": "#9ACD32"
}

codeTable = {} #convert rgb to colorcode
levels = [0, 95, 135, 175, 215, 255]
code = 16
for r in levels:
    for g in levels:
        for b in levels:
            codeTable[(r, g, b)] = code
            code += 1
for i in range(24):
    gray = 8 + i * 10
    codeTable[(gray, gray, gray)] = 232 + i

def _getCode(prefix, color):
    code = codeTable.get(tuple(color))
    if code is not None:
        return f"{prefix}8;5;{code}"
    return f"{prefix}8;2;{color[0]};{color[1]};{color[2]}"

Number = int | float
"a single numeric value, either int or float"

class Color:
    assumeHsl = False
    
    @staticmethod
    def _normalizer(color, isHsl, target):
        if isHsl:
            hMultiplier = 1/360 if target else 360
            slMultiplier = 0.01 if target else 100
            h, s, l = color
            return (h*hMultiplier, s*slMultiplier, l*slMultiplier)
        else:
            rgbMultiplier = 1/255 if target else 255
            return tuple(int(val*rgbMultiplier) for val in color)
    
    @staticmethod
    def normalHelper(color: Sequence, isHsl: bool=False, normal: bool=None, asHsl:bool=None):
        #if normal is none, flip, else make it whatever normal is, in the provided color format
        
        current = False
        if isinstance(color, Sequence) and len(color)==3:
            for n in color:
                if isinstance(n, float) and 0 <= n <= 1:
                    current = True
                elif not (isinstance(n, int) and 0 <= n <= 255):
                    raise ValueError(f"color must be a sequence of exactly 3 numbers: ints in [0, 255] or floats in [0, 1]; got {repr(color)} instead")
        
        target = fallback(normal, not current)
        
        asHsl = fallback(asHsl, isHsl)
        if isHsl != asHsl:
            if not current:
                color = Color._normalizer(color, isHsl, True)
                current = True
            color = colour.hsl2rgb(color) if isHsl else colour.rgb2hsl(color)
            
        if current != target:
            color = Color._normalizer(color, asHsl, target)
        return color
    
    @staticmethod
    def parse(x, y=None, z=None, isHsl=None) -> ...:
        if isinstance(x, Color):
            return x.rgb, x.hsl
        elif isinstance(x, str):
            x = colorTable.get(x.lower(), x)
            return colour.hex2rgb(x), colour.hex2hsl(x)
        
        isHsl = fallback(isHsl, Color.assumeHsl)
        
        if isinstance(x, Sequence):
            if len(x) != 3: raise ValueError(f"if x is a sequence, it must consist of 3 ColorNumbers; got len {len(x)} instead")
            xyz = x
        else:
            xyz = (x,y,z)
        
        rgb = Color.normalHelper(xyz, isHsl, False, False) # if this errors, x, y or z is an incorrect color value
        hsl = Color.normalHelper(xyz, isHsl, True, True) # if this errors, Color.normalHelper broke
        return rgb, hsl
    
    @staticmethod
    def ansi(color, background=None):
        if isinstance(color, Color):
            color, background = color.rgb, fallback(background, color.background)
        return f"\033[{_getCode(4 if background else 3, color)}m"
    
    def __init__(self, x, y=None, z=None, background=False, isHsl=None):
        self.background = background
        isHsl = fallback(isHsl, Color.assumeHsl)
        self.rgb, self.hsl = self.parse(x, y, z, isHsl)
    
    def __str__(self):
        return self.ansi(self)
    def __add__(self, other):
        return str(self)+str(other)
    def __radd__(self, other):
        return str(other)+str(self)
    
    def __repr__(self):
        return f"Color(rgb={self.rgb}, hsl={self.hsl}, background={self.background})"
    
    def __call__(self, as_dict=False, as_hex=False, rgb_tuple=False, hsl_tuple=False, inverted=False, complementary=False):
        r, g, b = self.rgb
        h, s, l = self.hsl
        rgb_dirty = hsl_dirty = False

        if complementary:
            h, s, l = ((h+0.5)%1, s, 1-l)
            rgb_dirty = True

        if rgb_dirty and (as_dict or as_hex or rgb_tuple or inverted):
            r, g, b = self.normalHelper(colour.hsl2rgb((h,s,l), True, False), False, False)

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
        return self.ansi(self) # cause rgb may be dirty
    
    def __call__(self, RGBtriplet=False, HSLtriplet=False, asDict=False, asHex=False, inverted=False, complementary=False):
        r, g, b = self.rgb
        h, s, l = self.hsl
        RGBdirty = HSLdirty = False
        
        if complementary:
            h, s, l = ((h+0.5)%1, s, 1-l)
            RGBdirty = True
            
        if RGBdirty and (asDict or asHex or RGBtriplet or inverted):
            r, g, b = self.normalHelper((h,s,l), True, False, False)
        
        if inverted:
            r, g, b = (255-r, 255-g, 255-b)
            HSLdirty = True
        
        if HSLdirty and (asDict or HSLtriplet):
            h, s, l = self.normalHelper((r,g,b), False, True, True)
            
        if RGBtriplet and HSLtriplet:
            return (r, g, b), (h, s, l)
        if RGBtriplet:
            return (r, g, b)
        if HSLtriplet:
            return (h, s, l)
        if asDict:
            return {"r":r, "g":g, "b":b, "h":h, "s":s, "l":l, "rgb":(r,g,b), "hsl":(h,s,l)}
        if asHex:
            return '#%02x%02x%02x' % (r, g, b)
        return self.ansi((r,g,b), self.background) # cause rgb may be dirty

class Fore:
    black = "\033[30m"
    red = "\033[31m"
    green = "\033[32m"
    yellow = "\033[33m"
    blue = "\033[34m"
    magenta = "\033[35m"
    cyan = "\033[36m"
    white = "\033[37m"
    
    reset = "\033[39m"
    
    brightBlack = "\033[90m"
    brightRed = "\033[91m"
    brightGreen = "\033[92m"
    brightYellow = "\033[93m"
    brightBlue = "\033[94m"
    brightMagenta = "\033[95m"
    brightCyan = "\033[96m"
    brightWhite = "\033[97m"
    
    def __call__(self, x, y=None, z=None, isHsl=None):
        return Color(x, y, z, False, isHsl)

class Back:
    black = "\033[40m"
    red = "\033[41m"
    green = "\033[42m"
    yellow = "\033[43m"
    blue = "\033[44m"
    magenta = "\033[45m"
    cyan = "\033[46m"
    white = "\033[47m"
    
    reset = "\033[49m"
    
    brightBlack = "\033[100m"
    brightRed = "\033[101m"
    brightGreen = "\033[102m"
    brightYellow = "\033[103m"
    brightBlue = "\033[104m"
    brightMagenta = "\033[105m"
    brightCyan = "\033[106m"
    brightWhite = "\033[107m"
    
    def __call__(self, x, y=None, z=None, isHsl=None):
        return Color(x, y, z, True, isHsl)

class Style:
    Bold = "\033[1m"
    Dim = "\033[2m"
    Italic = "\033[3m"
    Underline = "\033[4m"
    SlowBlink = "\033[5m"
    FastBlink = "\033[6m"
    Negative = "\033[7m"
    Conceal = "\033[8m"
    Strikethrough = "\033[9m"
    Bold = "\033[1m"
    
    noBold = "\033[22m"
    
    
    Underline = "\033[4m"
    noUnderline = "\033[24m"
    Negative = "\033[7m"
    noNegative = Positive = "\033[27m"
    
    reset = "\033[0m"

class StyleExtended:
    doubleUnderlineAlt = "\033[4:2m"
    doubleUnderline = "\033[21m"