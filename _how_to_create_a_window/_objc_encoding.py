"""
将 Objective-C 类型编码的文本转换为 ctypes 可用格式。

Method 是 Objective-C 里的函数类，做为 Class/Instance 的函数方法使用。
它包含有一些成员变量，比如 name、type_encoding，其中就有 Imp 类型的变量。
我们知道 Objective-C 是用 C 语言实现的底层，所有的 Object 都是一个 C 语言结构体。
Imp 在结构体中的是一个 (void *)function，是一个 C 语言的函数（外加一些装饰器）。
既然是 C 语言函数，我们就可以使用 ctypes 链接它，然后越过 Objective-C 语言的限制。

将 C function 转换为 Py function 需要知道它的返回类型和参数类型。
因此，我们需要从 Objective-C Runtime 中拿到 Method 的相关的类型标记。
在 Runtime 中相关的类型标记是一个文本信息，类似这样 '@16@0:8'。
这个文本信息原本是用来检查纠正代码错误的，其中的数字不一定需要，但是任何 Method 都含有。
这也方便了我们的调用，我们只需要将它转换为 ctypes 的 restype 和 arg types，就可以了。

转换代码如下：
"""
import ctypes
import typing

# 一些基本的类型，这里缺少 '@': Id, '#': Class, ':': Sel，在后面单独加入。
objc_encodings = {
    b'c': ctypes.c_ubyte,  # A char (== unsigned char)
    b'i': ctypes.c_int,  # An int
    b's': ctypes.c_short,  # A short
    b'l': ctypes.c_long,  # A long (as a 32-bit quantity on 64-bit)
    b'q': ctypes.c_longlong,  # A long long
    b'C': ctypes.c_ubyte,  # An unsigned char
    b'I': ctypes.c_uint,  # An unsigned int
    b'S': ctypes.c_ushort,  # An unsigned short
    b'L': ctypes.c_ulong,  # An unsigned long
    b'Q': ctypes.c_ulonglong,  # An unsigned long long
    b'f': ctypes.c_float,  # A float
    b'd': ctypes.c_double,  # A double
    b'B': ctypes.c_bool,  # A C++ bool or a C99 _Bool (但是我从来没见它用过)
    b'v': None,  # A void
    b'*': ctypes.c_char_p,  # A character string (char *)
}


def _objc_split_encoding_by_number(encoding: bytes) -> typing.Generator:
    """
    将 encoding 分割成为以数字为间隔的队列。

    这里的 encoding 就是从 Runtime 中提取出来的 (method_getTypeEncoding)。
    """

    # 三个分别表示：参数的缓存区域，当前编码的深度，出栈标记。
    _param, _depth, _sign = [], 0, False

    for _b in encoding:
        if not _depth:
            # 数值'0123456789'的 Ascii 值为 48-57。
            if _b in b'0123456789':
                if not _sign:  # 如果深度为0，没有出栈标记，立即进行一次出栈。
                    yield bytes(_param)
                    _param.clear()
                    _sign = True  # 做好出栈标记，下次遇到正常字符也会进行一次出栈。
            else:
                if _sign:  # 如果有出栈标记，进行一次出栈操作。
                    yield int(bytes(_param))
                    _param.clear()
                    _sign = False

        if _b in b'([{':
            _depth += 1  # 调节深度，整体对比会更快，所以这里就重复一次运算。
        elif _b in b')]}':
            _depth -= 1

        _param.append(_b)

    yield int(bytes(_param))  # 理论上最后一次出栈是数字。


def _objc_split_encoding(encoding: bytes) -> typing.Generator:
    """
    把并列的一些类型分开。

    这个函数和 _objc_split_encoding_by_number 十分相似，具体细节差别由注释表明。
    但是没有明显的数字分割标记，只能按照字符分割，^归后面，数字归前面，有深度的合并。
    """
    _param, _depth, _sign = [], 0, False

    for _b in encoding:
        if not _depth:
            if _b in b'0123456789':
                if not _sign:
                    # yield bytes(_param)
                    # _param.clear()
                    _sign = True
            else:
                if _sign:
                    yield bytes(_param)  # yield int(bytes(_param))
                    _param.clear()
                    _sign = False
                if _b not in b'^':  # ^可以保留后面的字符。
                    _sign = True  # 每个字符标记一次出栈。

        if _b in b'([{':
            _depth += 1
        elif _b in b')]}':
            _depth -= 1

        _param.append(_b)

    yield bytes(_param)  # yield int(bytes(_param))


def _objc_get_type(encoding):
    """ 通过 Objective-C 类型文本获取 ctypes 的类型。 """
    encoding = encoding.lstrip(b'VrRnNoO')  # 这几个字符是标记字符，和类型无关。

    if encoding in objc_encodings:
        return objc_encodings[encoding]

    if encoding.startswith(b'^'):
        _type = ctypes.POINTER(_objc_get_type(encoding[1:]))  # 递归调用。

    elif encoding.startswith(b'('):  # 这是一个联合体。
        _type = _objc_make_type(encoding[1:-1], ctypes.Union)

    elif encoding.startswith(b'['):  # 这是一个数组，现场制作一个 ctypes.Array。
        _num, _sub = [], []

        for _b in encoding[1:-1]:
            if _b in b'0123456789':
                _num.append(_b)  # 获取长度。
            else:
                _sub.append(_b)  # 获取数组的基本类型。

        _type = _objc_get_type(bytes(_sub)) * int(bytes(_num))
        _type.auto_fit = lambda _input: _type(*_input)  # auto_fit 自动填充。

    elif encoding.startswith(b'{'):  # 这是一个结构体。
        _type = _objc_make_type(encoding[1:-1], ctypes.Structure)

    else:
        _type = None  # 如果不是指针的话，None 会报错。

    objc_encodings[encoding] = _type  # 记录该类型，下次调用可以节省速度。
    return _type


