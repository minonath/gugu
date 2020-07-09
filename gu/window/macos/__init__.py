import ctypes
import time

from ._objc_runtime import Id
from ._objc_library import OBJC, FIT, STR, SEL, SUBCLASS, BIND, FIND
from ..base import window_input, gl_context, WindowPrototype

NSOpenGLPFAAllRenderer = 1
NSOpenGLPFADoubleBuffer = 5
NSOpenGLPFADepthSize = 12
NSOpenGLPFAMaximumPolicy = 52
NSOpenGLPFASampleBuffers = 55
NSOpenGLPFASamples = 56
NSOpenGLPFAOpenGLProfile = 99
NSOpenGLProfileVersionLegacy = 0x1000
NSOpenGLProfileVersion3_2Core = 0x3200
NSOpenGLProfileVersion4_1Core = 0x4100
NSOpenGLCPSwapInterval = 222

NSBackingStoreBuffered = 2
NSAnyEventMask = 0xFFFFFFFF

APP_KIT = ctypes.cdll.LoadLibrary(
    '/System/Library/Frameworks/AppKit.framework/AppKit'
)

NSDefaultRunLoopMode = Id.in_dll(APP_KIT, 'NSDefaultRunLoopMode')
NSApplicationDidShowNotification = Id.in_dll(
    APP_KIT, 'NSApplicationDidUn''hideNotification'
)

NSWindowMaskTitle = 1 << 0
NSWindowMaskClose = 1 << 1
NSWindowMaskMiniaturize = 1 << 2
NSWindowMaskResize = 1 << 3

WINDOW_STYLE = (
        NSWindowMaskTitle | NSWindowMaskClose |
        NSWindowMaskMiniaturize | NSWindowMaskResize
)

NSTrackingMouseEnteredAndExited = 0x01
NSTrackingMouseMoved = 0x02
NSTrackingCursorUpdate = 0x04
NSTrackingActiveWhenFirstResponder = 0x10
NSTrackingActiveInKeyWindow = 0x20
NSTrackingActiveInActiveApp = 0x40
NSTrackingActiveAlways = 0x80
NSTrackingAssumeInside = 0x100
NSTrackingInVisibleRect = 0x200
NSTrackingEnabledDuringMouseDrag = 0x400

TRACKING_OPTION = (
        NSTrackingMouseEnteredAndExited |  # 鼠标进出检测。
        NSTrackingMouseMoved |  # 鼠标移动检测。
        NSTrackingCursorUpdate |  # 鼠标移动检测。
        NSTrackingActiveInActiveApp  # 激活检测。
)


NSEventTypeKeyDown = 10
NSEventTypeKeyUp = 11
NSEventTypeFlagsChanged = 12


def ignore_error():
    # 创建窗口会导致报错，这里取消这个错误检测
    # ApplePersistenceIgnoreState:
    # Existing state will not be touched.
    # New state will be written to (null)

    user_defaults = OBJC('NSUserDefaults', 'standardUserDefaults')
    ignore_state = STR('ApplePersistenceIgnoreState')
    if OBJC(user_defaults, 'objectForKey:', ignore_state):
        OBJC(user_defaults, 'setBool:forKey:', False, ignore_state)


def max_size():
    frame_rect = OBJC(OBJC('NSScreen', 'mainScreen'), 'visibleFrame')

    # frame rect 是指窗口大小，content rect 是绘制区域的大小
    content_rect = OBJC('NSWindow', 'contentRectForFrameRect:styleMask:',
                        frame_rect, WINDOW_STYLE)

    return content_rect.mem_1.mem_0, content_rect.mem_1.mem_1  # 宽和高


