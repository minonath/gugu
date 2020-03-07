import ctypes
import typing

from gu.geometry import Array
from .buffer import Buffer
from .gl_api import *


_GL_TYPE_INFO = {
    GL_BOOL: ('BOOL', 1, 1, GL_INT, 0),
    GL_BOOL_VEC2: ('BOOL_VEC2', 2, 1, GL_INT, 0),
    GL_BOOL_VEC3: ('BOOL_VEC3', 3, 1, GL_INT, 0),
    GL_BOOL_VEC4: ('BOOL_VEC4', 4, 1, GL_INT, 0),

    GL_INT: ('GL_INT', 1, 1, GL_INT, 0),
    GL_INT_VEC2: ('GL_INT_VEC2', 2, 1, GL_INT, 0),
    GL_INT_VEC3: ('GL_INT_VEC3', 3, 1, GL_INT, 0),
    GL_INT_VEC4: ('GL_INT_VEC4', 4, 1, GL_INT, 0),

    GL_UNSIGNED_INT: ('GL_UNSIGNED', 1, 1, GL_UNSIGNED_INT, 0),
    GL_UNSIGNED_INT_VEC2: ('GL_UNSIGNED_VEC2', 2, 1, GL_UNSIGNED_INT, 0),
    GL_UNSIGNED_INT_VEC3: ('GL_UNSIGNED_VEC3', 3, 1, GL_UNSIGNED_INT, 0),
    GL_UNSIGNED_INT_VEC4: ('GL_UNSIGNED_VEC4', 4, 1, GL_UNSIGNED_INT, 0),

    GL_FLOAT: ('GL_FLOAT', 1, 1, GL_FLOAT, 0),
    GL_FLOAT_VEC2: ('GL_FLOAT_VEC2', 2, 1, GL_FLOAT, 0),
    GL_FLOAT_VEC3: ('GL_FLOAT_VEC3', 3, 1, GL_FLOAT, 0),
    GL_FLOAT_VEC4: ('GL_FLOAT_VEC4', 4, 1, GL_FLOAT, 0),

    GL_DOUBLE: ('GL_DOUBLE', 1, 1, GL_DOUBLE, 0),
    GL_DOUBLE_VEC2: ('GL_DOUBLE_VEC2', 2, 1, GL_DOUBLE, 0),
    GL_DOUBLE_VEC3: ('GL_DOUBLE_VEC3', 3, 1, GL_DOUBLE, 0),
    GL_DOUBLE_VEC4: ('GL_DOUBLE_VEC4', 4, 1, GL_DOUBLE, 0),

    GL_SAMPLER_2D: ('GL_SAMPLER_2D', 1, 1, GL_INT, 0),
    GL_SAMPLER_2D_ARRAY: ('GL_SAMPLER_2D_ARRAY', 1, 1, GL_INT, 0),
    GL_SAMPLER_3D: ('GL_SAMPLER_3D', 1, 1, GL_INT, 0),
    GL_SAMPLER_2D_SHADOW: ('GL_SAMPLER_2D_SHADOW', 1, 1, GL_INT, 0),
    GL_SAMPLER_2D_MULTISAMPLE: ('GL_SAMPLER_2D_MULTI', 1, 1, GL_INT, 0),
    GL_SAMPLER_CUBE: ('GL_SAMPLER_CUBE', 1, 1, GL_INT, 0),
    # GL_IMAGE_2D: ('GL_IMAGE_2D', 1, 1, GL_INT, 0),

    GL_FLOAT_MAT2: ('GL_FLOAT_MAT2', 4, 1, GL_FLOAT, '2'),
    GL_FLOAT_MAT2x3: ('GL_FLOAT_MAT2x3', 6, 2, GL_FLOAT, '2x3'),
    GL_FLOAT_MAT2x4: ('GL_FLOAT_MAT2x4', 8, 2, GL_FLOAT, '2x4'),
    GL_FLOAT_MAT3x2: ('GL_FLOAT_MAT3x2', 6, 2, GL_FLOAT, '3x2'),
    GL_FLOAT_MAT3: ('GL_FLOAT_MAT3', 9, 3, GL_FLOAT, '3'),
    GL_FLOAT_MAT3x4: ('GL_FLOAT_MAT3x4', 12, 3, GL_FLOAT, '3x4'),
    GL_FLOAT_MAT4x2: ('GL_FLOAT_MAT4x2', 8, 2, GL_FLOAT, '4x2'),
    GL_FLOAT_MAT4x3: ('GL_FLOAT_MAT4x3', 12, 2, GL_FLOAT, '4x3'),
    GL_FLOAT_MAT4: ('GL_FLOAT_MAT4', 16, 4, GL_FLOAT, '4'),

    GL_DOUBLE_MAT2: ('GL_DOUBLE_MAT2', 4, 1, GL_DOUBLE, '2'),
    GL_DOUBLE_MAT2x3: ('GL_DOUBLE_MAT2x3', 6, 2, GL_DOUBLE, '2x3'),
    GL_DOUBLE_MAT2x4: ('GL_DOUBLE_MAT2x4', 8, 2, GL_DOUBLE, '2x4'),
    GL_DOUBLE_MAT3x2: ('GL_DOUBLE_MAT3x2', 6, 2, GL_DOUBLE, '3x2'),
    GL_DOUBLE_MAT3: ('GL_DOUBLE_MAT3', 9, 3, GL_DOUBLE, '3'),
    GL_DOUBLE_MAT3x4: ('GL_DOUBLE_MAT3x4', 12, 3, GL_DOUBLE, '3x4'),
    GL_DOUBLE_MAT4x2: ('GL_DOUBLE_MAT4x2', 8, 2, GL_DOUBLE, '4x2'),
    GL_DOUBLE_MAT4x3: ('GL_DOUBLE_MAT4x3', 12, 3, GL_DOUBLE, '4x3'),
    GL_DOUBLE_MAT4: ('GL_DOUBLE_MAT4', 16, 4, GL_DOUBLE, '4'),
}

