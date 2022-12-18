
import pcbnew
import types

# KiCAD 6 renames some of the types, ensure compatibility by introducing aliases
# when KiCAD 5 is used

def getVersion():
    try:
        v = [int(x) for x in pcbnew.GetMajorMinorVersion().split(".")]
        return tuple(v)
    except AttributeError:
        # KiCAD 5 does not have such function, assume it version 5.something
        return 5, 0

def boardGetProperties(self):
    return {}

def boardSetProperties(self, p):
    pass

def GetBoundingBox(self, includeText=True, includeInvisibleText=True):
    if not includeText and not includeInvisibleText:
        return self.GetFootprintRect()
    if includeText and includeInvisibleText:
        return self._GetBoundingBox()
    raise NotImplementedError("Incompatible v5 and v6 API")

def getAuxOrigin(self):
    return self.m_AuxOrigin

def setAuxOrigin(self, o):
    self.m_AuxOrigin = o

def NewBoard(filename):
    return pcbnew.BOARD()

def patchRotate(item):
    if hasattr(item, "Rotate"):
        originalRotate = item.Rotate
        if not getattr(originalRotate, "patched", False):
            newRotate = lambda self, center, angle: originalRotate(self, center, angle.AsTenthsOfADegree())
            setattr(newRotate, "patched", True)
            item.Rotate = newRotate
    if hasattr(item, "SetOrientation"):
        originalSetOrientation = item.SetOrientation
        if not getattr(originalSetOrientation, "patched", False):
            newSetOrientation = lambda self, angle: originalSetOrientation(self, angle.AsTenthsOfADegree())
            setattr(newSetOrientation, "patched", True)
            item.SetOrientation = newSetOrientation
    if hasattr(item, "GetOrientation"):
        originalGetOrientation = item.GetOrientation
        if not getattr(originalGetOrientation, "patched", False):
            newGetOrientation = lambda self: pcbnew.EDA_ANGLE(originalGetOrientation(self), pcbnew.TENTHS_OF_A_DEGREE_T)
            setattr(newGetOrientation, "patched", True)
            item.GetOrientation = newGetOrientation
    if hasattr(item, "GetDrawRotation"):
        originalGetDrawRotation = item.GetDrawRotation
        if not getattr(originalGetDrawRotation, "patched", False):
            newGetDrawRotation = lambda self: pcbnew.EDA_ANGLE(originalGetDrawRotation(self), pcbnew.TENTHS_OF_A_DEGREE_T)
            setattr(newGetDrawRotation, "patched", True)
            item.GetDrawRotation = newGetDrawRotation
    if hasattr(item, "SetTextAngle"):
        originalSetTextAngle = item.SetTextAngle
        if not getattr(originalSetTextAngle, "patched", False):
            newSetTextAngle = lambda self, angle: originalSetTextAngle(self, angle.AsTenthsOfADegree())
            setattr(newSetTextAngle, "patched", True)
            item.SetTextAngle = newSetTextAngle

KICAD_VERSION = getVersion()

def isV6(version=KICAD_VERSION):
    if version[0] == 5 and version[1] == 99:
        return True
    return version[0] == 6

def isV7(version=KICAD_VERSION):
    if version[0] == 6 and version[1] == 99:
        return True
    return version[0] == 7

