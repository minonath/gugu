import platform

if platform.system() == 'Darwin':
    from ._objc_window import create_mac_window
