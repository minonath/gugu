from ._objc_library import *
from ._objc_constants import *

from ._objc_runtime import sel_getName, object_getClassName
from ._gu_util import gu


def print_sel(sel):
    return sel_getName(sel).decode('utf-8')
    # print(ctypes.cast(sel, ctypes.c_char_p).value.decode('utf-8'))


def print_string(ns_string):
    return OBJC(ns_string, 'UTF8String').decode('utf-8')


def print_objc(objc_id):
    return object_getClassName(objc_id).decode('utf-8')


gu.meow = True

_key_enum = {
    'kVK_ANSI_A': 0x00, 'kVK_ANSI_S': 0x01, 'kVK_ANSI_D': 0x02,
    'kVK_ANSI_F': 0x03, 'kVK_ANSI_H': 0x04, 'kVK_ANSI_G': 0x05,
    'kVK_ANSI_Z': 0x06, 'kVK_ANSI_X': 0x07, 'kVK_ANSI_C': 0x08,
    'kVK_ANSI_V': 0x09, 'kVK_ANSI_B': 0x0B, 'kVK_ANSI_Q': 0x0C,
    'kVK_ANSI_W': 0x0D, 'kVK_ANSI_E': 0x0E, 'kVK_ANSI_R': 0x0F,
    'kVK_ANSI_Y': 0x10, 'kVK_ANSI_T': 0x11, 'kVK_ANSI_1': 0x12,
    'kVK_ANSI_2': 0x13, 'kVK_ANSI_3': 0x14, 'kVK_ANSI_4': 0x15,
    'kVK_ANSI_6': 0x16, 'kVK_ANSI_5': 0x17, 'kVK_ANSI_Equal': 0x18,
    'kVK_ANSI_9': 0x19, 'kVK_ANSI_7': 0x1A, 'kVK_ANSI_Minus': 0x1B,
    'kVK_ANSI_8': 0x1C, 'kVK_ANSI_0': 0x1D, 'kVK_ANSI_RightBracket ': 0x1E,
    'kVK_ANSI_O': 0x1F, 'kVK_ANSI_U': 0x20, 'kVK_ANSI_LeftBracket': 0x21,
    'kVK_ANSI_I': 0x22, 'kVK_ANSI_P': 0x23, 'kVK_ANSI_L': 0x25,
    'kVK_ANSI_J': 0x26, 'kVK_ANSI_Quote': 0x27, 'kVK_ANSI_K': 0x28,
    'kVK_ANSI_Semicolon': 0x29, 'kVK_ANSI_Backslash': 0x2A,
    'kVK_ANSI_Comma': 0x2B, 'kVK_ANSI_Slash': 0x2C, 'kVK_ANSI_N': 0x2D,
    'kVK_ANSI_M': 0x2E, 'kVK_ANSI_Period ': 0x2F, 'kVK_ANSI_Grave': 0x32,
    'kVK_ANSI_KeypadDecimal': 0x41, 'kVK_ANSI_KeypadMultiply ': 0x43,
    'kVK_ANSI_KeypadPlus ': 0x45, 'kVK_ANSI_KeypadClear': 0x47,
    'kVK_ANSI_KeypadDivide ': 0x4B, 'kVK_ANSI_KeypadEnter': 0x4C,
    'kVK_ANSI_KeypadMinus': 0x4E, 'kVK_ANSI_KeypadEquals ': 0x51,
    'kVK_ANSI_Keypad0': 0x52, 'kVK_ANSI_Keypad1': 0x53,
    'kVK_ANSI_Keypad2': 0x54, 'kVK_ANSI_Keypad3': 0x55,
    'kVK_ANSI_Keypad4': 0x56, 'kVK_ANSI_Keypad5': 0x57,
    'kVK_ANSI_Keypad6': 0x58, 'kVK_ANSI_Keypad7': 0x59,
    'kVK_ANSI_Keypad8': 0x5B, 'kVK_ANSI_Keypad9': 0x5C, 'kVK_Return': 0x24,
    'kVK_Tab ': 0x30, 'kVK_Space ': 0x31, 'kVK_Delete': 0x33,
    'kVK_Escape': 0x35, 'kVK_Command ': 0x37, 'kVK_Shift ': 0x38,
    'kVK_CapsLock': 0x39, 'kVK_Option': 0x3A, 'kVK_Control ': 0x3B,
    'kVK_RightCommand': 0x36, 'kVK_RightShift': 0x3C,
    'kVK_RightOption ': 0x3D, 'kVK_RightControl': 0x3E, 'kVK_Function': 0x3F,
    'kVK_F17 ': 0x40, 'kVK_VolumeUp': 0x48, 'kVK_VolumeDown': 0x49,
    'kVK_Mute': 0x4A, 'kVK_F18 ': 0x4F, 'kVK_F19 ': 0x50, 'kVK_F20 ': 0x5A,
    'kVK_F5': 0x60, 'kVK_F6': 0x61, 'kVK_F7': 0x62, 'kVK_F3': 0x63,
    'kVK_F8': 0x64, 'kVK_F9': 0x65, 'kVK_F11 ': 0x67, 'kVK_F13 ': 0x69,
    'kVK_F16 ': 0x6A, 'kVK_F14 ': 0x6B, 'kVK_F10 ': 0x6D, 'kVK_F12 ': 0x6F,
    'kVK_F15 ': 0x71, 'kVK_Help': 0x72, 'kVK_Home': 0x73, 'kVK_PageUp': 0x74,
    'kVK_ForwardDelete ': 0x75, 'kVK_F4': 0x76, 'kVK_End ': 0x77,
    'kVK_F2': 0x78, 'kVK_PageDown': 0x79, 'kVK_F1': 0x7A,
    'kVK_LeftArrow ': 0x7B, 'kVK_RightArrow': 0x7C, 'kVK_DownArrow ': 0x7D,
    'kVK_UpArrow ': 0x7E
}

