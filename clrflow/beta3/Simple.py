from collections.abc import Sequence
from Universal import fallback, getColorTerm
import colour

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

class Color:
    def __init__(self, x: int | Sequence | str, y: int = None, z: int = None, background: bool = False):
        if isinstance(x, Color):
            self.xyz = x.xyz
            
        elif isinstance(x, str):
            x = colorTable.get(x.lower(),x)
            xyz = tuple(int(255*c) for c in colour.hex2rgb(x))
            
        elif isinstance(x, Sequence):
            xyz = x
        
        else:
            xyz = (x,y,z)
        
        condition = (not isinstance(c, int) for c in xyz)
        if any(condition) or (len(condition) != 3):
            raise ValueError("xyz must be exactly 3 numbers")
        
        self.xyz = xyz
        self.background = background
    
    def ansi(self, color=None, background=None):
        color, background = fallback(color, self.xyz), fallback(background, self.background)
        return f"{getColorTerm(4 if background else 3, color)}"
    
    def __str__(self):
        return f"\033[{self.ansi()}m"
    
    def __add__(self, other):
        if not isinstance(other, Format):
            return str(self) + other
        
        tmp = Format()
        tmp.properties = [self.ansi(), *other.properties]
        return tmp
    
    def __radd__(self, other):
        return other + str(self)
    
    def __repr__(self):
        return f"<Color(xyz={self.xyz}, background={self.background})>"
    
    #def __call__(self)
    
class Format:
    def __init__(self, *codes):
        self.properties = list(codes)
    
    def __add__(self, other):
        if not isinstance(other, Format):
            return str(self) + other

        tmp = Format()
        tmp.properties = self.properties + other.properties
        return tmp
    
    def __radd__(self, other):
        return other + str(self)
    
    def __str__(self):
        return f"\033[{";".join(self.properties)}m"
_f = Format

# https://en.wikipedia.org/wiki/ANSI_escape_code

class _Fore:
    black = _f("30")
    red = _f("31")
    green = _f("32")
    yellow = _f("33")
    blue = _f("34")
    magenta = _f("35")
    cyan = _f("36")
    white = _f("37")
    
    reset = _f("39")
    
    brightBlack = _f("90")
    brightRed = _f("91")
    brightGreen = _f("92")
    brightYellow = _f("93")
    brightBlue = _f("94")
    brightMagenta = _f("95")
    brightCyan = _f("96")
    brightWhite = _f("97")
    
    def __call__(self, x, y=None, z=None):
        return Color(x, y, z, False)

Fore = _Fore()
    
class _Back:
    black = _f("40")
    red = _f("41")
    green = _f("42")
    yellow = _f("43")
    blue = _f("44")
    magenta = _f("45")
    cyan = _f("46")
    white = _f("47")
    
    reset = _f("49")
    
    brightBlack = _f("100")
    brightRed = _f("101")
    brightGreen = _f("102")
    brightYellow = _f("103")
    brightBlue = _f("104")
    brightMagenta = _f("105")
    brightCyan = _f("106")
    brightWhite = _f("107")
    
    def __call__(self, x, y=None, z=None):
        return Color(x, y, z, True)

Back = _Back()

# fact check this
class Style:
    "universal formatting options such as bold, italic, etc."
    Bold = _f("1")
    Dim = Faint = _f("2")
    noBold = noDim = noFaint = _f("22")
    
    Italic = _f("3")
    noItalic = _f("23")
    
    Underline = _f("4")
    noUnderline = _f("24")
    
    SlowBlink = _f("5")
    FastBlink = _f("6")
    noBlink = _f("25")
    
    Negative = _f("7")
    noNegative = Positive = _f("27")
    
    Conceal = _f("8")
    noConceal = Reveal =  _f("28")
    
    Strikethrough = _f("9")
    noStrikethrough = _f("29")
    
    Overline = _f("53")
    noOverline = _f("55")
    
    reset = _f("0")

class StyleExtras:
    "extra formatting that is not universally supported and should not be expected to work everywhere"
    Framed = _f("51")
    Encircled = _f("52")
    
    UnderlineColor = lambda r,g,b: _f(getColorTerm(5, (r,g,b)))
    resetUnderlineColor = _f("59")
    
    Superscript = _f("73")
    Subscript = _f("74")
    noScript = _f("75")
    
class Terminal: #meant to be stuff like background color
    # print("\033[48;2;125;175;200m\033[2J\033[H", end="") # background color
    ...