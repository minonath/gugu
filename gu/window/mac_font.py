import ctypes
import math

from gu.system import bind_dynamic_library

core_foundation = ctypes.cdll.LoadLibrary(
    '/System/Library/Frameworks/CoreFoundation.framework/CoreFoundation'
)
core_text = ctypes.cdll.LoadLibrary(
    '/System/Library/Frameworks/CoreText.framework/CoreText'
)
quartz = ctypes.cdll.LoadLibrary(
    '/System/Library/Frameworks/quartz.framework/quartz'
)
_F = bind_dynamic_library(core_foundation)
_T = bind_dynamic_library(core_text)
_G = bind_dynamic_library(quartz)
_P = ctypes.POINTER

CharP = ctypes.c_char_p
VoidP = ctypes.c_void_p
Bool = ctypes.c_bool
Double = ctypes.c_double
SizeT = ctypes.c_size_t

if ctypes.sizeof(ctypes.c_size_t) == 8:
    CGFloat = ctypes.c_double
    CFIndex = ctypes.c_longlong
    CFOptionFlags = ctypes.c_ulonglong
else:
    CGFloat = ctypes.c_float
    CFIndex = ctypes.c_long
    CFOptionFlags = ctypes.c_ulong

CFAllocatorRef = VoidP  # ptr of structure CFAllocator
CFDictionaryRef = VoidP  # ptr of structure CFDictionary
CFMutableDictionaryRef = VoidP  # ptr of structure CFDictionary 与前者有差别？
CFStringRef = VoidP  # ptr of structure CFString
CFStringEncoding = ctypes.c_uint32  # CF_ENUM
CFAttributedStringRef = VoidP  # ptr of structure CFAttributedString
CFNumberRef = VoidP  # ptr of structure CFNumber
CFNumberType = CFIndex  # CF_ENUM
CFDataRef = VoidP  # ptr of structure CFData
CTFontRef = VoidP  # ptr of structure CFFont
UniChar = ctypes.c_ushort
CGGlyph = ctypes.c_ushort  # CGFontIndex
CTFontOrientation = ctypes.c_uint32  # CF_ENUM
CGColorSpaceRef = VoidP  # ptr of structure CGColorSpace
CGContextRef = VoidP  # ptr of structure CGContext
CGBitmapInfo = ctypes.c_uint32  # CF_ENUM
CTLineRef = VoidP  # ptr of structure CTLine
CGImageRef = VoidP  # ptr of structure CGImage
CGDataProviderRef = VoidP  # ptr of structure CGDataProvider
CFArrayRef = VoidP  # ptr of structure CFArray


class CGPoint(ctypes.Structure):
    _fields_ = [("x", CGFloat), ("y", CGFloat)]


class CGSize(ctypes.Structure):
    _fields_ = [("width", CGFloat), ("height", CGFloat)]


class CGRect(ctypes.Structure):
    _fields_ = [ ("origin", CGPoint), ("size", CGSize) ]


class CFRange(ctypes.Structure):
    _fields_ = [("location", CFIndex), ("length", CFIndex)]


kCFStringEncodingUTF8 = 0x08000100  # 用于转换 CFString 和 char *
kCFTypeDictionaryKeyCallBacks = VoidP.in_dll(
    core_foundation, 'kCFTypeDictionaryKeyCallBacks')
kCFTypeDictionaryValueCallBacks = VoidP.in_dll(
    core_foundation, 'kCFTypeDictionaryValueCallBacks')
kCTFontAttributeName = VoidP.in_dll(core_text, 'kCTFontAttributeName')

kCFNumberSInt8Type = 1
kCFNumberSInt16Type = 2
kCFNumberSInt32Type = 3
kCFNumberSInt64Type = 4
kCFNumberFloat32Type = 5
kCFNumberFloat64Type = 6
kCFNumberCharType = 7
kCFNumberShortType = 8
kCFNumberIntType = 9
kCFNumberLongType = 10
kCFNumberLongLongType = 11
kCFNumberFloatType = 12
kCFNumberDoubleType = 13
kCFNumberCFIndexType = 14
kCFNumberCGFloatType = 16

kCGImageAlphaLast = 1
kCGImageAlphaOnly = 7

# 基础类
CFRelease = _F('CFRelease', None, VoidP)

# 文本类
CFStringCreateWithCString = _F(
    'CFStringCreateWithCString', CFStringRef, CFAllocatorRef, CharP,
    CFStringEncoding)
CFStringGetCString = _F(
    'CFStringGetCString', Bool, CFStringRef, CharP, CFIndex, CFStringEncoding)
CFAttributedStringCreate = _F(
    'CFAttributedStringCreate', CFAttributedStringRef, CFAllocatorRef,
    CFStringRef, CFDictionaryRef)
