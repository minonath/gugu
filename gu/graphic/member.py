import ctypes

from .buffer import BUFFER_TYPES, Buffer
from ..system import Array
from ..opengl import *

_normal = glVertexAttribPointer
_integer = glVertexAttribIPointer
_long = glVertexAttribLPointer

ATTRIB_TYPES = (
    # name, e_nums, e_type, stride, normalize, setter, occupy。
    ('GL_INT', 1, 'GL_INT', 4, False, _integer, 1),
    ('GL_INT_VEC2', 2, 'GL_INT', 8, False, _integer, 1),
    ('GL_INT_VEC3', 3, 'GL_INT', 12, False, _integer, 1),
    ('GL_INT_VEC4', 4, 'GL_INT', 16, False, _integer, 1),
    ('GL_UNSIGNED_INT', 1, 'GL_UNSIGNED_INT', 4, False, _integer, 1),
    ('GL_UNSIGNED_INT_VEC2', 2, 'GL_UNSIGNED_INT', 8, False, _integer, 1),
    ('GL_UNSIGNED_INT_VEC3', 3, 'GL_UNSIGNED_INT', 12, False, _integer, 1),
    ('GL_UNSIGNED_INT_VEC4', 4, 'GL_UNSIGNED_INT', 16, False, _integer, 1),
    ('GL_FLOAT', 1, 'GL_FLOAT', 4, True, _normal, 1),
    ('GL_FLOAT_VEC2', 2, 'GL_FLOAT', 8, True, _normal, 1),
    ('GL_FLOAT_VEC3', 3, 'GL_FLOAT', 12, True, _normal, 1),
    ('GL_FLOAT_VEC4', 4, 'GL_FLOAT', 16, True, _normal, 1),
    # version 410 以上才可以使用 double。
    ('GL_DOUBLE', 1, 'GL_DOUBLE', 8, False, _long, 1),
    ('GL_DOUBLE_VEC2', 2, 'GL_DOUBLE', 16, False, _long, 1),
    ('GL_DOUBLE_VEC3', 3, 'GL_DOUBLE', 24, False, _long, 1),
    ('GL_DOUBLE_VEC4', 4, 'GL_DOUBLE', 32, False, _long, 1),
    # 一般不考虑 attribute 输入矩阵的情况，但是万一呢。
    ('GL_FLOAT_MAT2', 4, 'GL_FLOAT', 16, True, _normal, 2),
    ('GL_FLOAT_MAT2x3', 6, 'GL_FLOAT', 24, True, _normal, 2),
    ('GL_FLOAT_MAT2x4', 8, 'GL_FLOAT', 32, True, _normal, 2),
    ('GL_FLOAT_MAT3x2', 6, 'GL_FLOAT', 24, True, _normal, 3),
    ('GL_FLOAT_MAT3', 9, 'GL_FLOAT', 36, True, _normal, 3),
    ('GL_FLOAT_MAT3x4', 12, 'GL_FLOAT', 48, True, _normal, 3),
    ('GL_FLOAT_MAT4x2', 8, 'GL_FLOAT', 32, True, _normal, 4),
    ('GL_FLOAT_MAT4x3', 12, 'GL_FLOAT', 48, True, _normal, 4),
    ('GL_FLOAT_MAT4', 16, 'GL_FLOAT', 64, True, _normal, 4),
    # occupy 表示行数，两行矩阵就占用两个。
    ('GL_DOUBLE_MAT2', 4, 'GL_DOUBLE', 32, False, _long, 2),
    ('GL_DOUBLE_MAT2x3', 6, 'GL_DOUBLE', 48, False, _long, 2),
    ('GL_DOUBLE_MAT2x4', 8, 'GL_DOUBLE', 64, False, _long, 2),
    ('GL_DOUBLE_MAT3x2', 6, 'GL_DOUBLE', 48, False, _long, 3),
    ('GL_DOUBLE_MAT3', 9, 'GL_DOUBLE', 72, False, _long, 3),
    ('GL_DOUBLE_MAT3x4', 12, 'GL_DOUBLE', 96, False, _long, 3),
    ('GL_DOUBLE_MAT4x2', 8, 'GL_DOUBLE', 64, False, _long, 4),
    ('GL_DOUBLE_MAT4x3', 12, 'GL_DOUBLE', 96, False, _long, 4),
    ('GL_DOUBLE_MAT4', 16, 'GL_DOUBLE', 128, False, _long, 4),
)

# print(program('texture')._program_member['m_proj[0]'].value)

