import ctypes
import sys


if sys.platform in ('win32', 'cygwin'):
    KEY_MAP = {
        'Esc': 0x01, 'F1': 0x3B, 'F2': 0x3C, 'F3': 0x3D, 'F4': 0x3E,
        'F5': 0x3F, 'F6': 0x40, 'F7': 0x41, 'F8': 0x42,
        'F9': 0x43, 'F10 ': 0x44, 'F11 ': 0x45, 'F12 ': 0x46,

        'Grave': 0x29, '1': 0x02, '2': 0x03, '3': 0x04, '4': 0x05,
        '5': 0x06, '6': 0x07, '7': 0x08, '8': 0x09,
        '9': 0x0A, '0': 0x0B, 'Minus': 0x0C, 'Equal': 0x0D, 'Delete': 0x0E,

        'Tab': 0x0F, 'Q': 0x10, 'W': 0x11, 'E': 0x12, 'R': 0x13,
        'T': 0x14, 'Y': 0x15, 'U': 0x16, 'I': 0x17, 'O': 0x18, 'P': 0x19,
        'LeftBracket': 0x1A, 'RightBracket': 0x1B, 'Backslash': 0x2B,

        'Caps': 0x3A, 'A': 0x1E, 'S': 0x1F, 'D': 0x20, 'F': 0x21,
        'G': 0x22, 'H': 0x23, 'J': 0x24, 'K': 0x25,
        'L': 0x26, 'Semicolon': 0x27, 'Quote': 0x28, 'Enter': 0x1C,

        'Shift': 0x2A, 'Z': 0x2C, 'X': 0x2D, 'C': 0x2E, 'V': 0x2F,
        'B': 0x30, 'N': 0x31, 'M': 0x32, 'Comma': 0x33,
        'Period': 0x34, 'Slash': 0x35, 'RightShift': 0x36,

        'Ctrl': 0x1D, 'Alt': 0x38, 'Space': 0x39, 'RightCtrl': 0x011D,
        'RightAlt': 0x0138, 'Left ': 0x014B, 'Up': 0x0148,
        'Down ': 0x0150, 'Right': 0x014D
    }
    SYSTEM_PLATFORM = 1

elif sys.platform == 'darwin':
    KEY_MAP = {  # 这里所有的按键实际上是 unsigned，但是在 python 里是 signed
        'Esc': 0x35, 'F1': 0x7A, 'F2': 0x78, 'F3': 0x63, 'F4': 0x76,
        'F5': 0x60, 'F6': 0x61, 'F7': 0x62, 'F8': 0x64,
        'F9': 0x65, 'F10 ': 0x6D, 'F11 ': 0x67, 'F12 ': 0x6F,

        'Grave': 0x32, '1': 0x12, '2': 0x13, '3': 0x14, '4': 0x15,
        '5': 0x17, '6': 0x16, '7': 0x1A, '8': 0x1C,
        '9': 0x19, '0': 0x1D, 'Minus': 0x1B, 'Equal': 0x18, 'Delete': 0x33,

        'Tab': 0x30, 'Q': 0x0C, 'W': 0x0D, 'E': 0x0E, 'R': 0x0F,
        'T': 0x11, 'Y': 0x10, 'U': 0x20, 'I': 0x22, 'O': 0x1F, 'P': 0x23,
        'LeftBracket': 0x21, 'RightBracket': 0x1E, 'Backslash': 0x2A,

        'Caps': 0x39, 'A': 0x00, 'S': 0x01, 'D': 0x02, 'F': 0x03,  # 注意 A
        'G': 0x05, 'H': 0x04, 'J': 0x26, 'K': 0x28,
        'L': 0x25, 'Semicolon': 0x29, 'Quote': 0x27, 'Enter': 0x24,

        'Shift': 0x38, 'Z': 0x06, 'X': 0x07, 'C': 0x08, 'V': 0x09,
        'B': 0x0B, 'N': 0x2D, 'M': 0x2E, 'Comma': 0x2B,
        'Period': 0x2F, 'Slash': 0x2C, 'RightShift': 0x3C,

        'Ctrl': 0x37, 'Alt': 0x3A, 'Space': 0x31, 'RightCtrl': 0x36,
        'RightAlt': 0x3D, 'Left ': 0x7B, 'Up': 0x7E,
        'Down ': 0x7D, 'Right': 0x7C
    }
    SYSTEM_PLATFORM = 2

