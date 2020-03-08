import ctypes
import time
from ._window_prototype import WindowPrototype
from gu.system import gu
from ctypes.wintypes import *

WM_DESTROY = 2
WM_SIZE = 5
WM_KEYDOWN = 256
WM_KEYUP = 257
WM_CHAR = 258
WM_SYSKEYDOWN = 260
WM_SYSKEYUP = 261
WM_SYSCHAR = 262
WM_UNICHAR = 265
WM_MOUSEMOVE = 512
WM_LBUTTONDOWN = 513
WM_LBUTTONUP = 514
WM_RBUTTONDOWN = 516
WM_RBUTTONUP = 517
WM_MBUTTONDOWN = 519
WM_MBUTTONUP = 520
WM_MOUSEWHEEL = 522
WM_MOUSEHWHEEL = 0x020E
WM_MOUSELEAVE = 0x02A3
WM_INPUT = 255
WHEEL_DELTA = 120


WNDPROC = ctypes.WINFUNCTYPE(LPARAM, HWND, UINT, WPARAM, LPARAM)


class WndClassEx(ctypes.Structure):
    _fields_ = [
        ('size', UINT), ('style', UINT), ('wndproc', WNDPROC),
        ('class_extra', INT), ('window_extra', INT), ('instance', HINSTANCE),
        ('icon', HANDLE), ('cursor', HANDLE), ('background', HBRUSH),
        ('menu_name', LPCWSTR), ('class_name', LPCWSTR), ('icon_small', HICON)
    ]


user32 = gu.bind_dynamic_library(ctypes.windll.user32)
RegisterClass = user32('RegisterClassExW', ATOM, ctypes.POINTER(WndClassEx))
CreateWindow = user32(
    'CreateWindowExW', HANDLE, DWORD, LPCWSTR, LPCWSTR, DWORD,
    INT, INT, INT, INT, HANDLE, HANDLE, HANDLE, LPVOID)
UpdateWindow = user32('UpdateWindow', BOOL, HANDLE)
GetDC = user32('GetDC', HDC, HWND)
ReleaseDC = user32('ReleaseDC', BOOL, HWND, HDC)
# ShowCursor = user32('ShowCursor',INT, BOOL)
DefWindowProc = user32('DefWindowProcW', LPARAM, HWND, UINT, WPARAM, LPARAM)
PeekMessage = user32(
    'PeekMessageW', BOOL, ctypes.POINTER(MSG), HWND, UINT, UINT, UINT)
TranslateMessage = user32('TranslateMessage', BOOL, ctypes.POINTER(MSG))
DispatchMessage = user32('DispatchMessageW', BOOL, ctypes.POINTER(MSG))
# VkKeyScan = user32('VkKeyScanW', ctypes.c_short, HANDLE)
GetCursorPos = user32('GetCursorPos', BOOL, ctypes.POINTER(POINT))
ScreenToClient = user32('ScreenToClient', BOOL, HWND, ctypes.POINTER(POINT))

gl32 = gu.bind_dynamic_library(ctypes.windll.opengl32)
wglMakeCurrent = gl32('wglMakeCurrent', BOOL, HDC, HANDLE)
wglCreateContext = gl32('wglCreateContext', HANDLE, HDC)
wglGetCurrentDC = gl32('wglGetCurrentDC', HDC)
wglDeleteContext = gl32('wglDeleteContext', BOOL, HANDLE)
wglGetCurrentContext = gl32('wglGetCurrentContext', HANDLE)
wglSwapBuffers = gl32('wglSwapBuffers', BOOL, HDC)


class PixelFormatDescriptor(ctypes.Structure):
    _fields_ = [
        ('size', WORD), ('version', WORD), ('flags', DWORD), ('pixel', BYTE),
        ('color_bits', BYTE), ('red_bits', BYTE), ('red_shift', BYTE),
        ('green_bits', BYTE), ('cGreen_shift', BYTE), ('blue_bits', BYTE),
        ('blue_shift', BYTE), ('alpha_bits', BYTE), ('alpha_shift', BYTE),
        ('acc_bits', BYTE), ('acc_red_bits', BYTE), ('acc_green_bits', BYTE),
        ('acc_blue_bits', BYTE), ('acc_alpha_bits', BYTE),
        ('depth_bits', BYTE), ('stencil_bits', BYTE), ('aux_buffer', BYTE),
        ('layer_type', BYTE), ('reserved', BYTE), ('layer_mask', DWORD),
        ('visible_mask', DWORD), ('damage_mask', DWORD)
    ]


