import ctypes
import time

from ._base_window import window_input, WindowPrototype
from ..graphic import gl_context
from ..macos import (
    OBJC, STR, WINDOW_STYLE, SUBCLASS, BIND, TRACKING_OPTION, SEL, FIT,
    NSBackingStoreBuffered, NSApplicationDidShowNotification,
    NSOpenGLPFADoubleBuffer, NSOpenGLPFASampleBuffers, NSOpenGLPFASamples,
    NSOpenGLPFADepthSize, NSOpenGLPFAAllRenderer, NSOpenGLPFAMaximumPolicy,
    NSOpenGLPFAOpenGLProfile, NSOpenGLProfileVersion4_1Core,
    NSOpenGLCPSwapInterval, NSAnyEventMask, NSDefaultRunLoopMode,
    NSEventTypeKeyDown, NSEventTypeKeyUp, NSEventTypeFlagsChanged
)


def _ignore_error():
    # 创建窗口会导致报错，这里取消这个错误检测
    # ApplePersistenceIgnoreState:
    # Existing state will not be touched.
    # New state will be written to (null)

    _user_defaults = OBJC('NSUserDefaults', 'standardUserDefaults')
    _ignore_state = STR('ApplePersistenceIgnoreState')
    if OBJC(_user_defaults, 'objectForKey:', _ignore_state):
        OBJC(_user_defaults, 'setBool:forKey:', False, _ignore_state)


def _max_size():
    _frame_rect = OBJC(OBJC('NSScreen', 'mainScreen'), 'visibleFrame')

    # frame rect 是指窗口大小，content rect 是绘制区域的大小
    _content_rect = OBJC('NSWindow', 'contentRectForFrameRect:styleMask:',
                         _frame_rect, WINDOW_STYLE)

    return _content_rect.mem_1.mem_0, _content_rect.mem_1.mem_1  # 宽和高


