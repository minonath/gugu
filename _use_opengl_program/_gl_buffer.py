import typing

from _use_opengl_program._gl_wrap import *
from _use_opengl_program._gl_info import SomeInfo
from _use_opengl_program._math_array import Array


class Buffer(object):
    """
    缓存对象

    缓存在内存中的结构:

    |---|---|---|---|---|---|---|---|---|   ...   |---|---|---|
    | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |   ...   |n-2|n-1| n | <- elements
    |---|---|---|---|---|---|---|---|---|   ...   |---|---|---|
    |     1     |     2     |     3     |   ...   |     m     | <- groups
    |-----------|-----------|-----------|   ...   |-----------|

    buffer_id:              缓存在显卡中的序列号，由显卡返回的序列确定

    buffer_element_number:  元素的数量（上图的 n ），即给定数组的元素个数
    buffer_group_number:    buffer_element_number ➗ buffer_group_contain

    buffer_element_size:    由 buffer_type 确定，显卡只接受 1 2 4 三个数
    buffer_group_size:      buffer_element_size ✖ buffer_group_contain
    buffer_size:            buffer_element_size ✖ buffer_element_number

    buffer_type:            缓存种类标记
    buffer_target:          缓存对象标记
    buffer_mode:            绘制模式标记
    """

    def __init__(self, data: typing.Union[list, tuple, int], buffer_type: int,
                 buffer_target: int, buffer_mode: int, group_length=1):
        """
        缓存对象

        data:           List[int or float] / Tuple[int or float]
        group_length:   表示缓存中每组元素包含的元素个数
        buffer_type:    GL_BYTE / GL_SHORT / GL_INT / GL_FLOAT / GL_DOUBLE /
                        GL_UNSIGNED_BYTE / GL_UNSIGNED_SHORT / GL_UNSIGNED_INT
        buffer_target:  GL_ARRAY_BUFFER, GL_ELEMENT_ARRAY_BUFFER
        buffer_mode:    GL_STATIC_DRAW / GL_DYNAMIC_DRAW / GL_STREAM_DRAW
        """
        _element_type = SomeInfo.get_c_type_by_type(buffer_type)
        _element_size = SomeInfo.get_size_by_type(buffer_type)

        if isinstance(data, int):  # 创建一个长度的空 Buffer
            _element_number, data = data, 0
        else:  # 重新定义 data，成为 ctypes.Array
            _element_number = len(data)
            data = (_element_type * _element_number)(*data)

        _byte_number = _element_size * _element_number

        _buffer_id = ctypes.c_uint()  # GL u int()
        glGenBuffers(1, _buffer_id)

        if not _buffer_id:
            raise OpenGLError('无法创建(Buffer)缓存')

        glBindBuffer(buffer_target, _buffer_id)
        glBufferData(buffer_target, _byte_number, data, buffer_mode)

        self._as_parameter_ = _buffer_id  # _as_parameter_ 作为 ctypes 传递专用
        self._buffer_size = _byte_number
        self._buffer_length = _element_number
        self._buffer_group_number = _element_number // group_length
        # self._buffer_byte_length
        # self._buffer_element_length = 1
        self._buffer_group_length = group_length
        # self._buffer_byte_size = 1
        self._buffer_element_size = _element_size
        self._buffer_group_size = _element_size * group_length
        # self._buffer_byte_type = ctypes.c_ubyte
        self._buffer_element_type = _element_type
        # self._buffer_group_type
        self._buffer_type = buffer_type
        self._buffer_target = buffer_target
        self._buffer_mode = buffer_mode

        self.__string__ = '<Buffer:{} size:{} ({} | {} | {})>'.format(
            _buffer_id.value, _byte_number,
            SomeInfo.get_name_by_type(buffer_type),
            SomeInfo.get_name_by_type(buffer_target),
            SomeInfo.get_name_by_type(buffer_mode)
        )

    @property
    def buffer_group_number(self):
        return self._buffer_group_number

    @property
    def buffer_type(self):
        return self._buffer_type

    def __repr__(self):
        return self.__string__

    def buffer_bind_location(self, location_generator: typing.Generator,
                             divisor: int) -> None:
        _offset, _stride = 0, self._buffer_group_size
        try:
            while _stride > _offset:
                (_location, _element_number, _element_type, _location_size,
                 _normalizable, _set_function) = next(location_generator)

                if (_element_type != self._buffer_type or
                        # type 相同 size 也相同，因此这里不检查 element_size 了
                        _element_number > self._buffer_group_length or
                        _location_size > self._buffer_group_size):
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

    def buffer_bind(self) -> None:
        glBindBuffer(self._buffer_target, self._as_parameter_)

    def buffer_write(self, data: Array, element_offset=0) -> None:
        if not data:
            raise ValueError('不能写入空值')

        element_offset *= self._buffer_element_size  # 偏移的元素个数

        # 不考虑格式问题，反正都能写入
        if data.array_size + element_offset > self._buffer_size:
            raise OverflowError('写入数据长度超过了缓冲区大小')

        glBindBuffer(self._buffer_target, self._as_parameter_)
        glBufferSubData(
            self._buffer_target, element_offset, data.array_size, data
        )

    def buffer_read(self, length=0, element_offset=0, result=None) -> Array:
        # 读取需要考虑格式问题
        if not length:  # size 表示的是读取的长度
            length = self._buffer_length - element_offset

        if (element_offset < 0 or
                element_offset + length > self._buffer_length):
            raise OverflowError('访问数据超出范围')

        glBindBuffer(self._buffer_target, self._as_parameter_)

        _buffer = glMapBufferRange(  # 读取的 _buffer 默认为 c_ubyte
            self._buffer_target,
            element_offset * self._buffer_element_size,
            length * self._buffer_element_size,
            GL_MAP_READ_BIT
        )

        if not _buffer:
            raise OpenGLError('不能映射当前缓存')

        if not result:
            result = Array(
                length=length, _type=self._buffer_element_type
            )

        if result.array_element_type != ctypes.c_ubyte:
            # 读取的 _buffer 默认为 c_ubyte
            _buffer = ctypes.cast(
                _buffer, ctypes.POINTER(result.array_element_type)
            )

        if result.array_length < length:
            raise ValueError('%s 的长度不足' % result.__repr__())

        result[:length] = _buffer[:length]  # 要确保 result 有足够的位置
        glUnmapBuffer(self._buffer_target)
        return result

    def buffer_clear(self, length=0, offset=0, chunk=None) -> None:
        if not length:
            length = self._buffer_length - offset

        if not chunk:
            chunk = Array(0, _type=self._buffer_element_type)

        _chunk_length = chunk.array_length
        _chunk_number, _exactly = divmod(length, _chunk_length)

        if _exactly:
            raise ValueError('复数的 chunk 不能填满 buffer')

        glBindBuffer(self._buffer_target, self._as_parameter_)

        _buffer = glMapBufferRange(
            self._buffer_target, 0, self._buffer_size, GL_MAP_WRITE_BIT
        )

        if not _buffer:
            raise OpenGLError('不能映射当前缓存')

        if chunk.array_element_type != ctypes.c_ubyte:
            _buffer = ctypes.cast(
                _buffer, ctypes.POINTER(chunk.array_element_type)
            )

        for _y in range(_chunk_number):
            _z = _chunk_length * _y + offset
            for _x in range(_chunk_length):
                _buffer[_z + _x] = chunk[_x]

        glUnmapBuffer(self._buffer_target)

    """
    def buffer_bind_to_storage_block(self, binding, offset=0, size=0) -> None:
        if not size:
            size = self._buffer_size - offset

        # 和 UniformBlock 一样的绑定方法
        # 这里是 ShaderStorageBufferObject 的绑定方法，它的储存量更大
        # 不过由于比较新，相关内容出现的比较晚，不需要单独设置
        # ShaderStorageBufferObject 的 binding 是在 shader 里直接指定的
        glBindBufferRange(
            GL_SHADER_STORAGE_BUFFER, binding, self, offset, size
        )
    """

    def buffer_orphan(self) -> None:
        """
        理论上，这个函数不会起到任何作用，因为在 buffer 创建的时候已经做好了
        但是，其他 buffer 回收后会造成显存碎片，这个操作可以重新调整空间
        """
        glBindBuffer(self._buffer_target, self._as_parameter_)
        glBufferData(
            self._buffer_target, self._buffer_size, 0, self._buffer_mode
        )