gdi32 = gu.bind_dynamic_library(ctypes.windll.gdi32)
GetStockObject = gdi32('GetStockObject', HANDLE, INT)
GetDeviceCaps = gdi32('GetDeviceCaps', INT, HANDLE, INT)
ChoosePixelFormat = gdi32(
    'ChoosePixelFormat', INT, HDC, ctypes.POINTER(PixelFormatDescriptor))
SetPixelFormat = gdi32(
    'SetPixelFormat', BOOL, HDC, INT, ctypes.POINTER(PixelFormatDescriptor))


def fill_structure(structure, *args, **kwargs):
    tmp = structure()
    if args:
        for k, v in zip(structure._fields_, args):
            setattr(tmp, k[0], v)
    for k in kwargs:
        setattr(tmp, k, kwargs[k])
    return tmp


def default_max_size():
    return 800, 600


# Window 使用的是完全的消息钩子，和 Mac 藏起消息钩子的做法不一样，所以我们可以完全接管。
WINDOWS_EVENT = {}  # 接管函数放这里


def event_bind(event_code):
    def wrap(function):
        WINDOWS_EVENT[event_code] = function
        return function

    return wrap


class Win32Window(WindowPrototype):
    def __init__(self, title='Gu', size=None, fps=30):
        if not size:  # 如果没有设置尺寸，以（非全屏）最大窗口创建。
            size = default_max_size()

        WindowPrototype.__init__(self, title, size, fps)
        self.window_run = False
        self.window_clock = time.perf_counter()

        self.window_window = None
        self.mouse_down_mask = 0

    def prepare_event_function(self):
        @event_bind(WM_DESTROY)
        def wndproc(hwnd, message, wparam, lparam):
            hdc = wglGetCurrentDC()
            wglDeleteContext(wglGetCurrentContext())
            ReleaseDC(hwnd, hdc)
            self.window_run = False

        @event_bind(WM_SIZE)
        def wndproc(hwnd, message, wparam, lparam):
            width = ctypes.c_int16(lparam & 0xFFFF).value
            height = ctypes.c_int16(lparam >> 16).value
            self.sync_push(self.window_resize, width, height)

        @event_bind(WM_KEYDOWN)
        @event_bind(WM_SYSKEYDOWN)
        @event_bind(WM_KEYUP)
        @event_bind(WM_SYSKEYUP)
        def wndproc(hwnd, message, wparam, lparam):
            key_code = ctypes.c_int16(lparam >> 16).value & 0x1FF
            self.sync_push(gu.keyboard.__call__, key_code)

        @event_bind(WM_CHAR)
        @event_bind(WM_SYSCHAR)
        def wndproc(hwnd, message, wparam, lparam):
            self.sync_push(self.window_char, wparam)

        @event_bind(WM_UNICHAR)
        def wndproc(hwnd, message, wparam, lparam):
            return True

        @event_bind(WM_MOUSEMOVE)
        def wndproc(hwnd, message, wparam, lparam):
            mouse_x = ctypes.c_int16(lparam & 0xFFFF).value
            mouse_y = ctypes.c_int16(lparam >> 16).value
            delta_x = mouse_x - self.mouse_x
            delta_y = mouse_y - self.mouse_y
            self.mouse_x, self.mouse_y = mouse_x, mouse_y
            # mouse_drag 检测
            if self.mouse_down_mask == 0:
                self.sync_push(self.mouse_move, delta_x, delta_y)
            elif self.mouse_down_mask == 1:
                self.sync_push(self.mouse_dragged, delta_x, delta_y)
            elif self.mouse_down_mask == 2:
                self.sync_push(self.mouse_right_dragged, delta_x, delta_y)
            elif self.mouse_down_mask == 3:
                self.sync_push(self.mouse_other_dragged, delta_x, delta_y)

        @event_bind(WM_LBUTTONDOWN)
        def wndproc(hwnd, message, wparam, lparam):
            self.mouse_down_mask = 1
            self.sync_push(self.mouse_down, self.mouse_x, self.mouse_y)

        @event_bind(WM_LBUTTONUP)
        def wndproc(hwnd, message, wparam, lparam):
            self.mouse_down_mask = 0
            self.sync_push(self.mouse_up, self.mouse_x, self.mouse_y)

        @event_bind(WM_RBUTTONDOWN)
        def wndproc(hwnd, message, wparam, lparam):
            self.mouse_down_mask = 2
            self.sync_push(self.mouse_right_down, self.mouse_x, self.mouse_y)

        @event_bind(WM_RBUTTONUP)
        def wndproc(hwnd, message, wparam, lparam):
            self.mouse_down_mask = 0
            self.sync_push(self.mouse_right_up, self.mouse_x, self.mouse_y)

        @event_bind(WM_MBUTTONDOWN)
        def wndproc(hwnd, message, wparam, lparam):
            self.mouse_down_mask = 3
            self.sync_push(self.mouse_other_down, self.mouse_x, self.mouse_y)

        @event_bind(WM_MBUTTONUP)
        def wndproc(hwnd, message, wparam, lparam):
            self.mouse_down_mask = 0
            self.sync_push(self.mouse_other_up, self.mouse_x, self.mouse_y)

        @event_bind(WM_INPUT)  # 获取屏幕输入点
        def wndproc(hwnd, message, wparam, lparam):
            pass

        @event_bind(WM_MOUSEWHEEL)
        def wndproc(hwnd, message, wparam, lparam):
            delta = ctypes.c_int16(wparam >> 16).value // WHEEL_DELTA
            self.sync_push(self.mouse_scroll_wheel, 0, delta)

        @event_bind(WM_MOUSEHWHEEL)  # XP 上不支持这个
        def wndproc(hwnd, message, wparam, lparam):
            delta = -ctypes.c_int16(wparam >> 16).value // WHEEL_DELTA
            self.sync_push(self.mouse_scroll_wheel, delta, 0)

        # @event_bind(WM_MOUSELEAVE)
        # @event_bind(WM_MOUSEENTER)
        # 这两个需要自己去勾消息，比较麻烦
        def callback(*args):
            func = WINDOWS_EVENT.get(args[1], None)
            if func:
                return func(*args) and 1 or 0
            return DefWindowProc(*args)

        return callback

    def get_mouse_position(self):
        position = ctypes.POINTER(POINT)()
        GetCursorPos(position)
        ScreenToClient(self.window_window, position)

        self.mouse_x = position[0].x
        self.mouse_y = position[0].y

    def sleep_time(self):
        """
        沉睡一段时间，控制帧数
        """
        current_clock = time.perf_counter()  # 当前时间
        frame_clock = current_clock - self.window_clock  # 上一帧实际经历的时间
        sleep_clock = self.window_interval - frame_clock  # 需要沉睡的时间
        if sleep_clock > 0:  # 判断是否掉帧了
            time.sleep(sleep_clock)  # 没有掉帧就沉睡
        current_clock = time.perf_counter()  # 再次计算当前时间
        interval_clock = current_clock - self.window_clock  # 本次跨越的帧数
        self.window_clock = current_clock  # 记录
        return interval_clock  # 返回间隔时间

    def window_start(self):
        gu.window = self
        self.window_run = True
        wndclass = fill_structure(
            WndClassEx, size=ctypes.sizeof(WndClassEx), style=3,
            wndproc=WNDPROC(self.prepare_event_function()),
            class_name="GuWindow", background=GetStockObject(4))
        RegisterClass(ctypes.byref(wndclass))
        """CS_HREDRAW = 2
        CS_VREDRAW = 1
        WS_EX_OVERLAPPEDWINDOW = 768
        WS_OVERLAPPEDWINDOW = 13565952
        WS_VISIBLE = 268435456
        WS_THICKFRAME = 262144
        CW_USEDEFAULT = -2147483648"""
        hwnd = CreateWindow(
            768, "GuWindow", self.window_title, 282001408, -2147483648,
            -2147483648, *self.window_size, None, None, None, None)
        UpdateWindow(hwnd)
        hdc = GetDC(hwnd)
        pfd = ctypes.byref(fill_structure(
            PixelFormatDescriptor, size=40, version=1, flags=37,
            color_bits=GetDeviceCaps(hdc, 12), depth_bits=24, stencil_bits=8))
        pf = ChoosePixelFormat(hdc, pfd)
        SetPixelFormat(hdc, pf, pfd)
        wglMakeCurrent(hdc, wglCreateContext(hdc))

        self.window_gl_init()
        msg = ctypes.byref(MSG())
        while self.window_run:
            interval = self.sleep_time()
            self.sync_pull()
            self.window_gl_clear()
            self.window_gl_render(interval)
            wglSwapBuffers(wglGetCurrentDC())
            while PeekMessage(msg, hwnd, 0, 0, 1):
                TranslateMessage(msg)
                DispatchMessage(msg)

    def window_stop(self):
        self.window_run = False