CFStringGetLength = _F('CFStringGetLength', CFIndex, CFStringRef)
CFStringGetMaximumSizeForEncoding = _F(
    'CFStringGetMaximumSizeForEncoding', CFIndex, CFIndex, CFStringEncoding)

# 数组
CFArrayGetCount = _F('CFArrayGetCount', CFIndex, CFArrayRef)
CFArrayGetValueAtIndex = _F(
    'CFArrayGetValueAtIndex', VoidP, CFArrayRef, CFIndex)

# 字典类
CFDictionaryCreateMutable = _F(
    'CFDictionaryCreateMutable', CFMutableDictionaryRef, CFAllocatorRef,
    CFIndex, VoidP, VoidP)
CFDictionaryAddValue = _F(
    'CFDictionaryAddValue', None, CFMutableDictionaryRef, VoidP, VoidP)
CFDictionarySetValue = _F(
    'CFDictionarySetValue', None, CFMutableDictionaryRef, VoidP, VoidP)
CFDictionaryRemoveValue = _F(
    'CFDictionaryRemoveValue', None, CFMutableDictionaryRef, VoidP)

# 数字类
CFNumberCreate = _F(
    'CFNumberCreate', CFNumberRef, CFAllocatorRef, CFNumberType, VoidP)

# 数据类
CFDataGetLength = _F('CFDataGetLength', CFIndex, CFDataRef)
CFDataGetBytes = _F(  # 最后一个参数为 Point(unsigned bytes)
    'CFDataGetBytes', None, CFDataRef, CFRange, VoidP)
CGDataProviderRelease = _G('CGDataProviderRelease', None, CGDataProviderRef)
CGDataProviderCopyData = _G(
    'CGDataProviderCopyData', CFDataRef, CGDataProviderRef)

# 字体类
CTFontCreateWithName = _T(  # 最后一个参数为 Point(CGAffineTransform)
    'CTFontCreateWithName', CTFontRef, CFStringRef, CGFloat, VoidP)
CTFontGetGlyphsForCharacters = _T(
    'CTFontGetGlyphsForCharacters', Bool, CTFontRef, _P(UniChar), _P(CGGlyph),
    CFIndex)
CTFontGetOpticalBoundsForGlyphs = _T(
    'CTFontGetOpticalBoundsForGlyphs', CGRect, CTFontRef,
    _P(CGGlyph), _P(CGRect), CFIndex, CFOptionFlags)
CTFontGetAdvancesForGlyphs = _T(
    'CTFontGetAdvancesForGlyphs', Double, CTFontRef, CTFontOrientation,
    _P(CGGlyph), _P(CGSize), CFIndex)
CTFontManagerCopyAvailableFontFamilyNames = _T(
    'CTFontManagerCopyAvailableFontFamilyNames', CFArrayRef)

# 位图类
CGBitmapContextCreate = _G(
    'CGBitmapContextCreate', CGContextRef, VoidP, SizeT, SizeT, SizeT, SizeT,
    CGColorSpaceRef, CGBitmapInfo)
CGContextSetTextPosition = _G(
    'CGContextSetTextPosition', None, CGContextRef, CGFloat, CGFloat)
CGBitmapContextCreateImage = _G(
    'CGBitmapContextCreateImage', CGImageRef, CGContextRef)
CGImageRelease = _G('CGImageRelease', None, CGImageRef)
CGImageGetDataProvider = _G(
    'CGImageGetDataProvider', CGDataProviderRef, CGImageRef)

# 色彩空间类
CGColorSpaceCreateDeviceGray = _G(
    'CGColorSpaceCreateDeviceGray', CGColorSpaceRef)
CGColorSpaceCreateDeviceRGB = _G(
    'CGColorSpaceCreateDeviceRGB', CGColorSpaceRef)

# 文本线
CTLineDraw = _T('CTLineDraw', None, CTLineRef, CGContextRef)
CTLineCreateWithAttributedString = _T(
    'CTLineCreateWithAttributedString', CTLineRef, CFAttributedStringRef)


class OCoreObject:
    def __init__(self, core_function, *args, release=CFRelease):
        self._as_parameter_ = core_function(*args)
        self._release_func_ = release

    def __del__(self):
        if self._as_parameter_:
            self._release_func_(self)


class OCoreDict(OCoreObject):
    def __init__(self, *args):
        OCoreObject.__init__(
            self, CFDictionaryCreateMutable, None, 0,
            kCFTypeDictionaryKeyCallBacks, kCFTypeDictionaryValueCallBacks
        )

        if args:
            args = iter(args)
            try:
                CFDictionaryAddValue(self, next(args), next(args))
            except StopIteration:
                pass

    def __setitem__(self, key, value):
        if self._as_parameter_:
            CFDictionarySetValue(self, key, value)

    def __delitem__(self, key):
        if self._as_parameter_:
            CFDictionaryRemoveValue(self, key)


