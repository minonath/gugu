import ctypes

from ._buffer import Buffer
from ..system import Array, Type, OpenGLObject
from ..opengl import *

_normal = glVertexAttribPointer
_integer = glVertexAttribIPointer
_long = glVertexAttribLPointer

_ATTRIB_TYPES = {
    # size, type, stride, normalize, setter, alloc
    GL_INT: (1, Type.Int, 4, False, _integer, 1),
    GL_INT_VEC2: (2, Type.Int, 8, False, _integer, 1),
    GL_INT_VEC3: (3, Type.Int, 12, False, _integer, 1),
    GL_INT_VEC4: (4, Type.Int, 16, False, _integer, 1),
    GL_UNSIGNED_INT: (1, Type.UInt, 4, False, _integer, 1),
    GL_UNSIGNED_INT_VEC2: (2, Type.UInt, 8, False, _integer, 1),
    GL_UNSIGNED_INT_VEC3: (3, Type.UInt, 12, False, _integer, 1),
    GL_UNSIGNED_INT_VEC4: (4, Type.UInt, 16, False, _integer, 1),
    GL_FLOAT: (1, Type.Float, 4, True, _normal, 1),
    GL_FLOAT_VEC2: (2, Type.Float, 8, True, _normal, 1),
    GL_FLOAT_VEC3: (3, Type.Float, 12, True, _normal, 1),
    GL_FLOAT_VEC4: (4, Type.Float, 16, True, _normal, 1),
    # version 410 以上才可以使用 double
    GL_DOUBLE: (1, Type.Double, 8, False, _long, 1),
    GL_DOUBLE_VEC2: (2, Type.Double, 16, False, _long, 1),
    GL_DOUBLE_VEC3: (3, Type.Double, 24, False, _long, 1),
    GL_DOUBLE_VEC4: (4, Type.Double, 32, False, _long, 1),
    # 一般不考虑 attribute 输入矩阵的情况，但是万一呢
    GL_FLOAT_MAT2: (4, Type.Float, 16, True, _normal, 2),
    GL_FLOAT_MAT2x3: (6, Type.Float, 24, True, _normal, 2),
    GL_FLOAT_MAT2x4: (8, Type.Float, 32, True, _normal, 2),
    GL_FLOAT_MAT3x2: (6, Type.Float, 24, True, _normal, 3),
    GL_FLOAT_MAT3: (9, Type.Float, 36, True, _normal, 3),
    GL_FLOAT_MAT3x4: (12, Type.Float, 48, True, _normal, 3),
    GL_FLOAT_MAT4x2: (8, Type.Float, 32, True, _normal, 4),
    GL_FLOAT_MAT4x3: (12, Type.Float, 48, True, _normal, 4),
    GL_FLOAT_MAT4: (16, Type.Float, 64, True, _normal, 4),
    # alloc 表示行数，两行矩阵就占用两个
    GL_DOUBLE_MAT2: (4, Type.Double, 32, False, _long, 2),
    GL_DOUBLE_MAT2x3: (6, Type.Double, 48, False, _long, 2),
    GL_DOUBLE_MAT2x4: (8, Type.Double, 64, False, _long, 2),
    GL_DOUBLE_MAT3x2: (6, Type.Double, 48, False, _long, 3),
    GL_DOUBLE_MAT3: (9, Type.Double, 72, False, _long, 3),
    GL_DOUBLE_MAT3x4: (12, Type.Double, 96, False, _long, 3),
    GL_DOUBLE_MAT4x2: (8, Type.Double, 64, False, _long, 4),
    GL_DOUBLE_MAT4x3: (12, Type.Double, 96, False, _long, 4),
    GL_DOUBLE_MAT4: (16, Type.Double, 128, False, _long, 4),
}


