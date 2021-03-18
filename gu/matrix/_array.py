import ctypes


class Array:
    # 支持以下类型作为内存数列
    UByte = ctypes.c_ubyte  # 如果没有特殊情况，这个是默认的
    Byte = ctypes.c_byte
    UShort = ctypes.c_ushort
    Short = ctypes.c_short
    UInt = ctypes.c_uint
    Int = ctypes.c_int
    ULong = ctypes.c_ulong
    Long = ctypes.c_long
    Float = ctypes.c_float  # 需要用 C 语言计算浮点的时候用这个
    Double = ctypes.c_double

    _CharPointer = ctypes.POINTER(ctypes.c_char)  # 以字符形式传出

    def __init__(self, data_nums, data_type=UByte):
        self._array_data = (data_type * data_nums)()  # 初始化
        self._array_type = data_type
        self._array_nums = data_nums
        self._array_unit = unit_length = ctypes.sizeof(data_type)
        self._array_size = unit_length * data_nums
        self._array_here = ctypes.addressof(self._array_data)  # 复制了地址对象
        self._as_parameter_ = ctypes.cast(  # 默认使用类型指针，上面的是野指针
            self._array_here, ctypes.POINTER(data_type)
        )

    def __call__(self, *values):
        _value_size = len(values)
        if _value_size > self._array_size:
            self._array_data[:] = values[:self._array_size]
        else:
            self._array_data[:_value_size] = values

        return self

    def __bytes__(self):
        if self._array_type == self._CharPointer:
            _array_data = self._array_data
        else:
            _array_data = ctypes.cast(self._array_data, self._CharPointer)

        return _array_data[:self._array_size]

    def __getitem__(self, item):

        return self._array_data[item]

    def __setitem__(self, key, value):

        self._array_data[key] = value

    @property
    def address(self):
        # 这是数组内存的地址头，实际上是一个野指针
        # 有些绑定的 C 语言函数需要类型指针，要用 _as_parameter_ 获取
        # 如果不需要类型指针，比如 glSubData 之类的，用野指针就行

        return self._array_here

    @property
    def offset(self, offset=0):
        # 将数列的某个元素作为类型指针传出，如果参数为零，等同于 _as_parameter_

        return ctypes.cast(
            self._array_here + offset * ctypes.sizeof(self._array_type),
            ctypes.POINTER(self._array_type)
        )

    @address.setter
    def address(self, address):
        # 从某个指针提取相应的数据
        # 注意这里是转化为有长度有类型的指针，也就是 type[size] 的结构指针

        _structure = ctypes.POINTER(self._array_type * self._array_size)
        _structure_data = ctypes.cast(address, _structure)[0]
        self._array_data[:] = _structure_data

    @classmethod
    def at(cls, address, data_nums, data_type=UByte):
        _array = object.__new__(cls)

        _array._array_type = data_type
        _array._array_nums = data_nums
        _array._array_data = ctypes.cast(
            address, ctypes.POINTER(data_type * data_nums)
        )[0]
        _array._array_unit = unit_length = ctypes.sizeof(data_type)
        _array._array_size = unit_length * data_nums

        _array._array_here = ctypes.addressof(_array._array_data)
        _array._as_parameter_ = ctypes.cast(
            _array._array_here, ctypes.POINTER(data_type)
        )

        return _array

    @property
    def size(self):
        return self._array_size

    @property
    def nums(self):
        return self._array_nums


class UBytes(Array):
    def __init__(self, *values, data_nums=0):
        if data_nums == 0:
            data_nums = len(values)

        Array.__init__(self, data_nums, Array.UByte)
        self.__call__(*values)


class Bytes(Array):
    def __init__(self, *values, data_nums=0):
        if data_nums == 0:
            data_nums = len(values)

        Array.__init__(self, data_nums, Array.Byte)
        self.__call__(*values)


class UShorts(Array):
    def __init__(self, *values, data_nums=0):
        if data_nums == 0:
            data_nums = len(values)

        Array.__init__(self, data_nums, Array.UShort)
        self.__call__(*values)


class Shorts(Array):
    def __init__(self, *values, data_nums=0):
        if data_nums == 0:
            data_nums = len(values)

        Array.__init__(self, data_nums, Array.Short)
        self.__call__(*values)


class UInts(Array):
    def __init__(self, *values, data_nums=0):
        if data_nums == 0:
            data_nums = len(values)

        Array.__init__(self, data_nums, Array.UInt)
        self.__call__(*values)


class Ints(Array):
    def __init__(self, *values, data_nums=0):
        if data_nums == 0:
            data_nums = len(values)

        Array.__init__(self, data_nums, Array.Int)
        self.__call__(*values)


class ULongs(Array):
    def __init__(self, *values, data_nums=0):
        if data_nums == 0:
            data_nums = len(values)

        Array.__init__(self, data_nums, Array.ULong)
        self.__call__(*values)


class Longs(Array):
    def __init__(self, *values, data_nums=0):
        if data_nums == 0:
            data_nums = len(values)

        Array.__init__(self, data_nums, Array.Long)
        self.__call__(*values)


class Floats(Array):
    def __init__(self, *values, data_nums=0):
        if data_nums == 0:
            data_nums = len(values)

        Array.__init__(self, data_nums, Array.Float)
        self.__call__(*values)


class Doubles(Array):
    def __init__(self, *values, data_nums=0):
        if data_nums == 0:
            data_nums = len(values)

        Array.__init__(self, data_nums, Array.Double)
        self.__call__(*values)


__all__ = [
    'Array', 'UBytes', 'Bytes', 'UShorts', 'Shorts', 'UInts', 'Ints',
    'ULongs', 'Longs', 'Floats', 'Doubles'
]
