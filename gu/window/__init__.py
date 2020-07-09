from ..system import SYSTEM_PLATFORM
from .base import window_input, gl_context

if SYSTEM_PLATFORM == 1:
    raise NotImplementedError
elif SYSTEM_PLATFORM == 2:
    from ..window.macos import Window
else:
    raise NotImplementedError