class Attribute(OpenGLObject):
    """
    program 中的输入变量

    attrib_location:        输入变量的位置
    attrib_array_size:      输入变量是否为数组，以及数组的长度
    attrib_element_nums:    输入变量含有的元素个数
    attrib_element_type:    输入变量含有的元素类型
    attrib_size:            attrib_element_size ✖ attrib_element_number
    attrib_normalizable:    输入的变量是否进行单位化，作为矩阵输入的四元数需要单位化
    attrib_set_function:    输入函数
    attrib_occupy           占用 location 的数量
    """

    def __init__(self, attrib_location, attrib_number, attrib_type):
        self._attrib_location = attrib_location
        self._attrib_number = attrib_number
        self._attrib_gl_type = attrib_type

        (self._attrib_size, self._attrib_type, self._attrib_bytes,
         self._attrib_normalizable, self._attrib_gl_setter,
         self._attrib_gl_alloc) = _ATTRIB_TYPES[attrib_type]

        self._attrib_c_type, _ = Type.C_TYPES[self._attrib_type]
        OpenGLObject.__init__(self)
        if attrib_number > 1:
            self._string = '<attribute_{} type={}x{}x{}>'.format(
                self._attrib_location, self._attrib_type,
                self._attrib_size, self._attrib_number
            )
        else:
            self._string = '<attribute_{} type={}x{}>'.format(
                self._attrib_location,
                self._attrib_type, self._attrib_size
            )

    def _initial(self):
        pass

    def _release(self):
        pass


def attribute_get_info(self):
    if self._attrib_number == 1:
        yield (
            self._attrib_location,
            self._attrib_size,
            self._attrib_c_type,
            self._attrib_bytes,
            self._attrib_normalizable,
            self._attrib_gl_setter
        )

    else:
        for _i in range(self._attrib_number):
            yield (
                self._attrib_location + _i * self._attrib_gl_alloc,
                self._attrib_size,
                self._attrib_c_type,
                self._attrib_bytes,
                self._attrib_normalizable,
                self._attrib_gl_setter
            )


# class Varying(object):
#     """
#     仅在显卡内部流转的变量类型
#
#     因为无法读取，所以没什么作用，OpenGL 3.0 后移除了
#     """
#
#     def __init__(self, index, size):
#         self._string = '<Varying:{} size:{}>'.format(index, size)
#
#     def __repr__(self):
#         return self._string


_Getter = 'glGetUniform%sv'
_Setter = 'glProgramUniform%sv'
_Matrix = 'glProgramUniformMatrix%sv'

_Gi, _Gu, _Gf, _Gd = (gl_getattr(_Getter % m) for m in ('i', 'ui', 'f', 'd'))

(_S1i, _S2i, _S3i, _S4i, _S1u, _S2u, _S3u, _S4u, _S1f, _S2f, _S3f, _S4f,
 _S1d, _S2d, _S3d, _S4d) = (gl_getattr(_Setter % m) for m in (
    '1i', '2i', '3i', '4i', '1ui', '2ui', '3ui', '4ui',
    '1f', '2f', '3f', '4f', '1d', '2d', '3d', '4d'))

(_M2f, _M2x3f, _M2x4f, _M3x2f, _M3f, _M3x4f, _M4x2f, _M4x3f, _M4f,
 _M2d, _M2x3d, _M2x4d, _M3x2d, _M3d, _M3x4d, _M4x2d, _M4x3d, _M4d
 ) = (gl_getattr(_Matrix % m) for m in (
    '2f', '2x3f', '2x4f', '3x2f', '3f', '3x4f', '4x2f', '4x3f', '4f',
    '2d', '2x3d', '2x4d', '3x2d', '3d', '3x4d', '4x2d', '4x3d', '4d'))

