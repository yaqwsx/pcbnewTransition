# Pcbnew Transition

This library allows you to easily support both, KiCAD 6 and KiCAD 5 in your
KiCAD plugins. It basically monkeypatches KiCAD 5 Python module, so it matches
KiCAD 6 API.

Note: By KiCAD 6 I mean current nightly (v5.99).

## Usage

Instead of:

```python
import pcbnew
```

Use:

```python
from pcbnewTransition import pcbnew
```

And then, use the API for KiCAD 6. In case you need to distinguish v5 and v6,
you can:

```python
from pcbnewTransition import KICAD_VERSION, isV6

if isV6():
    # something...
```
