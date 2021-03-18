import ctypes
from .library import *

_normal = glVertexAttribPointer
_integer = glVertexAttribIPointer
_long = glVertexAttribLPointer

_INFO = {
    # 每组元素的个数, 元素类型, 占用字节长度, 单位化, 设置函数, 占用编号数量
    GL_INT: (4, GL_INT, False, _integer, 1),
    GL_INT_VEC2: (4, GL_INT, False, _integer, 1),
    GL_INT_VEC3: (4, GL_INT, False, _integer, 1),
    GL_INT_VEC4: (4, GL_INT, False, _integer, 1),
    GL_UNSIGNED_INT: (4, GL_UNSIGNED_INT, False, _integer, 1),
    GL_UNSIGNED_INT_VEC2: (4, GL_UNSIGNED_INT, False, _integer, 1),
    GL_UNSIGNED_INT_VEC3: (4, GL_UNSIGNED_INT, False, _integer, 1),
    GL_UNSIGNED_INT_VEC4: (4, GL_UNSIGNED_INT, False, _integer, 1),
    GL_FLOAT: (4, GL_FLOAT, True, _normal, 1),
    GL_FLOAT_VEC2: (4, GL_FLOAT, True, _normal, 1),
    GL_FLOAT_VEC3: (4, GL_FLOAT, True, _normal, 1),
    GL_FLOAT_VEC4: (4, GL_FLOAT, True, _normal, 1),
    # version 410 以上才可以使用 double
    GL_DOUBLE: (8, GL_DOUBLE, False, _long, 1),
    GL_DOUBLE_VEC2: (8, GL_DOUBLE, False, _long, 1),
    GL_DOUBLE_VEC3: (8, GL_DOUBLE, False, _long, 1),
    GL_DOUBLE_VEC4: (8, GL_DOUBLE, False, _long, 1),
    # 一般不考虑 attribute 输入矩阵的情况，但是万一呢
    GL_FLOAT_MAT2: (4, GL_FLOAT, True, _normal, 2),
    GL_FLOAT_MAT2x3: (4, GL_FLOAT, True, _normal, 2),
    GL_FLOAT_MAT2x4: (4, GL_FLOAT, True, _normal, 2),
    GL_FLOAT_MAT3x2: (4, GL_FLOAT, True, _normal, 3),
    GL_FLOAT_MAT3: (4, GL_FLOAT, True, _normal, 3),
    GL_FLOAT_MAT3x4: (4, GL_FLOAT, True, _normal, 3),
    GL_FLOAT_MAT4x2: (4, GL_FLOAT, True, _normal, 4),
    GL_FLOAT_MAT4x3: (4, GL_FLOAT, True, _normal, 4),
    GL_FLOAT_MAT4: (4, GL_FLOAT, True, _normal, 4),
    # alloc 表示行数，两行矩阵就占用两个
    GL_DOUBLE_MAT2: (8, GL_DOUBLE, False, _long, 2),
    GL_DOUBLE_MAT2x3: (8, GL_DOUBLE, False, _long, 2),
    GL_DOUBLE_MAT2x4: (8, GL_DOUBLE, False, _long, 2),
    GL_DOUBLE_MAT3x2: (8, GL_DOUBLE, False, _long, 3),
    GL_DOUBLE_MAT3: (8, GL_DOUBLE, False, _long, 3),
    GL_DOUBLE_MAT3x4: (8, GL_DOUBLE, False, _long, 3),
    GL_DOUBLE_MAT4x2: (8, GL_DOUBLE, False, _long, 4),
    GL_DOUBLE_MAT4x3: (8, GL_DOUBLE, False, _long, 4),
    GL_DOUBLE_MAT4: (8, GL_DOUBLE, False, _long, 4),
}