ATTRIB_TYPES = dict((gl_getattr(m[0]), m) for m in ATTRIB_TYPES)


class Attribute(object):
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
        self._attrib_type = attrib_type

        (self._attrib_type_enum, self._attrib_element_nums,
         self._attrib_element_enum, self._attrib_bytes,
         self._attrib_normalizable, self._attrib_setter,
         self._attrib_occupy) = ATTRIB_TYPES[attrib_type]

        self._attrib_element_type = gl_getattr(self._attrib_element_enum)

    def __repr__(self):
        return '<attribute_{} type={}>'.format(
            self._attrib_location, self._attrib_type_enum)

    def attribute_get_info(self):
        if self._attrib_number == 1:
            yield (
                self._attrib_location,
                self._attrib_element_nums,
                self._attrib_element_type,
                self._attrib_bytes,
                self._attrib_normalizable,
                self._attrib_setter
            )

        else:
            for _i in range(self._attrib_number):
                yield (
                    self._attrib_location + _i * self._attrib_occupy,
                    self._attrib_element_nums,
                    self._attrib_element_type,
                    self._attrib_bytes,
                    self._attrib_normalizable,
                    self._attrib_setter
                )


class Varying(object):
    """
    仅在显卡内部流转的变量类型。

    因为无法读取，所以没什么作用，OpenGL 3.0 后移除了。
    """

    def __init__(self, index, size):
        self.__string__ = '<Varying:{} size:{}>'.format(index, size)

    def __repr__(self):
        return self.__string__


_getter = 'glGetUniform%sv'
_setter = 'glProgramUniform%sv'
_matrix = 'glProgramUniformMatrix%sv'

G_i, G_u, G_f, G_d = (gl_getattr(_getter % m) for m in ('i', 'ui', 'f', 'd'))

(S_1i, S_2i, S_3i, S_4i, S_1u, S_2u, S_3u, S_4u, S_1f, S_2f, S_3f, S_4f,
 S_1d, S_2d, S_3d, S_4d) = (gl_getattr(_setter % m) for m in (
    '1i', '2i', '3i', '4i', '1ui', '2ui', '3ui', '4ui',
    '1f', '2f', '3f', '4f', '1d', '2d', '3d', '4d'))

(M_2f, M_2x3f, M_2x4f, M_3x2f, M_3f, M_3x4f, M_4x2f, M_4x3f, M_4f,
 M_2d, M_2x3d, M_2x4d, M_3x2d, M_3d, M_3x4d, M_4x2d, M_4x3d, M_4d
 ) = (gl_getattr(_matrix % m) for m in (
    '2f', '2x3f', '2x4f', '3x2f', '3f', '3x4f', '4x2f', '4x3f', '4f',
    '2d', '2x3d', '2x4d', '3x2d', '3d', '3x4d', '4x2d', '4x3d', '4d'))