else:
    # KEY_MAP
    # esc f1 f2 f3 f4 f5 f6 f7 f8 f9 f10 f11 f12
    # grave 1 2 3 4 5 6 7 8 9 0 -(minus) =(equal) delete
    # tab q w e r t y u i o p [(left_bracket) ](right_bracket) \(backslash)
    # caps a s d f g h j k l ;(semicolon) '(quote) enter
    # shift z x c v b n m ,(comma) .(period) /(slash) shift
    # ctrl alt space ctrl alt left up down right
    SYSTEM_PLATFORM = 0

    raise NotImplementedError


class Array(object):
    _P_CHAR = ctypes.POINTER(ctypes.c_char)

    _array_size = 1

    def __init__(self, *args, size=0, data_type=None):
        if not size:
            size = self._array_size

        if not data_type:
            data_type = Type.Float

        _type, _element_bytes = Type.C_TYPES[data_type]
        self._array_type = data_type
        self._array_size = size
        self._array_bytes = size * _element_bytes
        self._array_data = (_type * size)(*args[:size])
        self._array_address = ctypes.addressof(self._array_data)
        self._as_parameter_ = ctypes.cast(
            self._array_address, ctypes.POINTER(_type)
        )

    @property
    def array_address(self):
        return self._array_address

    def array_from(self, address):
        """ 从某个指针提取相应的数据，原本用 @array_address.setter 的 """

        # 注意这里是转化为有长度有类型的指针，也就是 type[size] 的结构指针
        _type, _ = Type.C_TYPES[self._array_type]
        _structure = ctypes.POINTER(_type * self._array_size)
        _structure_data = ctypes.cast(address, _structure)[0]
        self._array_data[:] = _structure_data

    @classmethod
    def array_at(cls, address, size, data_type):
        _array = object.__new__(cls)

        _type, _element_bytes = Type.C_TYPES[data_type]
        _array._array_type = data_type
        _array._array_size = size
        _array._array_bytes = size * _element_bytes
        _array._array_data = ctypes.cast(
            address, ctypes.POINTER(_type * size)
        )[0]
        _array._array_address = ctypes.addressof(_array._array_data)
        _array._as_parameter_ = ctypes.cast(
            _array._array_address, ctypes.POINTER(_type)
        )

        return _array

    def array_offset(self, offset=0):
        """
        将数列的某个偏量作为指针变量传出
        如果参数为零，就是将自身转化为无长度有类型指针 type* 这样
        而 _as_parameter_ 不一样，是数列的无类型野指针，相当于 void* 这样
        """

        _type, _element_bytes = Type.C_TYPES[self._array_type]
        return ctypes.cast(
            self._array_address + offset * _element_bytes,
            ctypes.POINTER(_type)
        )

    def __getitem__(self, item):

        return self._array_data[item]

    def __setitem__(self, key, value):

        self._array_data[key] = value

    def __repr__(self):
        """ 这样会显示出浮点数，即使是整型也是浮点数表示 """

        if self._array_type == Type.Char:
            return str(bytes(self))

        elif self._array_type in (Type.Float, Type.Double, Type.Double2):
            return self.__class__.__name__ + '(%s)' % ', '.join(
                '{:.3f}' for _ in range(self._array_size)).format(*self)

        else:
            return self.__class__.__name__ + '(%s)' % ', '.join(
                '{:d}' for _ in range(self._array_size)).format(*self)

    def __call__(self, *new_value, new_type=None):
        """ 为整个数列进行赋值 """

        if new_type:
            _type, _element_bytes = Type.C_TYPES[new_type]

            self._array_type = new_type
            self._array_size = self.array_bytes // _element_bytes
            self._array_bytes = self._array_size * _element_bytes

            self._array_data = ctypes.cast(
                self._array_data, ctypes.POINTER(_type * self._array_size)
            )[0]
            # 上述操作并不影响 self._array_address 在内存中的位置
            # 只是改变了 python 虚拟机对该段内存的解读
            # 等于新建一个 python 对象，但是对象的指针还是指向原有内存
            # self._array_address = ctypes.address of(self._array_data)
            self._as_parameter_ = ctypes.cast(
                self._array_address, ctypes.POINTER(_type)
            )

        if new_value:  # 从第一位开始填写，不会影响超出输入的内容
            _s = len(new_value)
            if _s == self._array_size:
                self._array_data[:] = new_value
            elif _s < self._array_size:
                self._array_data[:_s] = new_value
            else:
                self._array_data[:] = new_value[:self._array_size]

        # if not (new_value or new_type):
        elif not new_type:
            ctypes.memset(self._as_parameter_, 0, self._array_bytes)

        return self

    def __bytes__(self):
        """ 使用 ctypes.c_char_p 的 value 来获取字节会导致在 0x00 处错误终止 """

        if self._array_type == Type.Char:
            _meow = self._array_data
        else:
            _meow = ctypes.cast(self._array_data, self._P_CHAR)

        return _meow[:self._array_bytes]

    def __len__(self):
        return self._array_size

    def array_new_size(self, new_size, new_bytes=False):
        """ 改变这个数组的长度 """

        _type, _element_bytes = Type.C_TYPES[self._array_type]

        if new_bytes:
            new_size = (new_size + _element_bytes - 1) // _element_bytes

        self._array_size = new_size
        self._array_bytes = new_size * _element_bytes
        self._array_data = (_type * new_size)(*self._array_data[:new_size])
        self._array_address = ctypes.addressof(self._array_data)
        self._as_parameter_ = ctypes.cast(
            self._array_address, ctypes.POINTER(_type)
        )

    @property
    def array_type(self):
        return self._array_type

    @property
    def array_size(self):
        return self._array_size

    @property
    def array_bytes(self):
        """ self._array_bytes == len(self.__bytes__()) """

        return self._array_bytes


