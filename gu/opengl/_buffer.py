import ctypes
import itertools

# from ._context import TYPE_TRANSLATE
# from ..opengl import *
# from ..system import Array, Type, OpenGLObject
# from ..matrix import
from .library import *

#
# class Type(object):
#     Byte = 'byte'
#     Short = 'short'
#     Int = 'int'
#     Long = 'long'
#     Long2 = 'longlong'
#
#     UByte = 'unsigned byte'
#     UShort = 'unsigned short'
#     UInt = 'unsigned int'
#     ULong = 'unsigned long'
#     ULong2 = 'unsigned longlong'
#
#     Char = 'char'
#     Float = 'float'
#     Double = 'double'
#     Double2 = 'longdouble'
#
#     C_TYPES = {  # all types
#         Byte: (ctypes.c_byte, ctypes.sizeof(ctypes.c_byte)),
#         Short: (ctypes.c_short, ctypes.sizeof(ctypes.c_short)),
#         Int: (ctypes.c_int, ctypes.sizeof(ctypes.c_int)),
#         Long: (ctypes.c_long, ctypes.sizeof(ctypes.c_long)),
#         Long2: (ctypes.c_longlong, ctypes.sizeof(ctypes.c_longlong)),
#
#         UByte: (ctypes.c_ubyte, ctypes.sizeof(ctypes.c_ubyte)),
#         UShort: (ctypes.c_ushort, ctypes.sizeof(ctypes.c_ushort)),
#         UInt: (ctypes.c_uint, ctypes.sizeof(ctypes.c_uint)),
#         ULong: (ctypes.c_ulong, ctypes.sizeof(ctypes.c_ulong)),
#         ULong2: (ctypes.c_ulonglong, ctypes.sizeof(ctypes.c_ulonglong)),
#
#         Char: (ctypes.c_char, ctypes.sizeof(ctypes.c_char)),
#         Float: (ctypes.c_float, ctypes.sizeof(ctypes.c_float)),
#         Double: (ctypes.c_double, ctypes.sizeof(ctypes.c_double)),
#         Double2: (ctypes.c_longdouble, ctypes.sizeof(ctypes.c_longdouble))
#     }
#
#
# TYPE_TRANSLATE = {
#     Type.Byte: GL_BYTE,
#     Type.Short: GL_SHORT,
#     Type.Int: GL_INT,
#
#     Type.Char: GL_UNSIGNED_BYTE,
#     Type.UByte: GL_UNSIGNED_BYTE,
#     Type.UShort: GL_UNSIGNED_SHORT,
#     Type.UInt: GL_UNSIGNED_INT,
#
#     Type.Float: GL_FLOAT,
#     Type.Double: GL_DOUBLE
# }
#
#
# class OldBuffer:
#     def __init__(self, data, data_type=None, *, target, mode):
#         """
#         接受 data target mode 三个参数时，要求 data 是 Array
#         接受 data data_type target mode 四个参数时，要求 data 是长度
#         """
#         self._buffer_type = ''
#         self._buffer_size = 0
#         self._buffer_bytes = 0
#         self._buffer_target = ''
#         self._buffer_mode = ''
#
#         self._buffer_c_type = None
#         self._buffer_e_bytes = 0
#
#         self._buffer_gl_type = 0
#         self._buffer_gl_target = 0
#         self._buffer_gl_mode = 0
#
#         self._buffer_id = ctypes.c_uint()
#         glGenBuffers(1, self._buffer_id)
#         if not self._buffer_id:
#             raise OpenGLError('无法创建(Buffer)缓存')
#
#         self._string = '<buffer_{}>'.format(self._buffer_id.value)
#         if data_type:
#             self.buffer_orphan(data, data_type, target, mode)
#         else:
#             self.buffer_rebuild(data, target, mode)
#
#     def _release(self):
#         glDeleteBuffers(1, self._buffer_id)
#
#     """ Bind """
#
#     def buffer_bind(self):
#         glBindBuffer(self._buffer_gl_target, self._buffer_id)
#
#     """ In/Out """
#
#     # @property
#     # def buffer_cache(self):
#     #     if hasattr(self, '_buffer_cache'):
#     #         return self._buffer_cache
#     #     else:
#     #         _array = Array(
#     #             size=self._buffer_size, data_type=self._buffer_type
#     #         )
#     #         setattr(self, '_buffer_cache', _array)
#     #         return _array
#
#     def buffer_rebuild(self, data, target=None, mode=None):
#         """ 重写 buffer 的数据 """
#
#         _data_type = data.array_type
#
#         # 强制要求 Array 的类型与 Buffer 类型相同
#         # 所以没有 Type.Long, Type.Long2, Type.Double2
#         # char 可以用 unsigned byte 代替
#         assert _data_type not in (Type.Long, Type.Long2, Type.Double2)
#
#         self._buffer_type = _data_type
#         (self._buffer_c_type, self._buffer_e_bytes
#          ) = Type.C_TYPES[_data_type]
#         self._buffer_size = data.array_size
#         self._buffer_bytes = data.array_bytes
#         self._buffer_gl_type = TYPE_TRANSLATE[_data_type]
#
#         if target:
#             self._buffer_target = target
#             self._buffer_gl_target = self._BUFFER_TARGETS[target]
#
#         if mode:
#             self._buffer_mode = mode
#             self._buffer_gl_mode = self._BUFFER_DRAW_MODES[mode]
#
#         if data or target or mode:
#             glBindBuffer(self._buffer_gl_target, self._buffer_id)
#             glBufferData(
#                 self._buffer_gl_target, self._buffer_bytes, data,
#                 self._buffer_gl_mode
#             )
#
#     def buffer_orphan(self, size, data_type, target=None, mode=None):
#         """ 空的 buffer """
#
#         self._buffer_type = data_type
#         (self._buffer_c_type, self._buffer_e_bytes
#          ) = Type.C_TYPES[data_type]
#         self._buffer_size = size
#         self._buffer_bytes = size * self._buffer_e_bytes
#         self._buffer_gl_type = TYPE_TRANSLATE[data_type]
#
#         if target:
#             self._buffer_target = target
#             self._buffer_gl_target = self._BUFFER_TARGETS[target]
#
#         if mode:
#             self._buffer_mode = mode
#             self._buffer_gl_mode = self._BUFFER_DRAW_MODES[mode]
#
#         glBindBuffer(self._buffer_gl_target, self._buffer_id)
#         glBufferData(
#             self._buffer_gl_target, self._buffer_bytes, 0,
#             self._buffer_gl_mode
#         )
#
#     def buffer_read(self, result=None):
#         """
#         将显卡的数据提取到 buffer 的 array 里
#         如果不是必须刷新的情况，一般都不会用到这个函数
#         比如由显卡进行了 buffer 数据操作
#         """
#         glBindBuffer(self._buffer_gl_target, self._buffer_id)
#
#         _inner_data = glMapBufferRange(  # 这里拿到的是一个整型
#             self._buffer_gl_target, 0, self._buffer_bytes, GL_MAP_READ_BIT
#         )
#
#         if not _inner_data:
#             raise OpenGLError('不能映射当前缓存')
#
#         if not result:  # 如果没有参数，就是默认的自身 cache 了
#             result = self.buffer_cache
#
#             if result.array_size != self._buffer_size:  # 必须不一样才能动手
#                 result.array_new_size(self._buffer_size)
#
#         result.array_from(_inner_data)  # 非安全性读取
#         glUnmapBuffer(self._buffer_gl_target)
#
#     def buffer_write(self, data, offset=0):
#         if not data:
#             raise ValueError('不能写入空值')
#
#         assert data.array_type == self._buffer_type
#
#         _end_size = data.array_size + offset
#
#         if _end_size > self._buffer_size:
#             _write_bytes = (self._buffer_size - offset) * self._buffer_e_bytes
#         else:
#             _write_bytes = data.array_bytes
#
#         _bytes_offset = offset * self._buffer_e_bytes  # 获取字节偏移的个数
#
#         glBindBuffer(self._buffer_gl_target, self._buffer_id)
#         glBufferSubData(
#             self._buffer_gl_target, _bytes_offset, _write_bytes, data
#         )
#
#     # def buffer_clear(self, offset=0, length=0, chunk=None) -> None:
#     #     if not length:
#     #         length = self._buffer_size - offset
#     #
#     #     length *= self._buffer_e_bytes
#     #
#     #     glBindBuffer(self._buffer_gl_target, self._buffer_id)
#     #
#     #     _inner_data = glMapBufferRange(
#     #         self._buffer_gl_target, 0, self._buffer_bytes, GL_MAP_WRITE_BIT
#     #     )
#     #
#     #     if not _inner_data:
#     #         raise OpenGLError('不能映射当前缓存')
#     #
#     #     _inner_data = Array.array_at(
#     #         _inner_data, self._buffer_size, self._buffer_type
#     #     )
#     #
#     #     if chunk:
#     #         _position = offset * self._buffer_e_bytes
#     #         _chunk = itertools.cycle(bytes(chunk))
#     #
#     #         for _ in range(length):
#     #             _inner_data[_position] = next(_chunk)
#     #             _position += 1
#     #
#     #     else:
#     #         ctypes.memset(_inner_data.array_offset(offset), 0, length)
#     #
#     #     glUnmapBuffer(self._buffer_gl_target)
#
#     """ Attribute """
#
#     @property
#     def buffer_type(self):
#         return self._buffer_type
#
#     @property
#     def buffer_size(self):
#         return self._buffer_size
#
#     @property
#     def buffer_bytes(self):
#         return self._buffer_bytes
#
#     @property
#     def buffer_target(self):
#         return self._buffer_target
#
#     @property
#     def buffer_mode(self):
#         return self._buffer_mode
#
#     @property
#     def buffer_c_type(self):
#         return self._buffer_c_type
#
#     @property
#     def buffer_e_bytes(self):
#         return self._buffer_e_bytes
#
#     @property
#     def buffer_gl_type(self):
#         return self._buffer_gl_type
#
#     @property
#     def buffer_gl_target(self):
#         return self._buffer_gl_target
#
#     @property
#     def buffer_gl_mode(self):
#         return self._buffer_gl_mode
#
#     @property
#     def _as_parameter_(self):
#         return self._buffer_id
#
#
# class VertexBuffer(Buffer):
#     def __init__(self, elements, data_type, data, component, dynamic=False):
#         self._buffer_stride = 0
#         self._buffer_vertices = 0
#         Buffer.__init__(self, elements, data_type, target=self.Array,
#                         mode=self.Dynamic if dynamic else self.Static)
#         self.buffer_write(data)  # ? 必须吗
#         self.buffer_split(component)
#
#     def buffer_split(self, component):
#         self._buffer_stride = self._buffer_e_bytes * component
#         self._buffer_vertices = self._buffer_size // component
#
#     @property
#     def buffer_stride(self):
#         return self._buffer_stride
#
#     @property
#     def buffer_vertices(self):
#         return self._buffer_vertices
#
#
# class IndexBuffer(VertexBuffer):
#     def __init__(self, data, dynamic=False):
#         Buffer.__init__(self, data, target=self.Element,
#                         mode=self.Dynamic if dynamic else self.Static)
#         self.buffer_split(1)