if not isV6(KICAD_VERSION):
    # Introduce new functions
    pcbnew.NewBoard = NewBoard

    # Introduce type aliases
    pcbnew.PCB_SHAPE = pcbnew.DRAWSEGMENT
    pcbnew.FP_SHAPE = pcbnew.EDGE_MODULE
    pcbnew.PCB_TEXT = pcbnew.TEXTE_PCB
    pcbnew.FP_TEXT = pcbnew.TEXTE_MODULE
    pcbnew.ZONE = pcbnew.ZONE_CONTAINER
    pcbnew.ZONES = pcbnew.ZONE_CONTAINERS
    pcbnew.DXF_UNITS_MILLIMETERS = pcbnew.DXF_PLOTTER.DXF_UNIT_MILLIMETERS

    # Introduce renamed functions
    pcbnew.BOARD.GetFootprints = pcbnew.BOARD.GetModules
    pcbnew.BOARD.FindFootprintByReference = pcbnew.BOARD.FindModuleByReference

    pcbnew.MODULE._GetBoundingBox = pcbnew.MODULE.GetBoundingBox
    pcbnew.MODULE.GetBoundingBox = GetBoundingBox

    # Add board properties
    pcbnew.BOARD.GetProperties = boardGetProperties
    pcbnew.BOARD.SetProperties = boardSetProperties
    pcbnew.BOARD_DESIGN_SETTINGS.GetAuxOrigin = getAuxOrigin
    pcbnew.BOARD_DESIGN_SETTINGS.SetAuxOrigin = setAuxOrigin

    # NETINFO_ITEM
    pcbnew.NETINFO_ITEM.GetNetCode = pcbnew.NETINFO_ITEM.GetNet

    # PCB_SHAPE
    pcbnew.PCB_SHAPE.GetArcAngle = pcbnew.DRAWSEGMENT.GetAngle

    # PLOTTING ENUMS
    pcbnew.PLOT_TEXT_MODE_STROKE = pcbnew.PLOTTEXTMODE_STROKE
    pcbnew.PLOT_TEXT_MODE_DEFAULT = pcbnew.PLOTTEXTMODE_DEFAULT
    pcbnew.PLOT_TEXT_MODE_NATIVE = pcbnew.PLOTTEXTMODE_NATIVE
    pcbnew.PLOT_TEXT_MODE_PHANTOM = pcbnew.PLOTTEXTMODE_PHANTOM

    pcbnew.PCB_PLOT_PARAMS.SetSketchPadLineWidth = pcbnew.PCB_PLOT_PARAMS.SetLineWidth

    # ZONE
    pcbnew.ZONE.SetIsRuleArea = pcbnew.ZONE.SetIsKeepout

    # PCB_TEXT
    pcbnew.PCB_TEXT.SetTextThickness = pcbnew.PCB_TEXT.SetThickness

#### V7 compatibility section
try:
    from pcbnew import EDA_ANGLE as _transition_EDA_ANGLE
except ImportError:
    from .eda_angle import EDA_ANGLE_T, EDA_ANGLE
    pcbnew.EDA_ANGLE = EDA_ANGLE
    pcbnew.DEGREES_T = EDA_ANGLE_T.DEGREES_T
    pcbnew.RADIANS_T = EDA_ANGLE_T.RADIANS_T
    pcbnew.TENTHS_OF_A_DEGREE_T = EDA_ANGLE_T.TENTHS_OF_A_DEGREE_T

if not isV7(KICAD_VERSION):
    # VECTOR2I & wxPoint
    class _transition_VECTOR2I(pcbnew.wxPoint):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

    pcbnew.VECTOR2I = _transition_VECTOR2I

    # EDA_RECT and BOX2I
    class _transition_BOX2I(pcbnew.EDA_RECT):
        def __init__(self, *args):
            # We now use this to construct BOX2I and the points are VECTOR2I
            if len(args) == 2 and isinstance(args[0], pcbnew.wxPoint) and isinstance(args[1], pcbnew.wxPoint):
                super().__init__(pcbnew.wxPoint(*args[0]), pcbnew.wxSize(*args[1]))
            else:
                super().__init__(*args)
    pcbnew.BOX2I = _transition_BOX2I

    # DRILL_MARKS
    pcbnew.DRILL_MARKS_NO_DRILL_SHAPE = 0
    pcbnew.DRILL_MARKS_SMALL_DRILL_SHAPE = 1
    pcbnew.DRILL_MARKS_FULL_DRILL_SHAPE = 2

    # ZONE
    pcbnew.ZONE.SetAssignedPriority = pcbnew.ZONE.SetPriority
    pcbnew.ZONE.GetAssignedPriority = pcbnew.ZONE.GetPriority

    # Orientation
    for x in dir(pcbnew):
        patchRotate(getattr(pcbnew, x))

    originalCalcArcAngles = pcbnew.EDA_SHAPE.CalcArcAngles
    if not getattr(originalCalcArcAngles, "patched", False):
        def newCalcArcAngles(self, start, end):
            start.value = self.GetArcAngleStart() / 10
            if self.GetShape() == pcbnew.SHAPE_T_CIRCLE:
                end.value = start.value + 360
            else:
                end.value = start.value + self.GetArcAngle() / 10
        setattr(newCalcArcAngles, "patched", True)
        pcbnew.EDA_SHAPE.CalcArcAngles = newCalcArcAngles

    # EDA_TEXT
    originalTextSize = pcbnew.EDA_TEXT.SetTextSize
    pcbnew.EDA_TEXT.SetTextSize = lambda self, size: originalTextSize(self, pcbnew.wxSize(size[0], size[1]))

    # PAD
    originalSetDrillSize = pcbnew.PAD.SetDrillSize
    pcbnew.PAD.SetDrillSize = lambda self, size: originalSetDrillSize(self, pcbnew.wxSize(size[0], size[1]))

    originalSetSize = pcbnew.PAD.SetSize
    pcbnew.PAD.SetSize = lambda self, size: originalSetSize(self, pcbnew.wxSize(size[0], size[1]))

