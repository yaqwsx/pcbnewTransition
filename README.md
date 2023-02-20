# Pcbnew Transition

This library allows you to easily support all, KiCAD 7, 6 and 5 in your KiCAD
plugins. It basically monkeypatches KiCAD Python module, so it matches KiCAD 7
API.
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

And then, use the API for KiCAD 8. In case you need to distinguish the versions,
you can:

```python
from pcbnewTransition import KICAD_VERSION, isV6

if isV6():
    # something...
```
