"""
缓存对象

缓存在内存中的结构:

┌───┬───┬───┬───┬───┬───┬───┬───┬───┐   ...   ┌───┬───┬───┐
│ 1 │ 2 │ 3 │ 4 │ 5 │ 6 │ 7 │ 8 │ 9 │   ...   │n─2│n─1│ n │ elements = n
├───┴───┴───┼───┴───┴───┼───┴───┴───┤   ...   ├───┴───┴───┤
│     1     │     2     │     3     │   ...   │     m     │ component = 3
└───────────┴───────────┴───────────┘   ...   └───────────┘ groups = m
"""

import ctypes
import itertools

from ..opengl import *
from ..system import Array, Type, OpenGLObject


class Buffer(OpenGLObject):
    Array = 'array'
    Element = 'element'
    Uniform = 'uniform'
    Texture = 'texture'
    Sampler = 'sampler'

    Static = 'static'
    Dynamic = 'dynamic'
    Stream = 'stream'

    _BUFFER_GL_TYPES = {
        Type.Byte: GL_BYTE,
        Type.Short: GL_SHORT,
        Type.Int: GL_INT,

        Type.Char: GL_UNSIGNED_BYTE,
        Type.UByte: GL_UNSIGNED_BYTE,
        Type.UShort: GL_UNSIGNED_SHORT,
        Type.UInt: GL_UNSIGNED_INT,

        Type.Float: GL_FLOAT,
        Type.Double: GL_DOUBLE
    }

    _BUFFER_TARGETS = {
        Array: GL_ARRAY_BUFFER,
        Element: GL_ELEMENT_ARRAY_BUFFER,
        Uniform: GL_UNIFORM_BUFFER,
        Texture: GL_TEXTURE_BUFFER,
        Sampler: GL_SAMPLER_BUFFER
    }

    _BUFFER_DRAW_MODES = {
        Static: GL_STATIC_DRAW,
        Dynamic: GL_DYNAMIC_DRAW,
        Stream: GL_STREAM_DRAW
    }

    def __init__(self, data, data_type=None, *, target, mode):
        """
        接受 data target mode 三个参数时，要求 data 是 Array
        接受 data data_type target mode 四个参数时，要求 data 是长度
        """
        self._buffer_type = ''
        self._buffer_size = 0
        self._buffer_bytes = 0
        self._buffer_target = ''
        self._buffer_mode = ''

        self._buffer_c_type = None
        self._buffer_e_bytes = 0

        self._buffer_gl_type = ''
        self._buffer_gl_target = ''
        self._buffer_gl_mode = ''

        OpenGLObject.__init__(self, data, data_type, target, mode)

    def _initial(self, data, data_type, target, mode):
        self._buffer_id = ctypes.c_uint()
        glGenBuffers(1, self._buffer_id)
        if not self._buffer_id:
            raise OpenGLError('无法创建(Buffer)缓存')

        self._string = '<buffer_{}>'.format(self._buffer_id.value)
        if data_type:
            self.buffer_orphan(data, data_type, target, mode)
        else:
            self.buffer_rebuild(data, target, mode)

    @property
    def _as_parameter_(self):
        return self._buffer_id

    def _release(self):
        glDeleteBuffers(1, self._buffer_id)

    def buffer_bind(self):
        glBindBuffer(self._buffer_gl_target, self._buffer_id)

    def buffer_rebuild(self, data, target=None, mode=None):
        """ 重写 buffer 的数据 """

        _data_type = data.array_type

        # 强制要求 Array 的类型与 Buffer 类型相同
        # 所以没有 Type.Long, Type.Long2, Type.Double2
        # char 可以用 unsigned byte 代替
        assert _data_type not in (Type.Long, Type.Long2, Type.Double2)

        self._buffer_type = _data_type
        (self._buffer_c_type, self._buffer_e_bytes
         ) = Type.C_TYPES[_data_type]
        self._buffer_size = data.array_size
        self._buffer_bytes = data.array_bytes
        self._buffer_gl_type = self._BUFFER_GL_TYPES[_data_type]

        if target:
            self._buffer_target = target
            self._buffer_gl_target = self._BUFFER_TARGETS[target]

        if mode:
            self._buffer_mode = mode
            self._buffer_gl_mode = self._BUFFER_DRAW_MODES[mode]

        if data or target or mode:
            glBindBuffer(self._buffer_gl_target, self._buffer_id)
            glBufferData(
                self._buffer_gl_target, self._buffer_bytes, data,
                self._buffer_gl_mode
            )

    def buffer_orphan(self, size, data_type, target=None, mode=None):
        """ 空的 buffer """

        self._buffer_type = data_type
        (self._buffer_c_type, self._buffer_e_bytes
         ) = Type.C_TYPES[data_type]
        self._buffer_size = size
        self._buffer_bytes = size * self._buffer_e_bytes
        self._buffer_gl_type = self._BUFFER_GL_TYPES[data_type]

        if target:
            self._buffer_target = target
            self._buffer_gl_target = self._BUFFER_TARGETS[target]

        if mode:
            self._buffer_mode = mode
            self._buffer_gl_mode = self._BUFFER_DRAW_MODES[mode]

        glBindBuffer(self._buffer_gl_target, self._buffer_id)
        glBufferData(
            self._buffer_gl_target, self._buffer_bytes, 0,
            self._buffer_gl_mode
        )

    def buffer_read(self, result=None):
        """
        将显卡的数据提取到 buffer 的 array 里
        如果不是必须刷新的情况，一般都不会用到这个函数
        比如由显卡进行了 buffer 数据操作
        """
        glBindBuffer(self._buffer_gl_target, self._buffer_id)

        _inner_data = glMapBufferRange(  # 这里拿到的是一个整型
            self._buffer_gl_target, 0, self._buffer_bytes, GL_MAP_READ_BIT
        )

        if not _inner_data:
            raise OpenGLError('不能映射当前缓存')

        if not result:  # 如果没有参数，就是默认的自身 cache 了
            result = self.buffer_cache

            if result.array_size != self._buffer_size:  # 必须不一样才能动手
                result.array_new_size(self._buffer_size)

        result.array_from(_inner_data)  # 非安全性读取
        glUnmapBuffer(self._buffer_gl_target)

    def buffer_write(self, data, offset=0):
        if not data:
            raise ValueError('不能写入空值')

        assert data.array_type == self._buffer_type

        _end_size = data.array_size + offset

        if _end_size > self._buffer_size:
            _write_bytes = (self._buffer_size - offset) * self._buffer_e_bytes
        else:
            _write_bytes = data.array_bytes

        _bytes_offset = offset * self._buffer_e_bytes  # 获取字节偏移的个数

        glBindBuffer(self._buffer_gl_target, self._buffer_id)
        glBufferSubData(
            self._buffer_gl_target, _bytes_offset, _write_bytes, data
        )

    def buffer_clear(self, offset=0, length=0, chunk=None) -> None:
        if not length:
            length = self._buffer_size - offset

        length *= self._buffer_e_bytes

        glBindBuffer(self._buffer_gl_target, self._buffer_id)

        _inner_data = glMapBufferRange(
            self._buffer_gl_target, 0, self._buffer_bytes, GL_MAP_WRITE_BIT
        )

        if not _inner_data:
            raise OpenGLError('不能映射当前缓存')

        _inner_data = Array.array_at(
            _inner_data, self._buffer_size, self._buffer_type
        )

        if chunk:
            _position = offset * self._buffer_e_bytes
            _chunk = itertools.cycle(bytes(chunk))

            for _ in range(length):
                _inner_data[_position] = next(_chunk)
                _position += 1

        else:
            ctypes.memset(_inner_data.array_offset(offset), 0, length)

        glUnmapBuffer(self._buffer_gl_target)

    @property
    def buffer_type(self):
        return self._buffer_type

    @property
    def buffer_size(self):
        return self._buffer_size

    @property
    def buffer_bytes(self):
        return self._buffer_bytes

    @property
    def buffer_cache(self):
        if hasattr(self, '_buffer_cache'):
            return self._buffer_cache
        else:
            _array = Array(
                size=self._buffer_size, data_type=self._buffer_type
            )
            setattr(self, '_buffer_cache', _array)
            return _array


def buffer_bind_location(self, location_generator, divisor):
    _offset, _stride = 0, self._buffer_group_bytes
    try:
        while _stride > _offset:
            (_location, _element_number, _element_type, _location_size,
             _normalizable, _set_function) = next(location_generator)

            if (_element_type != self._buffer_gl_type or
                    # type 相同 size 也相同，因此这里不检查 element_size 了
                    _element_number > self._buffer_groups or
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


def bind_buffer_with_attribute():
    raise NotImplementedError
