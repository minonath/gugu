import ctypes
import io

from gu.opengl import context, Program, VertexArray, Rule
from gu.opengl.library import *
from gu.matrix import Floats, Matrix4, Vector3
from gu.system import resource, gu
from gu.sprite.png_library import read_png

gu.window(title='General Image', width=400, height=300)

glClearColor(0.5, 0.5, 0.5, 1.0)