class OCoreNumber(OCoreObject):
    CORE_NUMBER = {
        kCFNumberSInt8Type: ctypes.c_int8,
        kCFNumberSInt16Type: ctypes.c_int16,
        kCFNumberSInt32Type: ctypes.c_int32,
        kCFNumberSInt64Type: ctypes.c_int64,
        kCFNumberFloat32Type: ctypes.c_float,
        kCFNumberFloat64Type: ctypes.c_double,
        kCFNumberCharType: ctypes.c_byte,
        kCFNumberShortType: ctypes.c_short,
        kCFNumberIntType: ctypes.c_int,
        kCFNumberLongType: ctypes.c_long,
        kCFNumberLongLongType: ctypes.c_longlong,
        kCFNumberFloatType: ctypes.c_float,
        kCFNumberDoubleType: ctypes.c_double,
        kCFNumberCFIndexType: CFIndex,
        kCFNumberCGFloatType: CGFloat,
    }

    def __init__(self, number, mask):
        c_type = self.CORE_NUMBER[mask]
        OCoreObject.__init__(
            self, CFNumberCreate, None, mask, ctypes.byref(c_type(number))
        )


class OCoreString(OCoreObject):
    def __init__(self, string):
        string = string.encode('utf8')
        OCoreObject.__init__(
            self, CFStringCreateWithCString, 0, string, kCFStringEncodingUTF8
        )


def cf_string_to_bytes(cf_string):
    size = CFStringGetLength(cf_string)
    c_size = CFStringGetMaximumSizeForEncoding(size, kCFStringEncodingUTF8)
    buffer = ctypes.create_string_buffer(c_size)
    CFStringGetCString(cf_string, buffer, c_size, kCFStringEncodingUTF8)
    return ctypes.string_at(buffer)


class OCoreFont(OCoreObject):
    def __init__(self, name, size: float):
        OCoreObject.__init__(
            self, CTFontCreateWithName, OCoreString(name), size, None
        )

    def render(self, text):
        count = len(text)

        chars = (UniChar * count)(*(ord(x) for x in text))
        glyphs = (CGGlyph * count)()
        CTFontGetGlyphsForCharacters(self, chars, glyphs, count)

        # for i in range(count):  # 无法从字体中获取图像编号，说明语言不对应。
        #     if glyphs[i] == 0:
        #         return

        rect = CTFontGetOpticalBoundsForGlyphs(self, glyphs, None, count, 0)
        advance = CTFontGetAdvancesForGlyphs(self, 0, glyphs, None, count)

        width = max(int(math.ceil(rect.size.width) + 2), 1)
        height = max(int(math.ceil(rect.size.height) + 2), 1)
        baseline = -int(math.floor(rect.origin.y)) + 1
        lsb = int(math.floor(rect.origin.x)) - 1
        width += int(round(advance)) + 2
        height += baseline

        color_space = OCoreObject(CGColorSpaceCreateDeviceGray)
        bitmap = OCoreObject(
            CGBitmapContextCreate, None, width, height,
            8, width, color_space, kCGImageAlphaOnly
        )
        # CGContextSetShouldAntialias(bitmap, True)
        CGContextSetTextPosition(bitmap, -lsb, baseline)

        attributes = OCoreDict(kCTFontAttributeName, self)
        string = OCoreObject(
            CFAttributedStringCreate, None, OCoreString(text), attributes)
        line = OCoreObject(CTLineCreateWithAttributedString, string)
        CTLineDraw(line, bitmap)

        image = OCoreObject(
            CGBitmapContextCreateImage, bitmap, release=CGImageRelease
        )
        image_data = OCoreObject(
            CGDataProviderCopyData, CGImageGetDataProvider(image),
            release=CGDataProviderRelease
        )
        buffer_size = CFDataGetLength(image_data)
        buffer_data = (ctypes.c_byte * buffer_size)()
        byte_range = CFRange(0, buffer_size)
        CFDataGetBytes(image_data, byte_range, buffer_data)
        return bytes(buffer_data), width, height


def list_all_fonts():
    all_fonts = CTFontManagerCopyAvailableFontFamilyNames()
    result = set()
    for i in range(CFArrayGetCount(all_fonts)):
        name = cf_string_to_bytes(CFArrayGetValueAtIndex(all_fonts, i))
        if not name.startswith(b'.'):
            result.add(name.decode())
    return list(result)
