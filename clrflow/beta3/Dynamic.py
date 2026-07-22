# please dont overthink it

# dependencies
from Universal import stripAnsi, fallback
import shutil
# types
from collections.abc import Callable
from typing import Literal

class RichText:
    def __init__(self, string: str):
        self.string = string
        self.probes = {}
        self.features = {}
        self.metadata = {}
        self.hashes = {}
    
    @staticmethod
    def _toposort(original: dict):
        remaining = {k: tuple(filter(lambda x: x in original, v._featurePredecessors)) for k, v in original.items()}
        layers = {}
        layer = 0

        while remaining:
            if layer >= len(original):
                raise ValueError(f"circular dependency detected:\n{remaining}")
            
            seen = {}
            for k, v in remaining.items():
                layers[k] = layer
                for d in v:
                    seen[d] = remaining[d]
            
            remaining = seen
            layer += 1
        
        return dict(sorted(original.items(), key=lambda x:layers[x[0]], reverse=True))
    
    def addEngine(self, engine: Engine): # this looks ugly
        if not issubclass(engine, Engine):
            raise ValueError("engine must be subclass of the base Engine class")
        
        if (getattr(engine, "probe", None) is not None):
            self.probes[engine.name] = engine
            
        if (not engine.name in self.features) and (getattr(engine, "feature", None) is not None):
            self.features[engine.name] = engine
            self.features = self._toposort(self.features)
        
        self.metadata.update(engine.configuration)
        self.hashes[engine.name] = hash(engine)
        
    def removeEngine(self, engine):
        if issubclass(engine, Engine):
            engine = engine.name
        
        self.probes.pop(engine,None)
        self.features.pop(engine,None)
    
    def __str__(self):
        string = self.string # copy
        
        if (self.hashes.get("string", None) != hash(string)) or (self.metadata.get("stripped_string", None) is None):
            self.metadata["stripped_string"] = stripAnsi(string)
            self.hashes["string"] = hash(string)
            
        ctx = {}
        stripped = self.metadata["stripped_string"]
        
        for engine in self.probes:
            engine.probe(self, ctx, stripped) # gather info and add to ctx. engines can share their own info and measurements
        
        for engine in self.features:
            string = engine.feature(self, ctx, string) # features can also append context here if necessary
            
        return string

class Engine:
    """Engine class. serves as the base for any engine capable of applying features to RichText, given the measurements made by any necessary probes"""
    name = "rver38_Base"
    # prefix engine names with your own username
    _featurePredecessors = ()
    # names of features that must come before the own if installed. you must enforce the presence of predecessor engines/probes yourself in the probe/feature functions.
    
    def __init__(self, *settings):
        # store input settings if necessary
        pass
    
    def __hash__(self):
        # return a hash of anything hashable
        pass
    
    @classmethod
    def addFeaturePredecessor(cls, *names): # for other modules
        cls._featurePredecessors += names
    
    def probe(self, container, ctx): # optional if no data is required for feature
        # measure stuff here and mutate ctx
        pass
    
    def feature(self, container, ctx, string):
        # apply features to string here using ctx and container.metadata, optionally mutate ctx
        return string
    
    def __call__(self, text, *settings):
        if not isinstance(text, RichText):
            text = RichText(text)
        text.addEngine(self)
        return text

class ColorMatrix:
    def rotate45(self):
        ...
    def rotate90(self):
        ...
    def rotate180(self):
        ...
    def mirrorX(self):
        ...
    def mirrorY(self):
        ...

class Gradient(Engine):
    name = "rver38_Gradient"
    _featureDependencies = ('rver38_Align',)
    _presets = {}
    
    @staticmethod
    def _getStringDimensions(text: RichText): 
        lines = text.metadata["stripped_string"].splitlines()
        return len(max(lines, key=len)), len(lines)
    
    @staticmethod
    def _getTerminalDimensions(_):
        return shutil.get_terminal_size((80, 24))
        
    @staticmethod
    def _makeFixedDimensions(dimensions):
        return lambda _: dimensions
    
    @staticmethod
    def _scaleDimensions(dimensions, scale):
        w, h = dimensions
        
        if not all(filter(lambda x: x > 0, dimensions)):
            raise ValueError(f"dimensions must be at minimum (1,1); got {dimensions}")
        
        if isinstance(scale, float): # scale both dimensions
            return (int(w*scale), int(h*scale))
        
        if w >= h: # scale both dimensions such that the bigger dimension is scale, and the aspect ratio stays the same
            return (scale, int((h/w)*scale))
        return (int((w/h)*scale), scale)
    
    def __init__(self, *,
        foregroundMatrix: ColorMatrix = None,
        backgroundMatrix: ColorMatrix = None,
        dimensions: Literal["string", "viewport"] | Callable[[RichText], tuple[int, int]] | tuple[int, int] = "string",
        scale: int | float = 1.0,
        resolution: int = 2
    ):
        match dimensions:
            case "string":
                dimensions = self._getStringDimensions
            case "viewport":
                dimensions = self._getTerminalDimensions
            case (int() as w, int() as h):
                dimensions = self._makeFixedDimensions(dimensions)
            case _ if callable(dimensions):
                pass
            case x:
                raise ValueError(
                    "dimensions must be\n"
                    " - the literal 'string' or 'viewport',\n"
                    " - a 2-integer tuple (width, height),\n"
                    " - any function that takes in a RichText instance and outputs a 2-integer tuple;\n"
                    f"got dimensions={x} instead"
                )
        self.configuration = {"gradForeMatrix": foregroundMatrix, "gradBackMatrix": backgroundMatrix, "gradDimensions": dimensions, "gradScale": scale, "gradRes": resolution}
    
    def __hash__(self):
        return hash(self.configuration.values())
    
    def __call__(self, text):
        if not isinstance(text, RichText):
            text = RichText(text)
        text.addEngine(self)
        return text 
    
    def probe(self, container, ctx):
        ctx["gradHash"] = hash(self)
        dimensions = container.metadata["gradDimensions"]
        scale = container.metadata["gradScale"]
        ctx["gradDimensions"] = self._scaleDimensions(dimensions(container), scale)
        
    def feature(self, container, ctx, string):
        ...
        

g = Gradient(dimensions=None)
text = g("hey")