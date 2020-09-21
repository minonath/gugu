from ..system import SYSTEM_PLATFORM

if SYSTEM_PLATFORM == 1:
    raise NotImplementedError
elif SYSTEM_PLATFORM == 2:
    from ._mac_window import Window
    # from .mac_font import Font
else:
    raise NotImplementedError