def _attributes(program):
    """ 获取 Program 对象的 Attributes 属性 """

    _number = ctypes.c_int()  # GLint()
    _member_type = ctypes.c_uint()  # GL enum
    _member_array = ctypes.c_int()  # GLint()
    _NAME_LENGTH = 256
    _member_name = (ctypes.c_char * _NAME_LENGTH)()
    _member_name_size = ctypes.c_int()  # GLint()

    glGetProgramiv(program, GL_ACTIVE_ATTRIBUTES, _number)
    for _i in range(_number.value):
        glGetActiveAttrib(
            program, _i, _NAME_LENGTH, _member_name_size,
            _member_array, _member_type, _member_name
        )
        _location = glGetAttribLocation(program, _member_name)
        _name = _member_name[:_member_name_size.value].decode()
        _multi = _member_array.value
        _size, _type, _normalize, _setter, _occupy = _INFO[_member_type.value]

        if _multi:
            yield _name, tuple((_location + _a * _occupy, _size, _type,
                                _normalize, _setter) for _a in range(_multi))
        else:
            yield _name, ((_location, _size, _type, _normalize, _setter),)


class VertexArray:
    POINTS = GL_POINTS
    LINES = GL_LINES
    LINE_STRIP = GL_LINE_STRIP
    LINE_LOOP = GL_LINE_LOOP
    TRIANGLES = GL_TRIANGLES
    TRIANGLE_STRIP = GL_TRIANGLE_STRIP
    TRIANGLE_FAN = GL_TRIANGLE_FAN

    def __init__(self, program, *rules):
        _vertex_array_id = ctypes.c_uint()
        glGenVertexArrays(1, _vertex_array_id)

        if not _vertex_array_id:
            raise OpenGLError('无法创建(VertexArray)顶点数组')

        self._as_parameter_ = _vertex_array_id
        program and self.__call__(program, *rules)

    def __del__(self):
        glDeleteVertexArrays(1, self._as_parameter_)  # 奇怪，这里用 self 报错

        # <class 'TypeError'>: expected P(UInt) instance instead of UInt
        # 应该是 Python 内部的一些错误，不能准确判断 C 语言中这个是指针传递类型

    def __call__(self, program, *rules):
        """ 指定 Program 对象生成生成对应的属性序列，然后将缓存送入指定的名字之中 """

        _vao_attributes = dict(_attributes(program))
        # print(_vao_attributes)
        """
        rules 需要按顺序包含下面七个信息
        attribute_name      attribute 的名称
        attribute_index     attribute 如果是数组，这个值就是数组的下标
        buffer              buffer 对象
        buffer_stride       buffer 每组元素的个数，会随着用户设置改变
        buffer_offset       buffer 元素的起点，会随着用户设置改变
        buffer_number       buffer 元素的终点，会随着用户设置改变
        divisor             设置每个 instance 绘制时读取的规则，0 表示全部读取
                            除 0 以外的任意正整数 n ，表示 n 个 instance 读取一次

        可是是 tuple 也可以是 Rule 对象
        """
        glBindVertexArray(self)

        for _name, _index, _buffer, _stride, _offset, _num, _divisor in rules:
            _attribute = _vao_attributes[_name]
            _location, _unit, _type, _normalize, _setter = _attribute[_index]

            _stride *= _unit
            _offset *= _unit

            glBindBuffer(GL_ARRAY_BUFFER, _buffer)

            if _normalize:  # glVertexAttribPointer
                _setter(_location, _num, _type, _normalize, _stride, _offset)
            else:  # glVertexAttribIPointer, glVertexAttribLPointer
                _setter(_location, _num, _type, _stride, _offset)

            glEnableVertexAttribArray(_location)
            glVertexAttribDivisor(_location, _divisor)


class Rule:
    def __init__(self, name, index=0, *,
                 buffer, stride, offset=0, number=0, divisor=0):
        self.name = name
        self.index = index
        self.buffer = buffer
        self.stride = stride
        self.offset = offset
        self.number = number or stride
        self.divisor = divisor

    def __iter__(self):
        yield self.name
        yield self.index
        yield self.buffer
        yield self.stride
        yield self.offset
        yield self.number
        yield self.divisor