UNIFORM_TYPES = (  # glGetUniform glProgramUniform
    # name, e_nums, e_type, stride, matrix, getter, setter, occupy。
    ('GL_BOOL', 1, 'GL_INT', False, G_i, S_1i, 1),
    ('GL_BOOL_VEC2', 2, 'GL_INT', False, G_i, S_2i, 1),
    ('GL_BOOL_VEC3', 3, 'GL_INT', False, G_i, S_3i, 1),
    ('GL_BOOL_VEC4', 4, 'GL_INT', False, G_i, S_4i, 1),
    ('GL_INT', 1, 'GL_INT', False, G_i, S_1i, 1),
    ('GL_INT_VEC2', 2, 'GL_INT', False, G_i, S_2i, 1),
    ('GL_INT_VEC3', 3, 'GL_INT', False, G_i, S_3i, 1),
    ('GL_INT_VEC4', 4, 'GL_INT', False, G_i, S_4i, 1),
    ('GL_UNSIGNED_INT', 1, 'GL_UNSIGNED_INT', False, G_u, S_1u, 1),
    ('GL_UNSIGNED_INT_VEC2', 2, 'GL_UNSIGNED_INT', False, G_u, S_2u, 1),
    ('GL_UNSIGNED_INT_VEC3', 3, 'GL_UNSIGNED_INT', False, G_u, S_3u, 1),
    ('GL_UNSIGNED_INT_VEC4', 4, 'GL_UNSIGNED_INT', False, G_u, S_4u, 1),
    ('GL_FLOAT', 1, 'GL_FLOAT', False, G_f, S_1f, 1),
    ('GL_FLOAT_VEC2', 2, 'GL_FLOAT', False, G_f, S_2f, 1),
    ('GL_FLOAT_VEC3', 3, 'GL_FLOAT', False, G_f, S_3f, 1),
    ('GL_FLOAT_VEC4', 4, 'GL_FLOAT', False, G_f, S_4f, 1),
    ('GL_DOUBLE', 1, 'GL_DOUBLE', False, G_d, S_1d, 1),
    ('GL_DOUBLE_VEC2', 2, 'GL_DOUBLE', False, G_d, S_2d, 1),
    ('GL_DOUBLE_VEC3', 3, 'GL_DOUBLE', False, G_d, S_3d, 1),
    ('GL_DOUBLE_VEC4', 4, 'GL_DOUBLE', False, G_d, S_4d, 1),
    # 这些涉及纹理的都是整数。
    ('GL_SAMPLER_2D', 1, 'GL_INT', False, G_i, S_1i, 1),
    ('GL_SAMPLER_2D_ARRAY', 1, 'GL_INT', False, G_i, S_1i, 1),
    ('GL_SAMPLER_3D', 1, 'GL_INT', False, G_i, S_1i, 1),
    ('GL_SAMPLER_2D_SHADOW', 1, 'GL_INT', False, G_i, S_1i, 1),
    ('GL_SAMPLER_2D_MULTI''SAMPLE', 1, 'GL_INT', False, G_i, S_1i, 1),
    ('GL_SAMPLER_CUBE', 1, 'GL_INT', False, G_i, S_1i, 1),
    ('GL_IMAGE_2D', 1, 'GL_INT', False, G_i, S_1i, 1),  # 330 后封了这个。
    # 接下来是矩阵。
    ('GL_FLOAT_MAT2', 4, 'GL_FLOAT', True, G_f, M_2f, 2),
    ('GL_FLOAT_MAT2x3', 6, 'GL_FLOAT', True, G_f, M_2x3f, 2),
    ('GL_FLOAT_MAT2x4', 8, 'GL_FLOAT', True, G_f, M_2x4f, 2),
    ('GL_FLOAT_MAT3x2', 6, 'GL_FLOAT', True, G_f, M_3x2f, 3),
    ('GL_FLOAT_MAT3', 9, 'GL_FLOAT', True, G_f, M_3f, 3),
    ('GL_FLOAT_MAT3x4', 12, 'GL_FLOAT', True, G_f, M_3x4f, 3),
    ('GL_FLOAT_MAT4x2', 8, 'GL_FLOAT', True, G_f, M_4x2f, 4),
    ('GL_FLOAT_MAT4x3', 12, 'GL_FLOAT', True, G_f, M_4x3f, 4),
    ('GL_FLOAT_MAT4', 16, 'GL_FLOAT', True, G_f, M_4f, 4),
    ('GL_DOUBLE_MAT2', 4, 'GL_DOUBLE', True, G_d, M_2d, 2),
    ('GL_DOUBLE_MAT2x3', 6, 'GL_DOUBLE', True, G_d, M_2x3d, 2),
    ('GL_DOUBLE_MAT2x4', 8, 'GL_DOUBLE', True, G_d, M_2x4d, 2),
    ('GL_DOUBLE_MAT3x2', 6, 'GL_DOUBLE', True, G_d, M_3d, 3),
    ('GL_DOUBLE_MAT3', 9, 'GL_DOUBLE', True, G_d, M_3x2d, 3),
    ('GL_DOUBLE_MAT3x4', 12, 'GL_DOUBLE', True, G_d, M_3x4d, 3),
    ('GL_DOUBLE_MAT4x2', 8, 'GL_DOUBLE', True, G_d, M_4x2d, 4),
    ('GL_DOUBLE_MAT4x3', 12, 'GL_DOUBLE', True, G_d, M_4x3d, 4),
    ('GL_DOUBLE_MAT4', 16, 'GL_DOUBLE', True, G_d, M_4d, 4),
)

UNIFORM_TYPES = dict((gl_getattr(m[0]), m) for m in UNIFORM_TYPES)