class Type(object):
    Byte = 'byte'
    Short = 'short'
    Int = 'int'
    Long = 'long'
    Long2 = 'longlong'

    UByte = 'unsigned byte'
    UShort = 'unsigned short'
    UInt = 'unsigned int'
    ULong = 'unsigned long'
    ULong2 = 'unsigned longlong'

    Char = 'char'
    Float = 'float'
    Double = 'double'
    Double2 = 'longdouble'

    C_TYPES = {  # all types
        Byte: (ctypes.c_byte, ctypes.sizeof(ctypes.c_byte)),
        Short: (ctypes.c_short, ctypes.sizeof(ctypes.c_short)),
        Int: (ctypes.c_int, ctypes.sizeof(ctypes.c_int)),
        Long: (ctypes.c_long, ctypes.sizeof(ctypes.c_long)),
        Long2: (ctypes.c_longlong, ctypes.sizeof(ctypes.c_longlong)),

        UByte: (ctypes.c_ubyte, ctypes.sizeof(ctypes.c_ubyte)),
        UShort: (ctypes.c_ushort, ctypes.sizeof(ctypes.c_ushort)),
        UInt: (ctypes.c_uint, ctypes.sizeof(ctypes.c_uint)),
        ULong: (ctypes.c_ulong, ctypes.sizeof(ctypes.c_ulong)),
        ULong2: (ctypes.c_ulonglong, ctypes.sizeof(ctypes.c_ulonglong)),

        Char: (ctypes.c_char, ctypes.sizeof(ctypes.c_char)),
        Float: (ctypes.c_float, ctypes.sizeof(ctypes.c_float)),
        Double: (ctypes.c_double, ctypes.sizeof(ctypes.c_double)),
        Double2: (ctypes.c_longdouble, ctypes.sizeof(ctypes.c_longdouble))
    }


def bind_dynamic_library(lib, fallback=None):
    """
    绑定函数

    输入已加载的动态库，返回绑定用函数
    """

    def _bind(name, restype, *arg_types):
        """
        从动态库里绑定函数的函数
        """
        try:
            _func = getattr(lib, name)
            _func.restype = restype
            setattr(_func, 'arg''types', arg_types)

        except AttributeError:  # 绑定失败，返回无效函数
            if fallback:
                _func = fallback(name, restype, *arg_types)
            else:
                def _func(*args):  # 无法加载的函数，默认使用这个
                    print('<Error Func>', lib, name, args)

        return _func

    return _bind


def null_function(*args, **kwargs):
    ...


__all__ = [
    'KEY_MAP', 'SYSTEM_PLATFORM', 'Array', 'Type',
    'bind_dynamic_library', 'null_function',
]