def _objc_make_type(encoding: bytes, base: type) -> type:
    """赞吉尔没有类型，赞吉尔自己做类型"""
    _name, _equal, _sub = encoding.partition(b'=')
    if not _equal:  # 无名结构，不进行参数指定
        _type = None
    _name = '_Anonymous' if _name == b'?' else _name.decode('utf-8')
    _type = type(_name, (base,), {})

    _fields = []
    if _sub.startswith(b'b'):  # 是个位域
        _bit_field_types = [
            ctypes.c_uint8, ctypes.c_uint16, ctypes.c_uint32, ctypes.c_uint32,
            ctypes.c_uint64, ctypes.c_uint64, ctypes.c_uint64, ctypes.c_uint64
        ]
        _type._pack_ = 1  # 对齐模式，设为 1-byte 对齐

        for _number, _field_encoding in enumerate(_objc_split_encoding(_sub)):
            _length = int(bytes(_field_encoding[1:]))
            _bit_type = _bit_field_types[(_length - 1) >> 3]
            _fields.append(('bit_{}'.format(_number), _bit_type, _length))
    else:
        for _number, _field_encoding in enumerate(_objc_split_encoding(_sub)):
            _fields.append(
                ('mem_{}'.format(_number), _objc_get_type(_field_encoding))
            )

    def _auto_fit(_input):  # 自动填充函数
        if not isinstance(_input, typing.Iterator):
            _input = iter(_input)

        _return = _type()
        for _field in _fields:
            _field_name, _field_type = _field[:2]
            if hasattr(_field_type, 'auto_fit'):
                # 只有传递 Iterator 才能不错位
                setattr(_return, _field_name, _field_type.auto_fit(_input))
            else:
                setattr(_return, _field_name, next(_input))

        return _return

    _type._fields_ = _fields
    _type.auto_fit = _auto_fit
    return _type


def objc_type_from_encoding(encoding: bytes) -> tuple:
    """
    将 encoding 分割成两组。第一组是返回类型，第二组是参数类型。

    第一步，通过 method_getTypeEncoding 拿到 encoding 数据。
    第二步，_objc_get_type 把文本转换为 ctypes 格式。

    默认的 encoding 是 '@16@0：8'（比如 [[AutoreleasePool alloc] init]）。
    分组文本后，我们可以得到 '@'、['@', ':']
    第一组文本是返回类型，第二组是参数类型。

    此外我们还能得到一个数组 [0, 8, 16]，这是参数的偏移量，是一个比较复杂的概念：
    在 C 语言中，函数的输入参数都会被压缩到一个内存块里，这个内存块的指针才是真正的参数。
    函数拿到内存块后，会按照编译器设定好内存偏移量逐个读取参数。
    所以实际输入参数数量超过设定参数数量时，函数还是可以正常运行。它只会拿它需要的参数。
    C 语言编译器会把参数的偏移量保存在函数头中，也就是参数的定位。
    作为动态静态混搭的 Objective-C，这个定位信息也是需要的，因为底层实现还是依靠 C 语言。

    因此，针对第三组 [0, 8, 16] 我们的解释是这样的：
    在 0 的位置输入 Class，在 8 的位置输入 Sel，在 16 的位置返回 Class。
    0，8，16 是字节偏量，它们的差值是 8，也就是一个 64-bit size_t 的字节长度。

    最后一组数字，对与 ctypes 来说没有使用价值，因为 ctypes 本身有自动匹配。
    但是我们可以拿它来做检测，参数的字节长度不应该超过定位，否则表示我们的参数有问题。
    """
    _generator = _objc_split_encoding_by_number(encoding)

    try:
        _return = next(_generator)  # 第一个类型是返回值类型
        _arguments_size = next(_generator)  # 第二个数是整个 arguments 的长度
    except StopIteration:
        raise ValueError('编码不合规定:{}'.format(encoding))

    _arguments, _check = [], []  # 参数类型数组 和 长度检测用数组
    try:
        _arguments.append(next(_generator))  # 第二个参数是 Class/Id '@'/'#'
        _check.append(next(_generator))  # 第二个数一般情况下是0
        _arguments.append(next(_generator))  # 第三个参数是 Sel ':'
        _check.append(next(_generator))  # 第三个数一般情况下是8

        try:
            while True:  # 两个两个一组
                _arguments.append(next(_generator))
                _check.append(next(_generator))
        except StopIteration:
            _check.append(_arguments_size)  # 把最初拿到的总长度添加到这里

        _arguments = tuple(map(_objc_get_type, _arguments))

        # 接下来检查参数类型的位置
        for _type, _previous, _next in zip(_arguments, _check, _check[1:]):
            if ctypes.sizeof(_type) > _next - _previous:
                raise ValueError('数据长度不符:{}'.format(encoding))

        return _objc_get_type(_return), _arguments

    except StopIteration:
        raise ValueError('编码不合规定，至少需要两个输入参数:{}'.format(encoding))


__all__ = ['objc_encodings', 'objc_type_from_encoding']
