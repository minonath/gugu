import ctypes
import time
from ._objc_library import OBJC, FIT, STR, SEL, SUBCLASS, BIND
from ._objc_runtime import Id

from gu.system import gu
from gu.window._window_prototype import WindowPrototype


def debug_area(area):
    print('Origin({}, {}), Size({}, {})'.format(
        area.mem_0.mem_0, area.mem_0.mem_1,
        area.mem_1.mem_0, area.mem_1.mem_1,
    ))


NSOpenGLPFAAllRenderer = 1
NSOpenGLPFADoubleBuffer = 5
NSOpenGLPFADepthSize = 12
NSOpenGLPFAMaximumPolicy = 52
NSOpenGLPFASampleBuffers = 55
NSOpenGLPFASamples = 56
NSOpenGLPFAOpenGLProfile = 99
# NSOpenGLProfileVersionLegacy = 0x1000
# NSOpenGLProfileVersion3_2Core = 0x3200
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

WINDOW_STYLE = (NSWindowMaskTitle | NSWindowMaskClose |
                NSWindowMaskMiniaturize | NSWindowMaskResize)

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

TRACKING_OPTION = (NSTrackingMouseEnteredAndExited |  # 鼠标进出检测
                   NSTrackingMouseMoved |  # 鼠标移动检测
                   NSTrackingCursorUpdate |  # 鼠标移动检测
                   NSTrackingActiveInActiveApp  # 激活检测
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


def default_max_size():
    frame_rect = OBJC(OBJC('NSScreen', 'mainScreen'), 'visibleFrame')

    # frame rect 是指窗口大小，content rect 是绘制区域的大小
    content_rect = OBJC('NSWindow', 'contentRectForFrameRect:styleMask:',
                        frame_rect, WINDOW_STYLE)

    return content_rect.mem_1.mem_0, content_rect.mem_1.mem_1  # 宽和高


class MacWindow(WindowPrototype):
    def __init__(self, title='Gu', size=None, fps=30):
        if not size:  # 如果没有设置尺寸，以（非全屏）最大窗口创建。
            size = default_max_size()

        WindowPrototype.__init__(self, title, size, fps)
        self.window_run = False
        self.window_clock = time.perf_counter()

        self.window_app = None
        self.window_window = None
        self.window_view = None
        self.window_tracking = None

    def prepare_objc_class(self):
        window_cls = SUBCLASS('GuWindow', 'NSWindow')
        view_cls = SUBCLASS('GuView', 'NSView')
        delegate_cls = SUBCLASS('GuDelegate', 'NSObject')

        @BIND(window_cls, 'canBecomeKeyWindow', 'B16@0:8')
        @BIND(view_cls, 'isOpaque', 'B16@0:8')
        # @BIND(view_cls, 'canBecomeKeyView', 'B16@0:8')
        def do(cls, sel):
            return True

        @BIND(view_cls, 'updateTrackingAreas', 'v16@0:8')
        def do(cls, sel):
            """
            当窗口 resize 的时候，会自动调用这个函数，需要手动重建 TrackingArea
            如果不主动替换，鼠标检测时，会在系统消息里进行一次报错（用户不可见）
            之后会有相应的纠错，但是需要一些时间
            """
            self.delete_tracking_area()
            self.create_tracking_area()

        @BIND(view_cls, 'cursorUpdate:', 'v24@0:8@16')
        @BIND(view_cls, 'mouseEntered:', 'v24@0:8@16')
        def do(cls, sel, notification):
            position = OBJC(self.window_view, 'convertPoint:fromView:',
                            OBJC(notification, 'locationInWindow'), None)
            # 鼠标进入时重新定位
            self.mouse_x, self.mouse_y = position.mem_0, position.mem_1
            self.sync_push(self.mouse_enter, self.mouse_x, self.mouse_y)

        @BIND(view_cls, 'mouseExited:', 'v24@0:8@16')
        def do(cls, sel, notification):
            position = OBJC(self.window_view, 'convertPoint:fromView:',
                            OBJC(notification, 'locationInWindow'), None)
            self.sync_push(self.mouse_exit, position.mem_0, position.mem_1)

        @BIND(view_cls, 'mouseMoved:', 'v24@0:8@16')
        def do(cls, sel, notification):
            position = OBJC(self.window_view, 'convertPoint:fromView:',
                            OBJC(notification, 'locationInWindow'), None)
            delta_x = position.mem_0 - self.mouse_x
            delta_y = position.mem_1 - self.mouse_y
            self.sync_push(self.mouse_move, delta_x, delta_y)
            self.mouse_x, self.mouse_y = position.mem_0, position.mem_1

        @BIND(view_cls, 'scrollWheel:', 'v24@0:8@16')
        def do(cls, sel, notification):  # 一般鼠标用不到纵向，但是触控板会检测横向
            delta_x = int(OBJC(notification, 'deltaX'))  # 横向
            delta_y = -int(OBJC(notification, 'deltaY'))  # 纵向
            if delta_x or delta_y:  # 触控板会误触这个事件，这里排除误触
                self.sync_push(self.mouse_scroll_wheel, delta_x, delta_y)

        @BIND(view_cls, 'mouseDown:', 'v24@0:8@16')
        def do(cls, sel, notification):
            position = OBJC(self.window_view, 'convertPoint:fromView:',
                            OBJC(notification, 'locationInWindow'), None)
            self.sync_push(self.mouse_down, position.mem_0, position.mem_1)

        @BIND(view_cls, 'mouseDragged:', 'v24@0:8@16')
        def do(cls, sel, notification):
            position = OBJC(self.window_view, 'convertPoint:fromView:',
                            OBJC(notification, 'locationInWindow'), None)
            self.sync_push(self.mouse_dragged, position.mem_0 - self.mouse_x,
                           position.mem_1 - self.mouse_y)
            self.mouse_x, self.mouse_y = position.mem_0, position.mem_1

        @BIND(view_cls, 'mouseUp:', 'v24@0:8@16')
        def do(cls, sel, notification):
            position = OBJC(self.window_view, 'convertPoint:fromView:',
                            OBJC(notification, 'locationInWindow'), None)
            self.sync_push(self.mouse_up, position.mem_0, position.mem_1)

        @BIND(view_cls, 'rightMouseDown:', 'v24@0:8@16')
        def do(cls, sel, notification):
            position = OBJC(self.window_view, 'convertPoint:fromView:',
                            OBJC(notification, 'locationInWindow'), None)
            self.sync_push(
                self.mouse_right_down, position.mem_0, position.mem_1)

        @BIND(view_cls, 'rightMouseDragged:', 'v24@0:8@16')
        def do(cls, sel, notification):
            position = OBJC(self.window_view, 'convertPoint:fromView:',
                            OBJC(notification, 'locationInWindow'), None)
            self.sync_push(
                self.mouse_right_dragged, position.mem_0, position.mem_1)

        @BIND(view_cls, 'rightMouseUp:', 'v24@0:8@16')
        def do(cls, sel, notification):
            position = OBJC(self.window_view, 'convertPoint:fromView:',
                            OBJC(notification, 'locationInWindow'), None)
            self.sync_push(
                self.mouse_right_up, position.mem_0, position.mem_1)

        @BIND(view_cls, 'otherMouseDown:', 'v24@0:8@16')
        def do(cls, sel, notification):
            position = OBJC(self.window_view, 'convertPoint:fromView:',
                            OBJC(notification, 'locationInWindow'), None)
            self.sync_push(
                self.mouse_other_down, position.mem_0, position.mem_1)

        @BIND(view_cls, 'otherMouseDragged:', 'v24@0:8@16')
        def do(cls, sel, notification):
            position = OBJC(self.window_view, 'convertPoint:fromView:',
                            OBJC(notification, 'locationInWindow'), None)
            self.sync_push(
                self.mouse_other_dragged, position.mem_0, position.mem_1)

        @BIND(view_cls, 'otherMouseUp:', 'v24@0:8@16')
        def do(cls, sel, notification):
            position = OBJC(self.window_view, 'convertPoint:fromView:',
                            OBJC(notification, 'locationInWindow'), None)
            self.sync_push(
                self.mouse_other_up, position.mem_0, position.mem_1)

        @BIND(delegate_cls, 'windowShouldClose:', 'B24@0:8@16')
        def do(cls, sel, notification):  # 参数是 Delegate类，SEL，消息
            restype = self.window_stop()
            return True if restype is None else restype  # 把 None 当做 True

        @BIND(delegate_cls, 'windowWillStartLiveResize:', 'B24@0:8@16')
        def do(cls, sel, notification):
            self.delete_tracking_area()

        @BIND(delegate_cls, 'windowDidEndLiveResize:', 'B24@0:8@16')
        def do(cls, sel, notification):
            self.create_tracking_area()
            area = OBJC(self.window_view, 'bounds')
            self.sync_push(self.window_resize, area.mem_1.mem_0,
                           area.mem_1.mem_1)

        @BIND(delegate_cls, 'windowWillMiniaturize:', 'B24@0:8@16')
        def do(cls, sel, notification):
            OBJC(self.window_app, 'hide:', None)

        @BIND(delegate_cls, 'applicationDidShow:', 'B24@0:8@16')
        def do(cls, sel, notification):
            OBJC(self.window_window, 'makeKeyAndOrderFront:', None)

        # NSApplication setDelegate: 无法设置 Application 的代理
        # 不知道是不是和 windowDelegate 混在一起导致了一些错误
        # 现在将 GuDelegate windowWillMiniaturize NSApplication hide: 绑定
        # 使 App 仅有一个窗口，这种情况下，可以借用 UnHide 指令
        # @BIND(delegate_cls, 'applicationShouldHandleReopen:'
        #                     'hasVisibleWindows:', 'B28@0:8@16B24')
        # def do(cls, sel, app, flag):
        #     print('applicationShouldHandleReopen')

    def create_menu(self):
        # 简单的添加目录，这是个雏形，后面还要做通过参数创造目录栏
        # OBJC(self._window_app, 'mainMenu')
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
        OBJC(self.window_app, 'setMainMenu:', bar)

        OBJC(menu, 'release')
        OBJC(item, 'release')
        OBJC(bar, 'release')

    def create_window(self):
        # 建立一个窗口
        window = FIT(
            OBJC('GuWindow', 'alloc'),
            'initWithContentRect:styleMask:backing:defer:',
            (0, 0) + self.window_size, WINDOW_STYLE,
            NSBackingStoreBuffered, False
        )
        OBJC(window, 'setTitle:', STR(self.window_title))

        delegate_obj = OBJC(OBJC('GuDelegate', 'alloc'), 'init')
        notification_center = OBJC('NSNotificationCenter', 'defaultCenter')
        OBJC(notification_center, 'addObserver:selector:name:object:',
             delegate_obj, SEL('applicationDidShow:'),
             NSApplicationDidShowNotification, None)
        OBJC(window, 'setDelegate:', delegate_obj)

        self.window_window = window

    def create_view(self):
        # 获取窗口的尺寸，提供给 View 使用
        area = OBJC(self.window_window, 'frame')

        view = OBJC(OBJC('GuView', 'alloc'), 'initWithFrame:', area)
        OBJC(self.window_window, 'setContentView:', view)  # 设置 View 为内容
        OBJC(self.window_window, 'makeFirstResponder:', view)  # 设置为第一响应

        self.window_view = view

    def create_tracking_area(self):
        view = self.window_view  # OBJC(self.window_window, 'contentView')
        # 获取窗口的尺寸，提供给 TrackingArea 使用
        area = OBJC(view, 'bounds')  # 这里也许应该用 frame? bounds?

        # 鼠标触碰检测，如果不设置这个，当窗口 resize 的时候，鼠标会按不到键
        # 如果窗口位置进行了变动，tracking_area 必须重建
        tracking_area = OBJC('NSTrackingArea', 'alloc')
        OBJC(tracking_area, 'initWithRect:options:owner:userInfo:',
             area, TRACKING_OPTION, view, None)
        OBJC(view, 'addTrackingArea:', tracking_area)  # 设置鼠标触碰

        self.window_tracking = tracking_area

    def delete_tracking_area(self):
        # 删除原有 TrackingArea
        OBJC(self.window_view, 'removeTrackingArea:', self.window_tracking)
        OBJC(self.window_tracking, 'release')

    def create_context(self):
        pixel_format_attributes = [
            NSOpenGLPFADoubleBuffer, NSOpenGLPFASampleBuffers, 1,
            NSOpenGLPFASamples, 4, NSOpenGLPFADepthSize, 24,
            NSOpenGLPFAAllRenderer, NSOpenGLPFAMaximumPolicy,
            NSOpenGLPFAOpenGLProfile, NSOpenGLProfileVersion4_1Core, 0x00
        ]  # 最后一位 0x00 是结束符号

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

        OBJC(context, 'setView:', self.window_view)
        OBJC(self.window_view, 'setWantsBestResolutionOpenGLSurface:', 1)
        OBJC(context, 'makeCurrentContext')
        OBJC(context, 'setValues:forParameter:',
             ctypes.c_int(1), NSOpenGLCPSwapInterval)
        OBJC(context, 'update')  # 不进行 update 会有的原本的 context 一闪而过

        return context

    def finish_launch(self):
        window = self.window_window

        # 窗口如果接受鼠标事件，就会重复 View 的鼠标事件
        OBJC(window, 'setAcceptsMouseMovedEvents:', False)  # 不接受鼠标移动事件
        OBJC(window, 'setReleasedWhenClosed:', True)  # 关闭时回收
        OBJC(window, 'useOptimizedDrawing:', False)  # 不需要专心绘制 View
        # 改变尺寸时不保留内容
        OBJC(window, 'setPreservesContentDuringLiveResize:', False)

        OBJC(window, 'orderOut:', None)  # 设置为关键窗口
        OBJC(window, 'makeKeyAndOrderFront:', window)  # 设置为关键窗口

        OBJC(window, 'center')  # 注意，设置 center 后区域会改变

        OBJC(self.window_app, 'finishLaunching')
        OBJC(self.window_app, 'activateIgnoringOtherApps:', True)

    def get_mouse_position(self):
        mouse_pos = OBJC('NSEvent', 'mouseLocation')
        window_pos = OBJC(self.window_window, 'frame').mem_0
        mouse_pos.mem_0 -= window_pos.mem_0
        mouse_pos.mem_1 -= window_pos.mem_1
        mouse_pos = OBJC(self.window_view, 'convertPoint:fromView:',
                         mouse_pos, None)
        self.mouse_x = mouse_pos.mem_0
        self.mouse_y = mouse_pos.mem_1

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

    def handle_event(self):
        app = self.window_app

        while True:
            event = OBJC(
                app, 'nextEventMatchingMask:untilDate:inMode:dequeue:',
                NSAnyEventMask, OBJC('NSDate', 'distantPast'),
                NSDefaultRunLoopMode, True)

            if not event:
                break

            event_type = OBJC(event, 'type')
            OBJC(app, 'sendEvent:', event)

            if ((event_type == NSEventTypeKeyDown and
                 not OBJC(event, 'isARepeat')) or
                    event_type == NSEventTypeKeyUp or
                    event_type == NSEventTypeFlagsChanged):
                gu.keyboard(OBJC(event, 'keyCode'))

    def window_start(self):
        gu.window = self
        self.window_run = True

        pool = OBJC(OBJC('NSAutoreleasePool', 'alloc'), 'init')
        self.window_app = OBJC('NSApplication', 'sharedApplication')
        OBJC(self.window_app, 'setActivationPolicy:', 0)

        ignore_error()

        if not OBJC(self.window_app, 'isRunning'):
            self.prepare_objc_class()
            self.create_menu()
            self.create_window()
            self.create_view()
            self.create_tracking_area()
            context = self.create_context()
            self.finish_launch()
            self.get_mouse_position()

            self.window_gl_init()
            while self.window_run:
                interval = self.sleep_time()  # 上一帧的运行时间
                OBJC(context, 'makeCurrentContext')
                self.sync_pull()
                self.window_gl_clear()
                self.window_gl_render(interval)
                OBJC(context, 'flushBuffer')
                self.handle_event()
                OBJC(self.window_app, 'updateWindows')

            OBJC('NSOpenGLContext', 'clearCurrentContext')

        OBJC(pool, 'drain')

    def window_stop(self):
        self.window_run = False
        # 这里需要一个返回值，通知系统是否关闭整个程序
        # 没有返回值也会关闭，因为我在检测那里把 None 也当成 True 了
        return True

    def window_set_title(self, title):
        self.window_title = title
        if self.window_window:
            OBJC(self.window_window, 'setTitle:', STR(title))
