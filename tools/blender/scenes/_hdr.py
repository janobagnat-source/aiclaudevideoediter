# encabezado común: importar studio desde la carpeta padre
import math, os, random, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from studio import Studio, hexlin  # noqa
import bpy  # noqa
from mathutils import Vector  # noqa