_KEY_MAP = dict((v, k) for k, v in _key_enum.items())


# 简单的添加目录，这是个雏形，后面还要做可以编辑的目录方式，通过参数创造大型目录栏
def _create_menu(_app):
    OBJC(_app, 'mainMenu')
    _menu = OBJC(OBJC('NSMenu', 'alloc'), 'init')

    OBJC(_menu, 'addItem:', OBJC(OBJC('NSMenuItem', 'alloc'),
                                 'initWithTitle:action:keyEquivalent:',
                                 STR('hide'), SEL('hide:'), STR('h')))
    OBJC(_menu, 'addItem:', OBJC('NSMenuItem', 'separatorItem'))
    OBJC(_menu, 'addItem:', OBJC(OBJC('NSMenuItem', 'alloc'),
                                 'initWithTitle:action:keyEquivalent:',
                                 STR('quit'), SEL('terminate:'), STR('q')))

    _bar = OBJC(OBJC('NSMenu', 'alloc'), 'init')
    _item = OBJC(OBJC('NSMenuItem', 'alloc'), 'init')
    OBJC(_item, 'setSubmenu:', _menu)
    OBJC(_bar, 'addItem:', _item)
    OBJC(_app, 'setMainMenu:', _bar)

    OBJC(_menu, 'release')
    OBJC(_item, 'release')
    OBJC(_bar, 'release')


def _create_context():  # 考虑不同版本的 OpenGL
    _pixel_format_attributes = [
        NSOpenGLPFADoubleBuffer, NSOpenGLPFASampleBuffers, 1,
        NSOpenGLPFASamples, 4, NSOpenGLPFADepthSize, 24,
        NSOpenGLPFAAllRenderers, NSOpenGLPFAMaximumPolicy,
        NSOpenGLPFAOpenGLProfile, NSOpenGLProfileVersion4_1Core, 0x00
    ]  # 最后一位 0x00 是结束符号
    # NSOpenGLProfileVersion3_2Core
    # NSOpenGLProfileVersionLegacy
    # NSOpenGLProfileVersion4_1Core,

    _pfa = (ctypes.c_uint32 * len(_pixel_format_attributes))(
        *_pixel_format_attributes)

    _pixel_format = OBJC(OBJC('NSOpenGLPixelFormat', 'alloc'),
                         'initWithAttributes:', _pfa)
    _context = OBJC(OBJC('NSOpenGLContext', 'alloc'),
                    'initWithFormat:shareContext:', _pixel_format, None)
    return _context


def _create_window(area=(0, 0, 800, 600)):
    _window = FIT(OBJC('NSWindow', 'alloc'),
                  'initWithContentRect:styleMask:backing:defer:', area,
                  (NSTitledWindowMask | NSClosableWindowMask |
                   NSMiniaturizableWindowMask | NSResizableWindowMask),
                  NSBackingStoreBuffered, False)
    area = OBJC(_window, 'frame')

    OBJC(_window, 'center')

    OBJC(_window, 'setAcceptsMouseMovedEvents:', True)
    OBJC(_window, 'setReleasedWhenClosed:', False)
    OBJC(_window, 'useOptimizedDrawing:', True)
    OBJC(_window, 'setPreservesContentDuringLiveResize:', False)
    return _window, area


