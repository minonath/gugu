import ctypes

from ..system import bind, platform

# OpenGL 使用到的变量类型
Int = ctypes.c_int
UInt = ctypes.c_uint
Byte = ctypes.c_byte
UByte = ctypes.c_ubyte
UShort = ctypes.c_ushort
Float = ctypes.c_float
VoidP = ctypes.c_void_p
CharP = ctypes.c_char_p
P = ctypes.POINTER
C = ctypes.CFUNCTYPE
Double = ctypes.c_double
Short = ctypes.c_short
Size = ctypes.c_size_t
UInt64 = ctypes.c_uint64
Int64 = ctypes.c_int64
Int32 = ctypes.c_int32
if platform == 1:
    Handle = UInt
elif platform == 2:
    Handle = Size
else:
    raise NotImplementedError


class _GLSync(ctypes.Structure):
    ...


GLSync = P(_GLSync)

if platform == 1:  # 适配不同的系统
    class E(object):  # 扩展函数调用

        def __init__(self, name, restype, *arg_types):
            self._func = None
            self._name = bytes(ord(_c) for _c in name)
            self._type = ctypes.WINFUNCTYPE(restype, *arg_types)

        def __call__(self, *args):
            if self._func is None:  # 第一次调用勾取函数指针
                _address = _wglGetFunction(self._name)
                if not ctypes.cast(_address, P(Handle)):
                    return None
                self._func = ctypes.cast(_address, self._type)

            return self._func(*args)


    gl = bind(ctypes.windll.opengl32, E)  # 非扩展函数调用
    _wglGetFunction = gl('wglGetP''rocAddress', C(P(Handle)), CharP)


elif platform == 2:
    E = gl = bind(ctypes.cdll.LoadLibrary(
        '/System/Library/Framework/OpenGL.framework/OpenGL'
    ))

else:
    import ctypes.util

    E = gl = bind(ctypes.cdll.LoadLibrary(
        ctypes.util.find_library('OpenGL')
    ))


__all__ = [
    'UByte', 'Byte', 'UShort', 'Short', 'UInt', 'Int', 'Float', 'Double',
    'Int32', 'UInt64', 'Int64', 'Size', 'Handle', 'VoidP', 'CharP', 'GLSync',
    'C', 'P', 'E', 'gl'
]