_UNIFORM_TYPES = {
    GL_BOOL: (1, Type.Int, False, _Gi, _S1i, 1),
    GL_BOOL_VEC2: (2, Type.Int, False, _Gi, _S2i, 1),
    GL_BOOL_VEC3: (3, Type.Int, False, _Gi, _S3i, 1),
    GL_BOOL_VEC4: (4, Type.Int, False, _Gi, _S4i, 1),
    GL_INT: (1, Type.Int, False, _Gi, _S1i, 1),
    GL_INT_VEC2: (2, Type.Int, False, _Gi, _S2i, 1),
    GL_INT_VEC3: (3, Type.Int, False, _Gi, _S3i, 1),
    GL_INT_VEC4: (4, Type.Int, False, _Gi, _S4i, 1),
    GL_UNSIGNED_INT: (1, Type.UInt, False, _Gu, _S1u, 1),
    GL_UNSIGNED_INT_VEC2: (2, Type.UInt, False, _Gu, _S2u, 1),
    GL_UNSIGNED_INT_VEC3: (3, Type.UInt, False, _Gu, _S3u, 1),
    GL_UNSIGNED_INT_VEC4: (4, Type.UInt, False, _Gu, _S4u, 1),
    GL_FLOAT: (1, Type.Float, False, _Gf, _S1f, 1),
    GL_FLOAT_VEC2: (2, Type.Float, False, _Gf, _S2f, 1),
    GL_FLOAT_VEC3: (3, Type.Float, False, _Gf, _S3f, 1),
    GL_FLOAT_VEC4: (4, Type.Float, False, _Gf, _S4f, 1),
    GL_DOUBLE: (1, Type.Double, False, _Gd, _S1d, 1),
    GL_DOUBLE_VEC2: (2, Type.Double, False, _Gd, _S2d, 1),
    GL_DOUBLE_VEC3: (3, Type.Double, False, _Gd, _S3d, 1),
    GL_DOUBLE_VEC4: (4, Type.Double, False, _Gd, _S4d, 1),
    # 这些涉及纹理的都是整数
    GL_SAMPLER_2D: (1, Type.Int, False, _Gi, _S1i, 1),
    GL_SAMPLER_2D_ARRAY: (1, Type.Int, False, _Gi, _S1i, 1),
    GL_SAMPLER_3D: (1, Type.Int, False, _Gi, _S1i, 1),
    GL_SAMPLER_2D_SHADOW: (1, Type.Int, False, _Gi, _S1i, 1),
    GL_SAMPLER_2D_MULTISAMPLE: (1, Type.Int, False, _Gi, _S1i, 1),
    GL_SAMPLER_CUBE: (1, Type.Int, False, _Gi, _S1i, 1),
    GL_IMAGE_2D: (1, Type.Int, False, _Gi, _S1i, 1),  # 330 后封了这个
    # 接下来是矩阵
    GL_FLOAT_MAT2: (4, Type.Float, True, _Gf, _M2f, 2),
    GL_FLOAT_MAT2x3: (6, Type.Float, True, _Gf, _M2x3f, 2),
    GL_FLOAT_MAT2x4: (8, Type.Float, True, _Gf, _M2x4f, 2),
    GL_FLOAT_MAT3x2: (6, Type.Float, True, _Gf, _M3x2f, 3),
    GL_FLOAT_MAT3: (9, Type.Float, True, _Gf, _M3f, 3),
    GL_FLOAT_MAT3x4: (12, Type.Float, True, _Gf, _M3x4f, 3),
    GL_FLOAT_MAT4x2: (8, Type.Float, True, _Gf, _M4x2f, 4),
    GL_FLOAT_MAT4x3: (12, Type.Float, True, _Gf, _M4x3f, 4),
    GL_FLOAT_MAT4: (16, Type.Float, True, _Gf, _M4f, 4),
    GL_DOUBLE_MAT2: (4, Type.Double, True, _Gd, _M2d, 2),
    GL_DOUBLE_MAT2x3: (6, Type.Double, True, _Gd, _M2x3d, 2),
    GL_DOUBLE_MAT2x4: (8, Type.Double, True, _Gd, _M2x4d, 2),
    GL_DOUBLE_MAT3x2: (6, Type.Double, True, _Gd, _M3d, 3),
    GL_DOUBLE_MAT3: (9, Type.Double, True, _Gd, _M3x2d, 3),
    GL_DOUBLE_MAT3x4: (12, Type.Double, True, _Gd, _M3x4d, 3),
    GL_DOUBLE_MAT4x2: (8, Type.Double, True, _Gd, _M4x2d, 4),
    GL_DOUBLE_MAT4x3: (12, Type.Double, True, _Gd, _M4x3d, 4),
    GL_DOUBLE_MAT4: (16, Type.Double, True, _Gd, _M4d, 4),
}