def _create_delegate():
    _delegate = SUBCLASS('GuDelegate', 'NSObject')
    _object = OBJC(OBJC('GuDelegate', 'alloc'), 'init')
    _notification_center = OBJC('NSNotificationCenter', 'defaultCenter')
    OBJC(_notification_center, 'addObserver:selector:name:object:',
         _object, SEL('applicationDidHide:'),
         NSApplicationDidHideNotification, None)
    OBJC(_notification_center, 'addObserver:selector:name:object:',
         _object, SEL('applicationDidUn''hide:'),
         NSApplicationDidShowNotification, None)

    @BIND(_delegate, 'applicationDidHide:', 'v24@0:8@16')
    @BIND(_delegate, 'windowDidMiniaturize:', 'v24@0:8@16')
    def call(cls, sel, notification):
        print(print_objc(cls), print_sel(sel), print_objc(notification),
              print_string(OBJC(notification, 'name')),
              print_objc(OBJC(notification, 'object'))
              )

    @BIND(_delegate, 'applicationDidUn''hide:', 'v24@0:8@16')
    @BIND(_delegate, 'windowDidDe''miniaturize:', 'v24@0:8@16')
    def call(cls, sel, notification):
        print(print_objc(cls), print_sel(sel), print_objc(notification),
              print_string(OBJC(notification, 'name')),
              print_objc(OBJC(notification, 'object'))
              )

    @BIND(_delegate, 'windowDidEnterFullScreen:', 'v24@0:8@16')
    def call(cls, sel, notification):
        print(print_objc(cls), print_sel(sel), print_objc(notification),
              print_string(OBJC(notification, 'name')),
              print_objc(OBJC(notification, 'object')),
              print_objc(OBJC(notification, 'userInfo'))
              )

    @BIND(_delegate, 'windowShouldClose:', 'B24@0:8@16')
    def call(cls, sel, notification):
        gu.Meow = False
        return False

    @BIND(_delegate, 'windowDidMove:', 'v24@0:8@16')
    def call(cls, sel, notification):
        print(print_objc(cls), print_sel(sel), print_objc(notification),
              print_string(OBJC(notification, 'name')),
              print_objc(OBJC(notification, 'object')),
              print_objc(OBJC(notification, 'userInfo'))
              )

    @BIND(_delegate, 'windowDidResize:', 'v24@0:8@16')
    def call(cls, sel, notification):
        print(print_objc(cls), print_sel(sel), print_objc(notification),
              print_string(OBJC(notification, 'name')),
              print_objc(OBJC(notification, 'object')),
              print_objc(OBJC(notification, 'userInfo'))
              )

    return _object


def _ignore_error():
    # 创建窗口会导致报错
    # ApplePersistenceIgnoreState:
    # Existing state will not be touched. New state will be written to (null)
    # 这里取消这个错误检测

    user_defaults = OBJC('NSUserDefaults', 'standardUserDefaults')
    ignore_state = STR('ApplePersistenceIgnoreState')
    if OBJC(user_defaults, 'objectForKey:', ignore_state):
        OBJC(user_defaults, 'setBool:forKey:', False, ignore_state)


def _create_view(area):
    _view = OBJC(OBJC('NSView', 'alloc'), 'initWithFrame:', area)
    _options = (NSTrackingMouseEnteredAndExited | NSTrackingActiveInActiveApp
                | NSTrackingCursorUpdate)

    _tracking_area = OBJC('NSTrackingArea', 'alloc')
    OBJC(_tracking_area, 'initWithRect:options:owner:userInfo:', area,
         _options, _view, None)
    OBJC(_view, 'addTrackingArea:', _tracking_area)

    return _view, _tracking_area,


def _attach(window, view, context):
    OBJC(window, 'setContentView:', view)
    OBJC(window, 'makeFirstResponder:', view)
    OBJC(context, 'setView:', view)
    OBJC(OBJC(context, 'view'), 'setWantsBestResolutionOpenGLSurface:', 1)
    OBJC(context, 'makeCurrentContext')
    OBJC(context, 'setValues:forParameter:', ctypes.c_int(1),
         NSOpenGLCPSwapInterval)  # 设置同步
    OBJC(window, 'orderOut:', None)
    OBJC(window, 'makeKeyAndOrderFront:', None)


class _OpenGLWindow:
    @staticmethod
    def gl_init():
        pass

    @staticmethod
    def gl_clear():
        pass

    @staticmethod
    def gl_render():
        pass


def create_mac_window(gl_obj=_OpenGLWindow):
    pool = OBJC(OBJC('NSAutoreleasePool', 'alloc'), 'init')
    app = OBJC('NSApplication', 'sharedApplication')

    if not OBJC(app, 'isRunning'):
        _ignore_error()
        _create_menu(app)
        context = _create_context()
        window, area = _create_window()
        view, tracking_area, = _create_view(area)
        delegate = _create_delegate()
        OBJC(window, 'setDelegate:', delegate)

        _attach(window, view, context)

        OBJC(window, 'setTitle:', STR('Gu'))

        OBJC(app, 'finishLaunching')
        OBJC(app, 'activateIgnoringOtherApps:', True)
        OBJC(context, 'makeCurrentContext')
        gl_obj.context = context
        gl_obj.gl_init()
        while gu.meow:
            while True:
                OBJC(context, 'makeCurrentContext')
                gl_obj.gl_clear()
                gl_obj.gl_render()
                OBJC(context, 'flushBuffer')
                # 做强制刷新
                event = OBJC(
                    app, 'nextEventMatchingMask:untilDate:inMode:de''queue:',
                    NSAnyEventMask, OBJC('NSDate', 'distantPast'),
                    NSDefaultRunLoopMode, True)
                if not event:
                    break

                event_type = OBJC(event, 'type')
                OBJC(app, 'sendEvent:', event)

                if event_type == NSKeyDown and not OBJC(event, 'isARepeat'):
                    print(_KEY_MAP[OBJC(event, 'keyCode')])
                    # print(bin(OBJC(event, 'modifierFlags')))
                elif event_type == NSKeyUp:
                    pass
                elif event_type == NSFlagsChanged:
                    pass

                OBJC(app, 'updateWindows')

    OBJC(pool, 'drain')