class Uniform(object):
    def __init__(self, program_id, location, uniform_number, uniform_type):
        self._uniform_program = program_id
        self._uniform_location = location
        self._uniform_number = uniform_number
        self._uniform_type = uniform_type

        (self._uniform_type_enum, self._uniform_element_nums,
         self._uniform_element_enum, self._uniform_is_matrix,
         self._uniform_getter, self._uniform_setter, self._uniform_occupy
         ) = UNIFORM_TYPES[uniform_type]

        self._uniform_element_type, size = \
            BUFFER_TYPES[self._uniform_element_enum]
        self._uniform_bytes = size * self._uniform_element_nums

    def __repr__(self):
        return '<uniform_{} type:{}>'.format(
            self._uniform_location, self._uniform_type_enum)

    def _uniform_get_value(self, data):
        for i in range(self._uniform_number):
            self._uniform_getter(
                self._uniform_program,
                self._uniform_location + i * self._uniform_occupy, data
            )

            yield data[:]

    @property
    def value(self):
        getter_cache = Array(  # 用于获取自身内容的缓存
            element_nums=self._uniform_element_nums,
            element_type=self._uniform_element_type
        )
        return tuple(self._uniform_get_value(getter_cache))

    def _uniform_set_value(self, i, data):
        if (data.array_data_bytes != self._uniform_bytes or
                data.array_element_type != self._uniform_element_type):
            raise ValueError('长度或元素类型不匹配')

        if self._uniform_is_matrix:
            self._uniform_setter(
                self._uniform_program,
                self._uniform_location + i * self._uniform_occupy,
                self._uniform_number, False, data
            )

        else:
            self._uniform_setter(
                self._uniform_program,
                self._uniform_location + i * self._uniform_occupy,
                self._uniform_number, data
            )

    @value.setter
    def value(self, data_arrays):
        if isinstance(data_arrays, tuple):
            assert len(data_arrays) == self._uniform_number
            for i, data in enumerate(data_arrays):
                self._uniform_set_value(i, data)
        else:
            self._uniform_set_value(0, data_arrays)


class UniformBlock(object):
    _uniform_binding = 1

    def __init__(self, program_id, uniform_id, block_size):
        self._uniform_program = program_id
        self._uniform_id = uniform_id
        self._uniform_size = block_size
        self._uniform_binding = UniformBlock._uniform_binding
        self._uniform_buffer = None

        # 通过这个步骤绑定 UniformBufferObject，然后通过修改 Buffer 的值来改变
        glUniformBlockBinding(
            self._uniform_program, self._uniform_id, self._uniform_binding
        )
        UniformBlock._uniform_binding += 1

    def __repr__(self):
        return '<UniformBlock:{} size:{} bind:{}>'.format(
            self._uniform_id, self._uniform_size, self._uniform_binding
        )

    # def uniform_block_bind(self, buffer):
    #     # 需要设置为 GL_UNSIGNED_BYTE, GL_UNIFORM_BUFFER, GL_DYNAMIC_DRAW
    #     offset = 0
    #     glBindBufferRange(
    #         GL_UNIFORM_BUFFER, self._uniform_binding, buffer, offset,
    #         self._uniform_size
    #     )
    #     # 我觉得用 glBindBufferBase 会更好，虽然 glBindBufferRange 更有适用性
    #     glBindBufferBase(GL_UNIFORM_BUFFER, self._uniform_binding, buffer)
    #     self._uniform_buffer = buffer

    @property
    def value(self):
        if not self._uniform_buffer:
            return None
        return self._uniform_buffer.buffer_read()

    @value.setter
    def value(self, data):
        if self._uniform_buffer:
            self._uniform_buffer.buffer_write(data)
        else:
            self._uniform_buffer = Buffer(
                data, 'GL_UNSIGNED_BYTE',
                'GL_UNIFORM_BUFFER', 'GL_DYNAMIC_DRAW'
            )
            glBindBufferBase(
                GL_UNIFORM_BUFFER, self._uniform_binding, self._uniform_buffer
            )


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

    glGetProgramiv(program_id, GL_TRANSFORM_FEEDBACK_VARYINGS, _number)
    for _i in range(_number.value):
        glGetTransformFeedbackVarying(
            program_id, _i, _NAME_LENGTH, _member_name_size,
            _member_array, _member_type, _member_name
        )

        yield (_member_name[:_member_name_size.value].decode(),
               Varying(_i, _member_array.value))

    glGetProgramiv(program_id, GL_ACTIVE_UNIFORMS, _number)
    for _i in range(_number.value):
        glGetActiveUniform(
            program_id, _i, _NAME_LENGTH, _member_name_size,
            _member_array, _member_type, _member_name
        )
        _location = glGetUniformLocation(program_id, _member_name)

        yield (_member_name[:_member_name_size.value].decode(),
               Uniform(program_id, _location,
                       _member_array.value, _member_type.value))

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