class Buffer:
    # 按照 OpenGL Programming Guide 的叙述，只有下面八组（十个）类型的缓冲区
    Array = 'GL_ARRAY_BUFFER'  # 顶点数组
    CopyRead = 'GL_COPY_READ_BUFFER'  # 拷贝缓冲区
    CopyWrite = 'GL_COPY_WRITE_BUFFER'  # 配合拷贝的目标区域
    DrawIndirect = 'GL_DRAW_INDIRECT_BUFFER'  # glDraw...Indirect 的偏量数组
    ElementArray = 'GL_ELEMENT_ARRAY_BUFFER'  # 索引数组
    PixelPack = 'GL_PIXEL_PACK_BUFFER'  # 读取数据
    PixelUnpack = 'GL_PIXEL_UNPACK_BUFFER'  # 放回数据
    Texture = 'GL_TEXTURE_BUFFER'  # 纹理
    TransformFeedback = 'GL_TRANSFORM_FEEDBACK_BUFFER'  # 顶点变换捕获
    Uniform = 'GL_UNIFORM_BUFFER'  # Uniform 格式缓存对象

    # 实际上，还有很多种类的缓冲区
    DispatchIndirect = 'GL_DISPATCH_INDIRECT_BUFFER'  # glDispatchCompute...
    AtomicCounter = 'GL_ATOMIC_COUNTER_BUFFER'  # 原子计数器
    ShaderStorage = 'GL_SHADER_STORAGE_BUFFER'  # 着色器存储
    Query = 'GL_QUERY_BUFFER'  # 查询对象
    Sampler = 'GL_SAMPLER_BUFFER'
    IntSampler = 'GL_INT_SAMPLER_BUFFER'
    UnsignedIntSampler = 'GL_UNSIGNED_INT_SAMPLER_BUFFER'
    Image = 'GL_IMAGE_BUFFER'

    # 可能还有其它的缓冲区，所以需要一个开放性的参数。

    # 缓冲区位置
    StreamDraw = 'GL_STREAM_DRAW'  # 只有单向数据，重新访问很麻烦的
    StreamRead = 'GL_STREAM_READ'
    StreamCopy = 'GL_STREAM_COPY'
    StaticDraw = 'GL_STATIC_DRAW'  # 单次使用
    StaticRead = 'GL_STATIC_READ'  # 单次使用，用于代码查询
    StaticCopy = 'GL_STATIC_COPY'  # 单次使用
    DynamicDraw = 'GL_DYNAMIC_DRAW'  # 高频率使用缓存绘制
    DynamicRead = 'GL_DYNAMIC_READ'  # 高频率读取缓存，用于代码查询
    DynamicCopy = 'GL_DYNAMIC_COPY'  # 高频率复制区

    def __init__(self):
        self._buffer_id = ctypes.c_uint()
        glGenBuffers(1, self._buffer_id)
        if not self._buffer_id:
            raise OpenGLError('无法创建(Buffer)缓存')

    def __del__(self):
        glDeleteBuffers(1, self._buffer_id)

    def bind(self, value, target=Array, mode=StaticDraw):
        pass