class Window(WindowPrototype):
    def __init__(self):
        WindowPrototype.__init__(self)

        self._app = None
        self._window = None
        self._delegate = None
        self._view = None
        self._tracking_area = None

    def _window_start(self):
        _width, _height = self._window_size
        if _width == 0 or _height == 0:
            _width, _height = _max_size()

        _pool = OBJC(OBJC('NSAutoreleasePool', 'alloc'), 'init')
        self._app = OBJC('NSApplication', 'sharedApplication')
        OBJC(self._app, 'setActivationPolicy:', 0)
        _ignore_error()

        if not OBJC(self._app, 'isRunning'):
            self._prepare_objc_class()
            self._create_menu()

            _context = self._create_window(
                self._window_title, _width, _height
            )
            self._finish_launch()
            self._init_mouse_position()
            self.window_running = True

            gl_context.prepare()
            self._window_prepare()
            self._window_clock = time.perf_counter()  # 记录启动时间

            try:
                while self.window_running:
                    _interval = self._window_sleep()  # 上一帧的运行时间
                    OBJC(_context, 'makeCurrentContext')
                    self._window_pull()
                    gl_context.gl_render(_interval)
                    OBJC(_context, 'flushBuffer')
                    self._app_event_hook()
                    OBJC(self._app, 'updateWindows')
            except KeyboardInterrupt:  # 防止 Ctrl-C 打断后无法回收，主动退出
                pass

            self._delete_tracking_area()
            OBJC('NSOpenGLContext', 'clearCurrentContext')
            OBJC(self._view, 'release')
            OBJC(self._delegate, 'release')

        OBJC(_pool, 'drain')

    def _prepare_objc_class(self):
        """ 准备好需要的 ObjC 类，注意不要重复加载 """

        _window_cls = SUBCLASS('GuWindow', 'NSWindow')
        _view_cls = SUBCLASS('GuView', 'NSView')
        _delegate_cls = SUBCLASS('GuDelegate', 'NSObject')

        @BIND(_window_cls, 'canBecomeKeyWindow', 'B16@0:8')
        @BIND(_window_cls, 'canBecomeMainWindow', 'B16@0:8')
        @BIND(_view_cls, 'isOpaque', 'B16@0:8')
        # @BIND(_view_cls, 'canBecomeKeyView', 'B16@0:8')  大概不需要这个
        def do(cls, sel):
            return True

        @BIND(_view_cls, 'updateTrackingAreas', 'v16@0:8')
        def do(cls, sel):
            """
            当窗口 resize 的时候，会自动调用这个函数，需要手动重建 TrackingArea
            如果不主动替换，鼠标检测时，会在系统消息里进行一次报错（用户不可见）
            之后会有相应的纠错，但是需要一些时间
            """
            self._delete_tracking_area()
            self._create_tracking_area()

        @BIND(_view_cls, 'cursorUpdate:', 'v24@0:8@16')
        @BIND(_view_cls, 'mouseEntered:', 'v24@0:8@16')
        def do(cls, sel, notification):
            _position = OBJC(self._view, 'convertPoint:fromView:',
                             OBJC(notification, 'locationInWindow'), None)
            _origin_x = _position.mem_0
            _origin_y = _position.mem_1
            self._window_push(
                window_input.mouse_enter, _origin_x, _origin_y
            )
            window_input.mouse_x, window_input.mouse_x = (
                _origin_x, _origin_y
            )  # 鼠标进入时重新定位

        @BIND(_view_cls, 'mouseExited:', 'v24@0:8@16')
        def do(cls, sel, notification):
            _position = OBJC(self._view, 'convertPoint:fromView:',
                             OBJC(notification, 'locationInWindow'), None)
            self._window_push(
                window_input.mouse_exit, _position.mem_0, _position.mem_1
            )

        @BIND(_view_cls, 'mouseMoved:', 'v24@0:8@16')
        def do(cls, sel, notification):
            _position = OBJC(self._view, 'convertPoint:fromView:',
                             OBJC(notification, 'locationInWindow'), None)
            _origin_x = _position.mem_0
            _origin_y = _position.mem_1
            self._window_push(
                window_input.mouse_move,
                _origin_x - window_input.mouse_x,
                _origin_y - window_input.mouse_y
            )
            window_input.mouse_x, window_input.mouse_y = (
                _origin_x, _origin_y
            )

        @BIND(_view_cls, 'scrollWheel:', 'v24@0:8@16')
        def do(cls, sel, notification):  # 鼠标用不到纵向，但是触控板会检测横向
            _delta_x = int(OBJC(notification, 'deltaX'))  # 横向
            _delta_y = -int(OBJC(notification, 'deltaY'))  # 纵向
            if _delta_x or _delta_y:  # 触控板会误触这个事件，这里排除误触
                self._window_push(
                    window_input.mouse_scroll_wheel, _delta_x, _delta_y
                )

        @BIND(_view_cls, 'mouseDown:', 'v24@0:8@16')
        def do(cls, sel, notification):
            _position = OBJC(self._view, 'convertPoint:fromView:',
                             OBJC(notification, 'locationInWindow'), None)
            self._window_push(
                window_input.mouse_down, _position.mem_0, _position.mem_1
            )

        @BIND(_view_cls, 'mouseDragged:', 'v24@0:8@16')
        def do(cls, sel, notification):
            _position = OBJC(self._view, 'convertPoint:fromView:',
                             OBJC(notification, 'locationInWindow'), None)
            _origin_x = _position.mem_0
            _origin_y = _position.mem_1
            self._window_push(
                window_input.mouse_dragged,
                _origin_x - window_input.mouse_x,
                _origin_y - window_input.mouse_y
            )
            window_input.mouse_x, window_input.mouse_y = (
                _origin_x, _origin_y
            )

        @BIND(_view_cls, 'mouseUp:', 'v24@0:8@16')
        def do(cls, sel, notification):
            _position = OBJC(self._view, 'convertPoint:fromView:',
                             OBJC(notification, 'locationInWindow'), None)
            self._window_push(
                window_input.mouse_up, _position.mem_0, _position.mem_1
            )

        @BIND(_view_cls, 'rightMouseDown:', 'v24@0:8@16')
        def do(cls, sel, notification):
            _position = OBJC(self._view, 'convertPoint:fromView:',
                             OBJC(notification, 'locationInWindow'), None)
            self._window_push(
                window_input.right_down, _position.mem_0, _position.mem_1
            )

        @BIND(_view_cls, 'rightMouseDragged:', 'v24@0:8@16')
        def do(cls, sel, notification):
            _position = OBJC(self._view, 'convertPoint:fromView:',
                             OBJC(notification, 'locationInWindow'), None)
            _origin_x = _position.mem_0
            _origin_y = _position.mem_1
            self._window_push(
                window_input.right_dragged,
                _origin_x - window_input.mouse_x,
                _origin_y - window_input.mouse_y
            )
            window_input.mouse_x, window_input.mouse_y = (
                _origin_x, _origin_y
            )

        @BIND(_view_cls, 'rightMouseUp:', 'v24@0:8@16')
        def do(cls, sel, notification):
            _position = OBJC(self._view, 'convertPoint:fromView:',
                             OBJC(notification, 'locationInWindow'), None)
            self._window_push(
                window_input.right_up, _position.mem_0, _position.mem_1
            )

        @BIND(_view_cls, 'otherMouseDown:', 'v24@0:8@16')
        def do(cls, sel, notification):
            _position = OBJC(self._view, 'convertPoint:fromView:',
                             OBJC(notification, 'locationInWindow'), None)
            self._window_push(
                window_input.other_down, _position.mem_0, _position.mem_1
            )

        @BIND(_view_cls, 'otherMouseDragged:', 'v24@0:8@16')
        def do(cls, sel, notification):
            _position = OBJC(self._view, 'convertPoint:fromView:',
                             OBJC(notification, 'locationInWindow'), None)
            _origin_x = _position.mem_0
            _origin_y = _position.mem_1
            self._window_push(
                window_input.other_dragged,
                _origin_x - window_input.mouse_x,
                _origin_y - window_input.mouse_y
            )
            window_input.mouse_x, window_input.mouse_y = (
                _origin_x, _origin_y
            )

        @BIND(_view_cls, 'otherMouseUp:', 'v24@0:8@16')
        def do(cls, sel, notification):
            _position = OBJC(self._view, 'convertPoint:fromView:',
                             OBJC(notification, 'locationInWindow'), None)
            self._window_push(
                window_input.other_up, _position.mem_0, _position.mem_1
            )

        @BIND(_delegate_cls, 'windowShouldClose:', 'B24@0:8@16')
        def do(cls, sel, notification):  # 参数是 Delegate类，SEL，消息
            self.window_running = False
            return True

        @BIND(_delegate_cls, 'windowWillStartLiveResize:', 'B24@0:8@16')
        def do(cls, sel, notification):
            self._delete_tracking_area()

        @BIND(_delegate_cls, 'windowDidEndLiveResize:', 'B24@0:8@16')
        def do(cls, sel, notification):
            self._create_tracking_area()
            _area = OBJC(self._view, 'bounds').mem_1
            self._window_push(
                window_input.resize, _area.mem_0, _area.mem_1
            )

        @BIND(_delegate_cls, 'windowWillMiniaturize:', 'B24@0:8@16')
        def do(cls, sel, notification):
            # NSApplication setDelegate: 无法设置 Application 的代理
            # 现在将 GuDelegate windowWillMiniaturize NSApplication hide: 绑定，
            # 使 App 仅有一个窗口，这种情况下，可以借用 UnHide 指令
            OBJC(self._app, 'hide:', None)

        @BIND(_delegate_cls, 'applicationDidShow:', 'B24@0:8@16')
        def do(cls, sel, notification):
            OBJC(self._window, 'makeKeyAndOrderFront:', None)

    def _create_tracking_area(self):
        # 获取窗口的尺寸，提供给 TrackingArea 使用
        _area = OBJC(self._view, 'bounds')  # 这里也许应该用 frame? bounds?
        # 鼠标触碰检测，如果不设置这个，当窗口 resize 的时候，鼠标会按不到键
        # 如果窗口位置进行了变动，tracking_area 必须重建
        _tracking_area = OBJC('NSTrackingArea', 'alloc')
        OBJC(_tracking_area, 'initWithRect:options:owner:userInfo:',
             _area, TRACKING_OPTION, self._view, None)
        OBJC(self._view, 'addTrackingArea:', _tracking_area)  # 设置鼠标触碰
        self._tracking_area = _tracking_area

    def _delete_tracking_area(self):
        """ 删除原有 TrackingArea """
        OBJC(self._view, 'removeTrackingArea:', self._tracking_area)
        OBJC(self._tracking_area, 'release')

    def _create_menu(self):
        _menu = OBJC(OBJC('NSMenu', 'alloc'), 'init')
        OBJC(_menu, 'addItem:',
             OBJC(OBJC('NSMenuItem', 'alloc'),
                  'initWithTitle:action:keyEquivalent:',
                  STR('hide'), SEL('hide:'), STR('h')))
        OBJC(_menu, 'addItem:', OBJC('NSMenuItem', 'separatorItem'))
        OBJC(_menu, 'addItem:',
             OBJC(OBJC('NSMenuItem', 'alloc'),
                  'initWithTitle:action:keyEquivalent:',
                  STR('quit'), SEL('terminate:'), STR('q')))
        _bar = OBJC(OBJC('NSMenu', 'alloc'), 'init')
        _item = OBJC(OBJC('NSMenuItem', 'alloc'), 'init')
        OBJC(_item, 'setSubmenu:', _menu)
        OBJC(_bar, 'addItem:', _item)
        OBJC(self._app, 'setMainMenu:', _bar)
        OBJC(_menu, 'release')
        OBJC(_item, 'release')
        OBJC(_bar, 'release')

    def _create_window(self, title, width, height):
        # 创建窗口
        _window = FIT(  # 建立一个窗口
            OBJC('GuWindow', 'alloc'),
            'initWithContentRect:styleMask:backing:defer:',
            (0, 0, width, height), WINDOW_STYLE,
            NSBackingStoreBuffered, False
        )
        OBJC(_window, 'setTitle:', STR(title))
        self._window = _window

        # 创建代理
        _delegate_obj = OBJC(OBJC('GuDelegate', 'alloc'), 'init')
        _notification_center = OBJC('NSNotificationCenter', 'defaultCenter')
        OBJC(_notification_center, 'addObserver:selector:name:object:',
             _delegate_obj, SEL('applicationDidShow:'),
             NSApplicationDidShowNotification, None)
        OBJC(_window, 'setDelegate:', _delegate_obj)
        self._delegate = _delegate_obj

        # 创建视口
        _area = OBJC(_window, 'frame')  # 获取窗口的尺寸，提供给 View 使用
        _view = OBJC(OBJC('GuView', 'alloc'), 'initWithFrame:', _area)
        OBJC(_window, 'setContentView:', _view)  # 设置 View 为内容
        OBJC(_window, 'makeFirstResponder:', _view)  # 设置为第一响应
        self._view = _view

        # 创建鼠标区域
        self._create_tracking_area()

        # 创建显卡缓冲区
        _pixel_format_attributes = [
            NSOpenGLPFADoubleBuffer, NSOpenGLPFASampleBuffers, 1,
            NSOpenGLPFASamples, 4, NSOpenGLPFADepthSize, 24,
            NSOpenGLPFAAllRenderer, NSOpenGLPFAMaximumPolicy,
            NSOpenGLPFAOpenGLProfile, NSOpenGLProfileVersion4_1Core, 0x00
        ]  # 最后一位 0x00 是结束符号

        _pfa = (ctypes.c_uint32 * len(_pixel_format_attributes))(
            *_pixel_format_attributes)

        _pixel_format = OBJC(
            OBJC('NSOpenGLPixelFormat', 'alloc'), 'initWithAttributes:', _pfa
        )

        _context = OBJC(
            OBJC('NSOpenGLContext', 'alloc'),
            'initWithFormat:shareContext:',
            _pixel_format, None
        )

        OBJC(_context, 'setView:', _view)
        OBJC(_context, 'makeCurrentContext')
        OBJC(_context, 'setValues:forParameter:',
             ctypes.c_int(1), NSOpenGLCPSwapInterval)
        OBJC(_context, 'update')  # 不进行 update 会有的原本的 context 一闪而过
        return _context

    def _finish_launch(self):
        # 窗口如果接受鼠标事件，就会重复 View 的鼠标事件
        OBJC(self._window, 'setAcceptsMouseMovedEvents:', False)
        OBJC(self._window, 'setReleasedWhenClosed:', True)  # 关闭时回收
        OBJC(self._window, 'useOptimizedDrawing:', False)  # 不需专心绘制 View 
        # 改变尺寸时不保留内容
        OBJC(self._window, 'setPreservesContentDuringLiveResize:', False)

        OBJC(self._window, 'orderOut:', None)  # 设置为关键窗口
        OBJC(self._window, 'makeKeyAndOrderFront:', self._window)
        OBJC(self._window, 'center')  # 注意，设置 center 后区域会改变

        OBJC(self._app, 'finishLaunching')
        OBJC(self._app, 'activateIgnoringOtherApps:', True)

    def _init_mouse_position(self):  # 第一次获取鼠标位置
        _mouse_pos = OBJC('NSEvent', 'mouseLocation')
        _window_pos = OBJC(self._window, 'frame').mem_0
        _mouse_pos.mem_0 -= _window_pos.mem_0
        _mouse_pos.mem_1 -= _window_pos.mem_1
        _mouse_pos = OBJC(self._view, 'convertPoint:fromView:',
                          _mouse_pos, None)
        window_input.mouse_x, window_input.mouse_y = (
            _mouse_pos.mem_0, _mouse_pos.mem_1
        )

    def _app_event_hook(self):
        while True:
            _event = OBJC(
                self._app, 'nextEventMatchingMask:untilDate:inMode:dequeue:',
                NSAnyEventMask, OBJC('NSDate', 'distantPast'),
                NSDefaultRunLoopMode, True)

            if not _event:
                break

            _event_type = OBJC(_event, 'type')
            OBJC(self._app, 'sendEvent:', _event)

            if ((_event_type == NSEventTypeKeyDown and
                 not OBJC(_event, 'isARepeat')) or
                    _event_type == NSEventTypeKeyUp or
                    _event_type == NSEventTypeFlagsChanged):
                self._window_push(
                    window_input.key_input, OBJC(_event, 'keyCode')
                )

    def _window_set_title(self):
        def _inner_thread():
            OBJC(self._window, 'setTitle:', STR(self._window_title))

        self._window_push(_inner_thread)  # app 相关函数需要在主线程里运行
        # self._window_push(
        #     OBJC, self._window, 'setTitle:', STR(self._window_title)
        # )

    def _window_set_image(self):
        raise NotImplementedError

    def _window_set_size(self):
        def _inner_thread():
            _area = OBJC(self._window, 'frame')
            w = _area.mem_1.mem_0
            h = _area.mem_1.mem_1
            w1, h1 = self._window_size
            w2, h2 = (w1 - w) // 2, (h1 - h) // 2
            x = _area.mem_0.mem_0 - w2
            y = _area.mem_0.mem_1 - h2
            FIT(self._window, 'setFrame:display:', (x, y, w1, h1), False)
            self._delete_tracking_area()
            self._create_tracking_area()

        self._window_push(_inner_thread)  # app 相关函数需要在主线程里运行