_GL_TYPE_SIZE = {
    GL_BYTE: 1,
    GL_UNSIGNED_BYTE: 1,
    GL_SHORT: 2,
    GL_UNSIGNED_SHORT: 2,
    GL_INT: 4,
    GL_UNSIGNED_INT: 4,
    GL_FLOAT: 4,
    GL_DOUBLE: 8
}

_GL_ATTRIBUTE_GETTER = {
    GL_INT: (glVertexAttribIPointer, False),
    GL_UNSIGNED_INT: (glVertexAttribIPointer, False),
    GL_DOUBLE: (glVertexAttribLPointer, False),
    GL_FLOAT: (glVertexAttribPointer, True),
}


_GL_TYPE_TO_C_TYPE = {
    GL_BYTE: ctypes.c_byte,
    GL_UNSIGNED_BYTE: ctypes.c_ubyte,
    GL_SHORT: ctypes.c_short,
    GL_UNSIGNED_SHORT: ctypes.c_ushort,
    GL_INT: ctypes.c_int,
    GL_UNSIGNED_INT: ctypes.c_uint,
    GL_FLOAT: ctypes.c_float,
    GL_DOUBLE: ctypes.c_double
}

_GL_UNIFORM_GETTER_SUFFIX = {
    GL_INT: 'iv',
    GL_UNSIGNED_INT: 'uiv',
    GL_FLOAT: 'fv',
    GL_DOUBLE: 'dv'
}

