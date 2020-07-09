import ctypes

from .object import OpenGLObject

from ..system import Array
from ..opengl import *

BUFFER_TYPES = {
    'GL_BYTE': (ctypes.c_byte, 1),
    'GL_UNSIGNED_BYTE': (ctypes.c_ubyte, 1),
    'GL_SHORT': (ctypes.c_short, 2),
    'GL_UNSIGNED_SHORT': (ctypes.c_ushort, 2),
    'GL_INT': (ctypes.c_int, 4),
    'GL_UNSIGNED_INT': (ctypes.c_uint, 4),
    'GL_FLOAT': (ctypes.c_float, 4),
    'GL_DOUBLE': (ctypes.c_double, 8)
}

BUFFER_TARGETS = (
    'GL_ARRAY_BUFFER', 'GL_ELEMENT_ARRAY_BUFFER', 'GL_UNIFORM_BUFFER',
    # 'GL_TEXTURE_BUFFER'
)

BUFFER_MODES = (
    'GL_STATIC_DRAW', 'GL_DYNAMIC_DRAW', 'GL_STREAM_DRAW'
)


class Buffer(OpenGLObject):
    """
    缓存对象

    缓存在内存中的结构:

    ┌───┬───┬───┬───┬───┬───┬───┬───┬───┐   ...   ┌───┬───┬───┐
    │ 1 │ 2 │ 3 │ 4 │ 5 │ 6 │ 7 │ 8 │ 9 │   ...   │n─2│n─1│ n │ elements = n
    ├───┴───┴───┼───┴───┴───┼───┴───┴───┤   ...   ├───┴───┴───┤
    │     1     │     2     │     3     │   ...   │     m     │ component = 3
    └───────────┴───────────┴───────────┘   ...   └───────────┘ groups = m
    """

    def __init__(self, data, type_mask, buffer_target, buffer_mode,
                 components=1):
        assert type_mask in BUFFER_TYPES
        assert buffer_target in BUFFER_TARGETS
        assert buffer_mode in BUFFER_MODES

        self._buffer_type_mask = type_mask
        self._buffer_type = gl_getattr(type_mask)
        self._buffer_element_type, self._buffer_element_bytes = \
            BUFFER_TYPES[type_mask]

        if isinstance(data, int):  # 创建一个长度的空 Buffer 。
            self._buffer_element_nums = data
            self._buffer_data = 0

        else:
            if not isinstance(data, Array):  # 创建一个 Array 。
                data = Array(*data, element_nums=len(data),
                             element_type=self._buffer_element_type)

            self._buffer_element_nums = data.array_element_nums
            self._buffer_data = data

        self._buffer_id = ctypes.c_uint()
        self._buffer_bytes = (self._buffer_element_bytes *
                              self._buffer_element_nums)
        self._buffer_target_enum = buffer_target
        self._buffer_target = gl_getattr(buffer_target)
        self._buffer_mode_enum = buffer_mode
        self._buffer_mode = gl_getattr(buffer_mode)

        self._buffer_group_nums = self._buffer_element_nums // components
        self._buffer_group_element_nums = components
        self._buffer_group_bytes = self._buffer_element_bytes * components

        OpenGLObject.__init__(self)

    def __repr__(self):
        return self.__string__

    def __str__(self):
        if self._buffer_id:
            return ('<{} size={} elements={} components={} type={} target={}'
                    ' mode={}>').format(
                self.__string__, self._buffer_bytes, self._buffer_element_nums
                , self._buffer_group_element_nums, self._buffer_type_mask,
                self._buffer_target_enum, self._buffer_mode_enum
            )
        else:
            return 'wait...'

    def gl_initialize(self) -> str:
        glGenBuffers(1, self._buffer_id)

        if not self._buffer_id:
            raise OpenGLError('无法创建(Buffer)缓存')

        glBindBuffer(self._buffer_target, self._buffer_id)
        glBufferData(self._buffer_target, self._buffer_bytes,
                     self._buffer_data, self._buffer_mode)

        return 'buffer_%s' % self._buffer_id.value

    def gl_release(self) -> None:
        glDeleteBuffers(1, self._buffer_id)

    def __call__(self):
        glBindBuffer(self._buffer_target, self._buffer_id)

    def buffer_write(self, data, offset=0):
        if not data:
            raise ValueError('不能写入空值')

        offset *= self._buffer_element_bytes  # 获取字节偏移的个数。

        # 不考虑格式问题，反正都能写入。
        if data.array_data_bytes + offset > self._buffer_bytes:
            raise OverflowError('写入数据长度超过了缓冲区大小')

        glBindBuffer(self._buffer_target, self._buffer_id)
        glBufferSubData(
            self._buffer_target, offset, data.array_data_bytes, data
        )

    def buffer_read(self, length=0, offset=0, result=None):
        # 读取需要考虑格式问题。
        if not length:  # length 表示的是读取的元素个数。
            length = self._buffer_element_nums - offset

        if offset < 0 or offset + length > self._buffer_element_nums:
            raise OverflowError('访问数据超出范围')

        glBindBuffer(self._buffer_target, self._buffer_id)

        buffer = glMapBufferRange(  # 这里拿到的是一个整型。
            self._buffer_target,
            offset * self._buffer_element_bytes,
            length * self._buffer_element_bytes,
            GL_MAP_READ_BIT
        )

        if not buffer:
            raise OpenGLError('不能映射当前缓存')

        if not result:
            result = Array(
                element_nums=length, element_type=self._buffer_element_type
            )

        if result.array_element_nums < length:  # 要确保 result 有足够的位置。
            raise ValueError('%s 的长度不足' % result.__repr__())

        buffer = ctypes.cast(  # 把数值转化为指针。
            buffer, ctypes.POINTER(result.array_element_type)
        )

        result[:length] = buffer[:length]
        glUnmapBuffer(self._buffer_target)
        return result

    def buffer_clear(self, length=0, offset=0, chunk=None) -> None:
        if not length:
            length = self._buffer_element_nums - offset

        if not chunk:
            chunk = Array(0, element_type=self._buffer_element_type)

        chunk_length = chunk.array_element_nums
        chunk_number, exactly = divmod(length, chunk_length)

        if exactly:
            raise ValueError('复数的 chunk 不能填满 buffer')

        glBindBuffer(self._buffer_target, self._buffer_id)

        buffer = glMapBufferRange(
            self._buffer_target, 0, self._buffer_bytes, GL_MAP_WRITE_BIT
        )

        if not buffer:
            raise OpenGLError('不能映射当前缓存')

        buffer = ctypes.cast(
            buffer, ctypes.POINTER(chunk.array_element_type)
        )

        for _y in range(chunk_number):
            _z = chunk_length * _y + offset
            for _x in range(chunk_length):
                buffer[_z + _x] = chunk[_x]

        glUnmapBuffer(self._buffer_target)

    @property
    def buffer_group_nums(self):  # 传递给 Vertex 使用
        return self._buffer_group_nums

    @property
    def buffer_type(self):  # 传递给 Vertex 使用
        return self._buffer_type

    def buffer_bind_location(self, location_generator, divisor):
        _offset, _stride = 0, self._buffer_group_bytes
        try:
            while _stride > _offset:
                (_location, _element_number, _element_type, _location_size,
                 _normalizable, _set_function) = next(location_generator)

                if (_element_type != self._buffer_type or
                        # type 相同 size 也相同，因此这里不检查 element_size 了
                        _element_number > self._buffer_group_nums or
                        _location_size > self._buffer_group_bytes):
                    raise ValueError('%s 不匹配' % self.__string__)

                if _normalizable:
                    _set_function(  # glVertexAttribPointer
                        _location,  # 通过 attribute 在显卡定位
                        _element_number,  # 显卡需要读取的元素个数
                        _element_type,  # 元素类型
                        _normalizable,  # 是否单位化
                        _stride,  # 元素中每组的字节长度
                        _offset  # 起始偏量
                    )

                else:  # glVertexAttribIPointer, glVertexAttribLPointer
                    _set_function(
                        _location,
                        _element_number,
                        _element_type,
                        _stride,
                        _offset
                    )

                glEnableVertexAttribArray(_location)
                glVertexAttribDivisor(_location, divisor)
                _offset += _location_size

            if _stride < _offset:  # 偏量大于缓存步长
                raise ValueError('buffer 步长不匹配，注意是否为显卡开启了双精度')

        except StopIteration:
            raise ValueError('attribute 数量不足，一般情况下显卡使用的是 float')
