# Pcbnew Transition

This library allows you to easily support KiCAD 9, 8, 7 and 6 in your KiCAD
plugins. It basically monkeypatches the KiCAD Python module, so it matches KiCAD 9
API.

## Important notice

As KiCAD is deprecating the SWIG based API, this project is also becoming
deprecated. There won't be any support for KiCAD 10+.

Using this library in new projects is strongly discouraged as of 2026.

## Usage

Instead of:

```python
import pcbnew
from pcbnew import EDA_ANGLE
```

Use:

```python
from pcbnewTransition import pcbnew
from pcbnewTransition.pcbnew import EDA_ANGLE
```

And then, use the API for KiCAD 8. If you need to distinguish the versions,
you can:

```python
from pcbnewTransition import KICAD_VERSION, isV6

if isV6():
    # something...
```
