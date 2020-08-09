import ctypes

from ._objc_runtime import Id
from ._objc_library import OBJC, FIT, STR, SEL, SUBCLASS, BIND, FIND

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
