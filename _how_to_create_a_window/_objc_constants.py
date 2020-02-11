"""
下面是执行参数
"""
import ctypes
from ._objc_runtime import Id

# /System/Library/Frameworks/AppKit.framework/Headers/NSOpenGL.h
NSOpenGLPFAAllRenderers = 1
NSOpenGLPFADoubleBuffer = 5
NSOpenGLPFAStereo = 6
NSOpenGLPFAAuxBuffers = 7
NSOpenGLPFAColorSize = 8
NSOpenGLPFAAlphaSize = 11
NSOpenGLPFADepthSize = 12
NSOpenGLPFAStencilSize = 13
NSOpenGLPFAAccumSize = 14
NSOpenGLPFAMinimumPolicy = 51
NSOpenGLPFAMaximumPolicy = 52
NSOpenGLPFAOffScreen = 53
NSOpenGLPFAFullScreen = 54
NSOpenGLPFASampleBuffers = 55
NSOpenGLPFASamples = 56
NSOpenGLPFAAuxDepthStencil = 57
NSOpenGLPFAColorFloat = 58
NSOpenGLPFAMultisample = 59
NSOpenGLPFASupersample = 60
NSOpenGLPFASampleAlpha = 61
NSOpenGLPFARendererID = 70
NSOpenGLPFASingleRenderer = 71
NSOpenGLPFANoRecovery = 72
NSOpenGLPFAAccelerated = 73
NSOpenGLPFAClosestPolicy = 74
NSOpenGLPFARobust = 75
NSOpenGLPFABackingStore = 76
NSOpenGLPFAMPSafe = 78
NSOpenGLPFAWindow = 80
NSOpenGLPFAMultiScreen = 81
NSOpenGLPFACompliant = 83
NSOpenGLPFAScreenMask = 84
NSOpenGLPFAPixelBuffer = 90
NSOpenGLPFARemotePixelBuffer = 91
NSOpenGLPFAAllowOfflineRenderers = 96
NSOpenGLPFAAcceleratedCompute = 97
NSOpenGLPFAOpenGLProfile = 99
NSOpenGLPFAVirtualScreenCount = 128
NSOpenGLProfileVersionLegacy = 0x1000
NSOpenGLProfileVersion3_2Core = 0x3200
NSOpenGLProfileVersion4_1Core = 0x4100
NSOpenGLCPSwapInterval = 222

# /System/Library/Frameworks/AppKit.framework/Headers/NSGraphics.h
NSBackingStoreRetained = 0
NSBackingStoreNonretained = 1
NSBackingStoreBuffered = 2

# /System/Library/Frameworks/AppKit.framework/Headers/NSWindow.h
NSBorderlessWindowMask = 0
NSTitledWindowMask = 1 << 0
NSClosableWindowMask = 1 << 1
NSMiniaturizableWindowMask = 1 << 2
NSResizableWindowMask = 1 << 3

# /System/Library/Frameworks/AppKit.framework/Headers/NSRunningApplication.h
NSApplicationActivationPolicyRegular = 0
NSApplicationActivationPolicyAccessory = 1
NSApplicationActivationPolicyProhibited = 2

# /System/Library/Frameworks/AppKit.framework/Headers/NSTrackingArea.h
NSTrackingMouseEnteredAndExited = 0x01
NSTrackingMouseMoved = 0x02
NSTrackingCursorUpdate = 0x04
NSTrackingActiveInActiveApp = 0x40

# /System/Library/Frameworks/AppKit.framework/Headers/NSEvent.h
NSAnyEventMask = 0xFFFFFFFF

NSKeyDown = 10
NSKeyUp = 11
NSFlagsChanged = 12
NSApplicationDefined = 15

_app_kit = ctypes.cdll.LoadLibrary(
    '/System/Library/Frameworks/AppKit.framework/AppKit'
)

NSDefaultRunLoopMode = Id.in_dll(_app_kit, 'NSDefaultRunLoopMode')
NSEventTrackingRunLoopMode = Id.in_dll(_app_kit, 'NSEventTrackingRunLoopMode')
NSApplicationDidHideNotification = Id.in_dll(
    _app_kit, 'NSApplicationDidHideNotification'
)
NSApplicationDidShowNotification = Id.in_dll(
    _app_kit, 'NSApplicationDidUnhideNotification'
)
