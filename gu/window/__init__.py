from ._input import input

from ..system import platform

if platform == 2:
    from ._macos import Window

