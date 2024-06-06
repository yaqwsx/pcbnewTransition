
from . import _version
__version__ = _version.get_versions()['version']

# A (temporary) hack follows!
#
# Some packages on Linux for v7 change the location of the pcbnew module, let's
# add the new location to path. The native library is also in this location,
# thus, the loader can't load it. We trick it into loading by loading it first
# by an absolute path
import os
import sys
if os.name != "nt":
    sys.path.append("/usr/lib/kicad/lib/python3/dist-packages")
    try:
        from ctypes import cdll
        cdll.LoadLibrary("/usr/lib/kicad/lib/x86_64-linux-gnu/libkicad_3dsg.so.2.0.0")
    except Exception:
        pass # Ignore any errors as the library just might not exists here


from .transition import *
