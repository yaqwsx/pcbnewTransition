import pcbnew as pcbnewOrig
from pcbnew import *
import inspect

def inherit_classes(module):
    classes = inspect.getmembers(module, inspect.isclass)

    for class_name, class_obj in classes:
        new_class = type(class_name, (class_obj,), {})
        globals()[class_name] = new_class

inherit_classes(pcbnewOrig)