class Uniform(OpenGLObject):
    def __init__(self, program_id, location, uniform_count, uniform_type):
        self._uniform_program = program_id
        self._uniform_location = location
        self._uniform_count = uniform_count
        self._uniform_gl_type = uniform_type

        (self._uniform_size, self._uniform_type, self._uniform_is_matrix,
         self._uniform_gl_getter, self._uniform_gl_setter,
         self._uniform_gl_alloc) = _UNIFORM_TYPES[uniform_type]
        self._uniform_c_type, _e_bytes = Type.C_TYPES[self._uniform_type]
        self._uniform_bytes = _e_bytes * self._uniform_size

        OpenGLObject.__init__(self)
        if uniform_count > 1:
            self._string = '<uniform_{} type={}x{}x{}>'.format(
                self._uniform_location, self._uniform_type,
                self._uniform_size, self._uniform_count
            )
        else:
            self._string = '<uniform_{} type={}x{}>'.format(
                self._uniform_location,
                self._uniform_type, self._uniform_size
            )

    def _initial(self):
        pass

    def _release(self):
        pass

    @property
    def uniform_cache(self):
        if hasattr(self, '_uniform_cache'):
            return self._uniform_cache
        else:
            _array = Array(  # 用于获取自身内容的缓存
                size=self._uniform_size * self._uniform_count,
                data_type=self._uniform_type
            )
            setattr(self, '_uniform_cache', _array)
            return _array

    def uniform_read(self, data=None):
        if not data:
            data = self.uniform_cache

        for _i in range(self._uniform_count):
            self._uniform_gl_getter(
                self._uniform_program,
                self._uniform_location + _i * self._uniform_gl_alloc,
                data.array_offset(_i * self._uniform_size)
            )

    def uniform_write(self, data):
        print(self._uniform_bytes * self._uniform_count)
        assert data.array_bytes >= self._uniform_bytes * self._uniform_count

        if self._uniform_is_matrix:
            for _i in range(self._uniform_count):
                self._uniform_gl_setter(
                    self._uniform_program,
                    self._uniform_location + _i * self._uniform_gl_alloc,
                    self._uniform_count, False,
                    data.array_offset(_i * self._uniform_size)
                )

        else:
            for _i in range(self._uniform_count):
                self._uniform_gl_setter(
                    self._uniform_program,
                    self._uniform_location + _i * self._uniform_gl_alloc,
                    self._uniform_count,
                    data.array_offset(_i * self._uniform_size)
                )


class UniformBlock(OpenGLObject):
    _uniform_binding = 0

    def __init__(self, program_id, uniform_id, block_bytes):
        self._uniform_program = program_id
        self._uniform_id = uniform_id
        self._uniform_bytes = block_bytes

        UniformBlock._uniform_binding += 1
        self._uniform_binding = UniformBlock._uniform_binding
        OpenGLObject.__init__(
            self, program_id, uniform_id, self._uniform_binding, block_bytes
        )
        self._string = '<uniform_block_{} bytes={} bind={}>'.format(
            self._uniform_id, self._uniform_bytes, self._uniform_binding
        )

    def _initial(self, program_id, uniform_id, binding_id, size):
        # 通过这个步骤绑定 UniformBufferObject，然后通过修改 Buffer 的值来改变
        glUniformBlockBinding(program_id, uniform_id, binding_id)
        _buffer = Buffer(
            size, Type.UByte, target=Buffer.Uniform, mode=Buffer.Dynamic
        )
        glBindBufferRange(
            GL_UNIFORM_BUFFER, self._uniform_binding, _buffer, 0, size
        )
        # 我觉得用 glBindBufferBase 会更好，虽然 glBindBufferRange 更有适用性
        glBindBufferBase(GL_UNIFORM_BUFFER, self._uniform_binding, _buffer)
        self._uniform_buffer = _buffer

    def _release(self):
        pass

    @property
    def uniform_cache(self):
        return self._uniform_buffer.buffer_cache

    def uniform_read(self, data=None):
        self._uniform_buffer.buffer_read(data)

    def uniform_write(self, data, offset=0):
        self._uniform_buffer.buffer_write(data, offset)