class Window(WindowPrototype):
    def __init__(self):
        WindowPrototype.__init__(self)

        self._prepare = False  # 用于判断是否需要重新创建相关子类。
        self._app = None
        self._window = None
        self._delegate = None
        self._view = None
        self._tracking_area = None

    def _window_start(self):
        width, height = self.window_size
        if width == 0 or height == 0:
            width, height = max_size()

        pool = OBJC(OBJC('NSAutoreleasePool', 'alloc'), 'init')
        self._app = OBJC('NSApplication', 'sharedApplication')
        OBJC(self._app, 'setActivationPolicy:', 0)
        ignore_error()

        if not OBJC(self._app, 'isRunning'):
            for _ in range(self.window_queue.qsize()):  # 清空队列。
                self.window_queue.get_nowait()

            self._prepare_objc_class()
            self._create_menu()

            context = self._create_window(self.window_title, width, height)
            self._finish_launch()

            self._init_mouse_position()
            gl_context.prepare()
            gl_context.gl_init()
            self.window_running = True
            self.window_clock = time.perf_counter()  # 记录启动时间。
            self._prepare = True  # 不需要重复加载。

            try:
                while self.window_running:
                    interval = self._window_sleep()  # 上一帧的运行时间。
                    OBJC(context, 'makeCurrentContext')
                    self._window_pull()
                    gl_context.gl_clear()
                    gl_context.gl_render(interval)
                    OBJC(context, 'flushBuffer')
                    self._app_event_hook()
                    OBJC(self._app, 'updateWindows')
            except KeyboardInterrupt:  # 防止 Ctrl-C 打断后无法回收，主动退出。
                pass

            self._delete_tracking_area()
            OBJC('NSOpenGLContext', 'clearCurrentContext')
            OBJC(self._view, 'release')
            OBJC(self._delegate, 'release')

        OBJC(pool, 'drain')

    def _prepare_objc_class(self):
        """ 准备好需要的 ObjC 类 """
        if self._prepare:
            return

        window_cls = SUBCLASS('GuWindow', 'NSWindow')
        view_cls = SUBCLASS('GuView', 'NSView')
        delegate_cls = SUBCLASS('GuDelegate', 'NSObject')

        @BIND(window_cls, 'canBecomeKeyWindow', 'B16@0:8')
        @BIND(window_cls, 'canBecomeMainWindow', 'B16@0:8')
        @BIND(view_cls, 'isOpaque', 'B16@0:8')
        # @BIND(view_cls, 'canBecomeKeyView', 'B16@0:8')  大概不需要这个。
        def do(cls, sel):
            return True

        @BIND(view_cls, 'updateTrackingAreas', 'v16@0:8')
        def do(cls, sel):
            """
            当窗口 resize 的时候，会自动调用这个函数，需要手动重建 TrackingArea。
            如果不主动替换，鼠标检测时，会在系统消息里进行一次报错（用户不可见）。
            之后会有相应的纠错，但是需要一些时间。
            """
            self._delete_tracking_area()
            self._create_tracking_area()

        @BIND(view_cls, 'cursorUpdate:', 'v24@0:8@16')
        @BIND(view_cls, 'mouseEntered:', 'v24@0:8@16')
        def do(cls, sel, notification):
            position = OBJC(self._view, 'convertPoint:fromView:',
                            OBJC(notification, 'locationInWindow'), None)
            self.window_queue.put(
                (window_input.mouse_enter, position.mem_0, position.mem_1)
            )
            window_input.mouse_x, window_input.mouse_x = (
                position.mem_0, position.mem_1
            )  # 鼠标进入时重新定位。

        @BIND(view_cls, 'mouseExited:', 'v24@0:8@16')
        def do(cls, sel, notification):
            position = OBJC(self._view, 'convertPoint:fromView:',
                            OBJC(notification, 'locationInWindow'), None)
            self.window_queue.put(
                (window_input.mouse_exit, position.mem_0, position.mem_1)
            )

        @BIND(view_cls, 'mouseMoved:', 'v24@0:8@16')
        def do(cls, sel, notification):
            position = OBJC(self._view, 'convertPoint:fromView:',
                            OBJC(notification, 'locationInWindow'), None)
            delta_x = position.mem_0 - window_input.mouse_x
            delta_y = position.mem_1 - window_input.mouse_y
            self.window_queue.put(
                (window_input.mouse_move, delta_x, delta_y)
            )
            window_input.mouse_x, window_input.mouse_y = (
                position.mem_0, position.mem_1
            )

        @BIND(view_cls, 'scrollWheel:', 'v24@0:8@16')
        def do(cls, sel, notification):  # 鼠标用不到纵向，但是触控板会检测横向。
            delta_x = int(OBJC(notification, 'deltaX'))  # 横向
            delta_y = -int(OBJC(notification, 'deltaY'))  # 纵向
            if delta_x or delta_y:  # 触控板会误触这个事件，这里排除误触。
                self.window_queue.put(
                    (window_input.mouse_scroll_wheel, delta_x, delta_y)
                )

        @BIND(view_cls, 'mouseDown:', 'v24@0:8@16')
        def do(cls, sel, notification):
            position = OBJC(self._view, 'convertPoint:fromView:',
                            OBJC(notification, 'locationInWindow'), None)
            self.window_queue.put(
                (window_input.mouse_down, position.mem_0, position.mem_1)
            )

        @BIND(view_cls, 'mouseDragged:', 'v24@0:8@16')
        def do(cls, sel, notification):
            position = OBJC(self._view, 'convertPoint:fromView:',
                            OBJC(notification, 'locationInWindow'), None)
            self.window_queue.put((
                window_input.mouse_dragged,
                position.mem_0 - window_input.mouse_x,
                position.mem_1 - window_input.mouse_y
            ))
            window_input.mouse_x, window_input.mouse_y = (
                position.mem_0, position.mem_1
            )

        @BIND(view_cls, 'mouseUp:', 'v24@0:8@16')
        def do(cls, sel, notification):
            position = OBJC(self._view, 'convertPoint:fromView:',
                            OBJC(notification, 'locationInWindow'), None)
            self.window_queue.put(
                (window_input.mouse_up, position.mem_0, position.mem_1)
            )

        @BIND(view_cls, 'rightMouseDown:', 'v24@0:8@16')
        def do(cls, sel, notification):
            position = OBJC(self._view, 'convertPoint:fromView:',
                            OBJC(notification, 'locationInWindow'), None)
            self.window_queue.put(
                (window_input.right_down, position.mem_0, position.mem_1)
            )

        @BIND(view_cls, 'rightMouseDragged:', 'v24@0:8@16')
        def do(cls, sel, notification):
            position = OBJC(self._view, 'convertPoint:fromView:',
                            OBJC(notification, 'locationInWindow'), None)
            self.window_queue.put(
                (window_input.right_dragged, position.mem_0, position.mem_1)
            )

        @BIND(view_cls, 'rightMouseUp:', 'v24@0:8@16')
        def do(cls, sel, notification):
            position = OBJC(self._view, 'convertPoint:fromView:',
                            OBJC(notification, 'locationInWindow'), None)
            self.window_queue.put(
                (window_input.right_up, position.mem_0, position.mem_1)
            )

        @BIND(view_cls, 'otherMouseDown:', 'v24@0:8@16')
        def do(cls, sel, notification):
            position = OBJC(self._view, 'convertPoint:fromView:',
                            OBJC(notification, 'locationInWindow'), None)
            self.window_queue.put(
                (window_input.other_down, position.mem_0, position.mem_1)
            )

        @BIND(view_cls, 'otherMouseDragged:', 'v24@0:8@16')
        def do(cls, sel, notification):
            position = OBJC(self._view, 'convertPoint:fromView:',
                            OBJC(notification, 'locationInWindow'), None)
            self.window_queue.put(
                (window_input.other_dragged, position.mem_0, position.mem_1)
            )

        @BIND(view_cls, 'otherMouseUp:', 'v24@0:8@16')
        def do(cls, sel, notification):
            position = OBJC(self._view, 'convertPoint:fromView:',
                            OBJC(notification, 'locationInWindow'), None)
            self.window_queue.put(
                (window_input.other_up, position.mem_0, position.mem_1)
            )

        @BIND(delegate_cls, 'windowShouldClose:', 'B24@0:8@16')
        def do(cls, sel, notification):  # 参数是 Delegate类，SEL，消息。
            self.window_running = False
            return True

        @BIND(delegate_cls, 'windowWillStartLiveResize:', 'B24@0:8@16')
        def do(cls, sel, notification):
            self._delete_tracking_area()

        @BIND(delegate_cls, 'windowDidEndLiveResize:', 'B24@0:8@16')
        def do(cls, sel, notification):
            self._create_tracking_area()
            area = OBJC(self._view, 'bounds')
            self.window_queue.put(
                (window_input.resize, area.mem_1.mem_0, area.mem_1.mem_1)
            )

        @BIND(delegate_cls, 'windowWillMiniaturize:', 'B24@0:8@16')
        def do(cls, sel, notification):
            # NSApplication setDelegate: 无法设置 Application 的代理。
            # 现在将 GuDelegate windowWillMiniaturize NSApplication hide: 绑定，
            # 使 App 仅有一个窗口，这种情况下，可以借用 UnHide 指令。
            OBJC(self._app, 'hide:', None)

        @BIND(delegate_cls, 'applicationDidShow:', 'B24@0:8@16')
        def do(cls, sel, notification):
            OBJC(self._window, 'makeKeyAndOrderFront:', None)

    def _create_tracking_area(self):
        # 获取窗口的尺寸，提供给 TrackingArea 使用。
        area = OBJC(self._view, 'bounds')  # 这里也许应该用 frame? bounds?
        # 鼠标触碰检测，如果不设置这个，当窗口 resize 的时候，鼠标会按不到键。
        # 如果窗口位置进行了变动，tracking_area 必须重建。
        tracking_area = OBJC('NSTrackingArea', 'alloc')
        OBJC(tracking_area, 'initWithRect:options:owner:userInfo:',
             area, TRACKING_OPTION, self._view, None)
        OBJC(self._view, 'addTrackingArea:', tracking_area)  # 设置鼠标触碰。
        self._tracking_area = tracking_area

    def _delete_tracking_area(self):
        """ 删除原有 TrackingArea """
        OBJC(self._view, 'removeTrackingArea:', self._tracking_area)
        OBJC(self._tracking_area, 'release')

    def _create_menu(self):
        if self._prepare:
            return

        menu = OBJC(OBJC('NSMenu', 'alloc'), 'init')
        OBJC(menu, 'addItem:',
             OBJC(OBJC('NSMenuItem', 'alloc'),
                  'initWithTitle:action:keyEquivalent:',
                  STR('hide'), SEL('hide:'), STR('h')))
        OBJC(menu, 'addItem:', OBJC('NSMenuItem', 'separatorItem'))
        OBJC(menu, 'addItem:',
             OBJC(OBJC('NSMenuItem', 'alloc'),
                  'initWithTitle:action:keyEquivalent:',
                  STR('quit'), SEL('terminate:'), STR('q')))
        bar = OBJC(OBJC('NSMenu', 'alloc'), 'init')
        item = OBJC(OBJC('NSMenuItem', 'alloc'), 'init')
        OBJC(item, 'setSubmenu:', menu)
        OBJC(bar, 'addItem:', item)
        OBJC(self._app, 'setMainMenu:', bar)
        OBJC(menu, 'release')
        OBJC(item, 'release')
        OBJC(bar, 'release')

    def _create_window(self, title, width, height):
        # 创建窗口。
        window = FIT(  # 建立一个窗口。
            OBJC('GuWindow', 'alloc'),
            'initWithContentRect:styleMask:backing:defer:',
            (0, 0, width, height), WINDOW_STYLE,
            NSBackingStoreBuffered, False
        )
        OBJC(window, 'setTitle:', STR(title))
        self._window = window

        # 创建代理。
        delegate_obj = OBJC(OBJC('GuDelegate', 'alloc'), 'init')
        notification_center = OBJC('NSNotificationCenter', 'defaultCenter')
        OBJC(notification_center, 'addObserver:selector:name:object:',
             delegate_obj, SEL('applicationDidShow:'),
             NSApplicationDidShowNotification, None)
        OBJC(window, 'setDelegate:', delegate_obj)
        self._delegate = delegate_obj

        # 创建视口。
        area = OBJC(window, 'frame')  # 获取窗口的尺寸，提供给 View 使用。
        view = OBJC(OBJC('GuView', 'alloc'), 'initWithFrame:', area)
        OBJC(window, 'setContentView:', view)  # 设置 View 为内容。
        OBJC(window, 'makeFirstResponder:', view)  # 设置为第一响应。
        self._view = view

        # 创建鼠标区域。
        self._create_tracking_area()

        # 创建显卡缓冲区。
        pixel_format_attributes = [
            NSOpenGLPFADoubleBuffer, NSOpenGLPFASampleBuffers, 1,
            NSOpenGLPFASamples, 4, NSOpenGLPFADepthSize, 24,
            NSOpenGLPFAAllRenderer, NSOpenGLPFAMaximumPolicy,
            NSOpenGLPFAOpenGLProfile, NSOpenGLProfileVersion4_1Core, 0x00
        ]  # 最后一位 0x00 是结束符号。

        pfa = (ctypes.c_uint32 * len(pixel_format_attributes))(
            *pixel_format_attributes)

        pixel_format = OBJC(
            OBJC('NSOpenGLPixelFormat', 'alloc'), 'initWithAttributes:', pfa
        )

        context = OBJC(
            OBJC('NSOpenGLContext', 'alloc'),
            'initWithFormat:shareContext:',
            pixel_format, None
        )

        OBJC(context, 'setView:', view)
        OBJC(context, 'makeCurrentContext')
        OBJC(context, 'setValues:forParameter:',
             ctypes.c_int(1), NSOpenGLCPSwapInterval)
        OBJC(context, 'update')  # 不进行 update 会有的原本的 context 一闪而过。
        return context

    def _finish_launch(self):
        # 窗口如果接受鼠标事件，就会重复 View 的鼠标事件。
        OBJC(self._window, 'setAcceptsMouseMovedEvents:', False)
        OBJC(self._window, 'setReleasedWhenClosed:', True)  # 关闭时回收。
        OBJC(self._window, 'useOptimizedDrawing:', False)  # 不需专心绘制 View 。
        # 改变尺寸时不保留内容。
        OBJC(self._window, 'setPreservesContentDuringLiveResize:', False)

        OBJC(self._window, 'orderOut:', None)  # 设置为关键窗口。
        OBJC(self._window, 'makeKeyAndOrderFront:', self._window)
        OBJC(self._window, 'center')  # 注意，设置 center 后区域会改变。

        if not self._prepare:  # 不知道重复使用 finishLaunching 会有什么不良影响。
            OBJC(self._app, 'finishLaunching')
        OBJC(self._app, 'activateIgnoringOtherApps:', True)

    def _init_mouse_position(self):  # 第一次获取鼠标位置。
        mouse_pos = OBJC('NSEvent', 'mouseLocation')
        window_pos = OBJC(self._window, 'frame').mem_0
        mouse_pos.mem_0 -= window_pos.mem_0
        mouse_pos.mem_1 -= window_pos.mem_1
        mouse_pos = OBJC(self._view, 'convertPoint:fromView:',
                         mouse_pos, None)
        window_input.mouse_x, window_input.mouse_y =(
            mouse_pos.mem_0, mouse_pos.mem_1
        )

    def _app_event_hook(self):
        while True:
            event = OBJC(
                self._app, 'nextEventMatchingMask:untilDate:inMode:dequeue:',
                NSAnyEventMask, OBJC('NSDate', 'distantPast'),
                NSDefaultRunLoopMode, True)

            if not event:
                break

            event_type = OBJC(event, 'type')
            OBJC(self._app, 'sendEvent:', event)

            if ((event_type == NSEventTypeKeyDown and
                 not OBJC(event, 'isARepeat')) or
                    event_type == NSEventTypeKeyUp or
                    event_type == NSEventTypeFlagsChanged):
                self.window_queue.put(
                    (window_input.key_input, OBJC(event, 'keyCode'))
                )

    def _window_set_title(self):
        def _inner_thread():
            OBJC(self._window, 'setTitle:', STR(self.window_title))

        self.window_queue.put(
            (_inner_thread, )
        )  # app 相关函数需要在主线程里运行。

    def _window_set_image(self):
        raise NotImplementedError

    def _window_set_size(self):
        def _inner_thread():
            area = OBJC(self._window, 'frame')
            w = area.mem_1.mem_0
            h = area.mem_1.mem_1
            w1, h1 = self.window_size
            w2, h2 = (w1 - w) // 2, (h1 - h) // 2
            x = area.mem_0.mem_0 - w2
            y = area.mem_0.mem_1 - h2
            FIT(self._window, 'setFrame:display:', (x, y, w1, h1), False)
            self._delete_tracking_area()
            self._create_tracking_area()

        self.window_queue.put(
            (_inner_thread, )
        )  # app 相关函数需要在主线程里运行。