_GL_UNIFORM_FUNC = {
    'glGetUniformiv': glGetUniformiv,
    'glGetUniformuiv': glGetUniformuiv,
    'glGetUniformfv': glGetUniformfv,
    'glGetUniformdv': glGetUniformdv,

    'glProgramUniform1iv': glProgramUniform1iv,
    'glProgramUniform2iv': glProgramUniform2iv,
    'glProgramUniform3iv': glProgramUniform3iv,
    'glProgramUniform4iv': glProgramUniform4iv,
    'glProgramUniform1uiv': glProgramUniform1uiv,
    'glProgramUniform2uiv': glProgramUniform2uiv,
    'glProgramUniform3uiv': glProgramUniform3uiv,
    'glProgramUniform4uiv': glProgramUniform4uiv,
    'glProgramUniform1fv': glProgramUniform1fv,
    'glProgramUniform2fv': glProgramUniform2fv,
    'glProgramUniform3fv': glProgramUniform3fv,
    'glProgramUniform4fv': glProgramUniform4fv,
    'glProgramUniform1dv': glProgramUniform1dv,
    'glProgramUniform2dv': glProgramUniform2dv,
    'glProgramUniform3dv': glProgramUniform3dv,
    'glProgramUniform4dv': glProgramUniform4dv,

    'glProgramUniformMatrix2fv': glProgramUniformMatrix2fv,
    'glProgramUniformMatrix3fv': glProgramUniformMatrix3fv,
    'glProgramUniformMatrix4fv': glProgramUniformMatrix4fv,

    'glProgramUniformMatrix2dv': glProgramUniformMatrix2dv,
    'glProgramUniformMatrix3dv': glProgramUniformMatrix3dv,
    'glProgramUniformMatrix4dv': glProgramUniformMatrix4dv,

    'glProgramUniformMatrix2x3fv': glProgramUniformMatrix2x3fv,
    'glProgramUniformMatrix3x2fv': glProgramUniformMatrix3x2fv,
    'glProgramUniformMatrix2x4fv': glProgramUniformMatrix2x4fv,
    'glProgramUniformMatrix4x2fv': glProgramUniformMatrix4x2fv,
    'glProgramUniformMatrix3x4fv': glProgramUniformMatrix3x4fv,
    'glProgramUniformMatrix4x3fv': glProgramUniformMatrix4x3fv,

    'glProgramUniformMatrix2x3dv': glProgramUniformMatrix2x3dv,
    'glProgramUniformMatrix3x2dv': glProgramUniformMatrix3x2dv,
    'glProgramUniformMatrix2x4dv': glProgramUniformMatrix2x4dv,
    'glProgramUniformMatrix4x2dv': glProgramUniformMatrix4x2dv,
    'glProgramUniformMatrix3x4dv': glProgramUniformMatrix3x4dv,
    'glProgramUniformMatrix4x3dv': glProgramUniformMatrix4x3dv
}


def get_attribute_info_by_type(gl_enum: int) -> tuple:
    """
    获取 Attribute 的一些属性
    """
    (_name, _element_number, _location_occupy, _sign_type, _
     ) = _GL_TYPE_INFO[gl_enum]
    _stride = _GL_TYPE_SIZE[_sign_type] * _element_number
    _set_function, _normalizable = _GL_ATTRIBUTE_GETTER[_sign_type]

    return (_name, _element_number, _sign_type, _stride,
            _normalizable, _set_function, _location_occupy)


def get_uniform_info_by_type(gl_enum: int) -> tuple:
    """
    获取 Uniform 的一些属性
    """
    (_name, _element_number, _location_occupy, _sign_type, _is_matrix
     ) = _GL_TYPE_INFO[gl_enum]
    _element_type = _GL_TYPE_TO_C_TYPE[_sign_type]

    if _is_matrix:
        _suffix = _GL_UNIFORM_GETTER_SUFFIX[_sign_type]
        _get_function = _GL_UNIFORM_FUNC['glGetUniform%s' % _suffix]
        _set_function = _GL_UNIFORM_FUNC[
            'glProgramUniformMatrix%s%s' % (_is_matrix, _suffix)
            ]
        _is_matrix = True
    else:
        _suffix = _GL_UNIFORM_GETTER_SUFFIX[_sign_type]
        _get_function = _GL_UNIFORM_FUNC['glGetUniform%s' % _suffix]
        _set_function = _GL_UNIFORM_FUNC[
            'glProgramUniform%i%s' % (_element_number, _suffix)
            ]
        _is_matrix = False

    return (_name, _element_number, _element_type,  # _element_size,
            _is_matrix, _get_function, _set_function, _location_occupy)