def program_get_member(program_id):
    """
    获取 program 的所有成员

    attribute 和 uniform 都有自己的位置偏量（location）
    默认的 location 是 4 个元素，实际上就是 shader 里的 vec4
    当一个成员的元素超过 4 个，会导致占用多个 location
    mat4 会占用 4 个 location，导致它的下一个成员的 location + 4
    attribute 是显卡程序自动从缓存读取的，读取操作是 glVertexAttribPointer
    因此会限制在 4 个元素以内，glVertexAttribPointer 的第二个参数也是 4 以内
    也就导致了 attribute 一般不使用数组（in vec4 meow[3] 这样）
    如果是数组，会占用多个 location，对于程序来说，访问变量的顺序就会出问题
    你需要准确把握 location 的位置，每 4 个元素 1 个偏移量
    作为数组出现的时候，_member_array 的值将会变成 1 以外的正整数
    通过 location + n * (member_element_number // 4) 来进行序列的访问
    member_element_number = _GL_TYPE_ELEMENT_NUMBER[_member_type.value]
    """
    _number = ctypes.c_int()  # GLint()
    _member_type = ctypes.c_uint()  # GL enum
    _member_array = ctypes.c_int()  # GLint()
    _NAME_LENGTH = 256
    _member_name = (ctypes.c_char * _NAME_LENGTH)()
    _member_name_size = ctypes.c_int()  # GLint()

    glGetProgramiv(program_id, GL_ACTIVE_ATTRIBUTES, _number)
    for _i in range(_number.value):
        glGetActiveAttrib(
            program_id, _i, _NAME_LENGTH, _member_name_size,
            _member_array, _member_type, _member_name
        )
        _location = glGetAttribLocation(program_id, _member_name)

        yield (
            _member_name[:_member_name_size.value].decode(),
            Attribute(_location, _member_array.value, _member_type.value)
        )

    # glGetProgramiv(program_id, GL_TRANSFORM_FEEDBACK_VARYINGS, _number)
    # for _i in range(_number.value):
    #     glGetTransformFeedbackVarying(
    #         program_id, _i, _NAME_LENGTH, _member_name_size,
    #         _member_array, _member_type, _member_name
    #     )
    #
    #     yield (_member_name[:_member_name_size.value].decode(),
    #            Varying(_i, _member_array.value))

    glGetProgramiv(program_id, GL_ACTIVE_UNIFORMS, _number)
    for _i in range(_number.value):
        glGetActiveUniform(
            program_id, _i, _NAME_LENGTH, _member_name_size,
            _member_array, _member_type, _member_name
        )
        _location = glGetUniformLocation(program_id, _member_name)

        if _location == -1:  # UniformBlock 的内部数据
            continue
        _name = _member_name[:_member_name_size.value].decode()
        _k = _name.find('[')
        if _k >0:
            _name = _name[:_k]  # 取消方框

        yield (_name, Uniform(
            program_id, _location, _member_array.value, _member_type.value
        ))

    glGetProgramiv(program_id, GL_ACTIVE_UNIFORM_BLOCKS, _number)
    for _i in range(_number.value):
        glGetActiveUniformBlockName(
            program_id, _i, _NAME_LENGTH, _member_name_size, _member_name
        )
        _index = glGetUniformBlockIndex(program_id, _member_name)
        glGetActiveUniformBlockiv(
            program_id, _index, GL_UNIFORM_BLOCK_DATA_SIZE, _member_array
        )

        yield (_member_name[:_member_name_size.value].decode(),
               UniformBlock(program_id, _index, _member_array.value))


__all__ = ['program_get_member']
