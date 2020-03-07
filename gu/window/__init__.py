import sys

# 根据不同的系统载入不同的创建程序
if sys.platform in ('win32', 'cygwin'):
    from ._win32_window import Win32Window as Window

elif sys.platform == 'darwin':
    from ._objc_window import MacWindow as Window

else:
    pass
    # 用 tkinter 做一个窗口