class Attribute(object):
    """
    program 中的输入变量

    attrib_location:        输入变量的位置
    attrib_array_size:      输入变量是否为数组，以及数组的长度
    attrib_element_number:  输入变量含有的元素个数
    attrib_element_type:    输入变量含有的元素类型
    attrib_size:            attrib_element_size ✖ attrib_element_number
    attrib_normalizable:    输入的变量是否进行单位化，作为矩阵输入的四元数需要单位化
    attrib_set_function:    输入函数
    attrib_occupy           占用 location 的数量
                            ceil(self.attrib_element_number // 4)
    """

    def __init__(self, location: int, member_number: int, member_type: int):
        self._attrib_location = location
        self._attrib_number = member_number

        (_type, self._attrib_length, self._attrib_element_type,
         self._attrib_size, self._attrib_normalizable,
         self._attrib_setter, self._attrib_occupy
         ) = get_attribute_info_by_type(member_type)

        self.__string__ = '<Attribute:{} type:{}>'.format(location, _type)

    def __repr__(self):
        return self.__string__

    def attribute_get_info(self) -> typing.Generator:
        if self._attrib_number == 1:
            yield (
                self._attrib_location,
                self._attrib_length,
                self._attrib_element_type,
                self._attrib_size,
                self._attrib_normalizable,
                self._attrib_setter
            )

        else:
            for _i in range(self._attrib_number):
                yield (
                    self._attrib_location + _i * self._attrib_occupy,
                    self._attrib_length,
                    self._attrib_element_type,
                    self._attrib_size,
                    self._attrib_normalizable,
                    self._attrib_setter
                )

        # location, element_number, element_type, size, normalizable, function


class Varying(object):
    """
    仅在显卡内部流转的变量类型

    因为无法读取，所以没什么作用，OpenGL 3.0 后移除了
    """

    def __init__(self, index, size):
        self.__string__ = '<Varying:{} size:{}>'.format(index, size)

    def __repr__(self):
        return self.__string__


class Uniform(object):
    def __init__(self, program_id: int, location: int, uniform_number: int,
                 uniform_type: int):
        self._uniform_program = program_id
        self._uniform_location = location
        self._uniform_number = uniform_number

        (_type_name, self._uniform_length, self._uniform_element_type,
         self._uniform_is_matrix, self._uniform_getter,
         self._uniform_setter, self._uniform_occupy
         ) = get_uniform_info_by_type(uniform_type)

        self._uniform_full_length = uniform_number * self._uniform_length
        self.__string__ = '<Uniform:{} type:{}>'.format(location, _type_name)

    def __repr__(self):
        return self.__string__

    def _uniform_get_value(self, _data_buffer: Array):
        for _i in range(self._uniform_number):
            if self._uniform_is_matrix:
                self._uniform_getter(
                    self._uniform_program,
                    self._uniform_location + _i * self._uniform_occupy,
                    False,
                    _data_buffer
                )

            else:
                self._uniform_getter(
                    self._uniform_program,
                    self._uniform_location + _i * self._uniform_occupy,
                    _data_buffer
                )

            yield _data_buffer[:]

    @property
    def value(self):
        _getter = Array(  # 用于获取自身内容的缓存
            length=self._uniform_length,
            _type=self._uniform_element_type
        )
        return tuple(self._uniform_get_value(_getter))

    @value.setter
    def value(self, data_array: Array):
        if (data_array.array_length != self._uniform_full_length or
                data_array.array_element_type != self._uniform_element_type):
            raise

        if self._uniform_is_matrix:
            self._uniform_setter(
                self._uniform_program,
                self._uniform_location,
                self._uniform_number,
                False,
                data_array
            )

        else:
            self._uniform_setter(
                self._uniform_program,
                self._uniform_location,
                self._uniform_number,
                data_array
            )


class UniformBlock(object):
    _uniform_binding = 1

    def __init__(self, program_id: int, uniform_id: int, block_size: int):
        self._uniform_program = program_id
        self._uniform_id = uniform_id
        # self._uniform_size = block_size

        # 通过这个步骤绑定 UniformBufferObject，然后通过修改 Buffer 的值来改变
        glUniformBlockBinding(
            self._uniform_program, self._uniform_id, self._uniform_binding
        )
        self.__string__ = '<UniformBlock:{} size:{} bind:{}>'.format(
            uniform_id, block_size, self._uniform_binding
        )
        UniformBlock._uniform_binding += 1

    def __repr__(self):
        return self.__string__

    def uniform_block_bind(self, buffer: Buffer):
        # buffer 需要设置为 GL_UNSIGNED_BYTE, GL_UNIFORM_BUFFER, GL_DYNAMIC_DRAW
        # offset = 0
        # glBindBufferRange(
        #     GL_UNIFORM_BUFFER, self._uniform_binding, buffer, offset,
        #     self._uniform_size
        # )
        # 我觉得用 glBindBufferBase 会更好，虽然 glBindBufferRange 更有适用性
        glBindBufferBase(GL_UNIFORM_BUFFER, self._uniform_binding, buffer)
