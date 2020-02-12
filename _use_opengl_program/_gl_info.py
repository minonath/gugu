import typing

from _use_opengl_program._gl_wrap import *


class SomeInfo(object):
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

    _GL_ATTRIBUTE_GETTER = {
        GL_INT: (glVertexAttribIPointer, False),
        GL_UNSIGNED_INT: (glVertexAttribIPointer, False),
        GL_DOUBLE: (glVertexAttribLPointer, False),
        GL_FLOAT: (glVertexAttribPointer, True),
    }

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

    _GL_TYPE_TO_NAME = {
        GL_BYTE: 'GL_BYTE',
        GL_UNSIGNED_BYTE: 'GL_UNSIGNED_BYTE',
        GL_SHORT: 'GL_SHORT',
        GL_UNSIGNED_SHORT: 'GL_UNSIGNED_SHORT',
        GL_INT: 'GL_INT',
        GL_UNSIGNED_INT: 'GL_UNSIGNED_INT',
        GL_FLOAT: 'GL_FLOAT',
        GL_DOUBLE: 'GL_DOUBLE',

        GL_ARRAY_BUFFER: 'GL_ARRAY_BUFFER',
        GL_ELEMENT_ARRAY_BUFFER: 'GL_ELEMENT_ARRAY_BUFFER',
        GL_UNIFORM_BUFFER: 'GL_UNIFORM_BUFFER',

        GL_STATIC_DRAW: 'GL_STATIC_DRAW',
        GL_DYNAMIC_DRAW: 'GL_DYNAMIC_DRAW',
        GL_STREAM_DRAW: 'GL_STREAM_DRAW',

        GL_POINTS: 'GL_POINTS',
        GL_LINES: 'GL_LINES',
        GL_LINE_LOOP: 'GL_LINE_LOOP',
        GL_LINE_STRIP: 'GL_LINE_STRIP',
        GL_TRIANGLES: 'GL_TRIANGLES',
        GL_TRIANGLE_STRIP: 'GL_TRIANGLE_STRIP',
        GL_TRIANGLE_FAN: 'GL_TRIANGLE_FAN',

        # 在 OpenGL 3.2 之后，封掉了这几个
        # GL_QUADS: 'GL_QUADS',
        # GL_QUAD_STRIP: 'GL_QUAD_STRIP',
        # GL_POLYGON: 'GL_POLYGON',
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

    @classmethod
    def get_uniform_info_by_type(cls, gl_enum: int) -> tuple:
        """
        获取 Uniform 的一些属性
        """
        (_name, _element_number, _location_occupy, _sign_type, _is_matrix
         ) = cls._GL_TYPE_INFO[gl_enum]
        _element_type = cls._GL_TYPE_TO_C_TYPE[_sign_type]
        # _element_size = cls._GL_TYPE_SIZE[gl_enum]

        if _is_matrix:
            _suffix = cls._GL_UNIFORM_GETTER_SUFFIX[_sign_type]
            _get_function = cls._GL_UNIFORM_FUNC['glGetUniform%s' % _suffix]
            _set_function = cls._GL_UNIFORM_FUNC[
                'glProgramUniformMatrix%s%s' % (_is_matrix, _suffix)
                ]
            _is_matrix = True
        else:
            _suffix = cls._GL_UNIFORM_GETTER_SUFFIX[_sign_type]
            _get_function = cls._GL_UNIFORM_FUNC['glGetUniform%s' % _suffix]
            _set_function = cls._GL_UNIFORM_FUNC[
                'glProgramUniform%i%s' % (_element_number, _suffix)
                ]
            _is_matrix = False

        return (_name, _element_number, _element_type,  # _element_size,
                _is_matrix, _get_function, _set_function, _location_occupy)

    @classmethod
    def get_attribute_info_by_type(cls, gl_enum: int) -> tuple:
        """
        获取 Attribute 的一些属性
        """
        (_name, _element_number, _location_occupy, _sign_type, _
         ) = cls._GL_TYPE_INFO[gl_enum]
        _stride = cls._GL_TYPE_SIZE[_sign_type] * _element_number
        _set_function, _normalizable = cls._GL_ATTRIBUTE_GETTER[_sign_type]

        return (_name, _element_number, _sign_type, _stride,
                _normalizable, _set_function, _location_occupy)

    @classmethod
    def get_c_type_by_type(cls, gl_enum: int) -> typing.Union:
        """
        返回一个 ctypes._SimpleData
        """
        return cls._GL_TYPE_TO_C_TYPE[gl_enum]

    @classmethod
    def get_size_by_type(cls, gl_enum: int) -> int:
        """
        返回类型的字节长度
        """
        return cls._GL_TYPE_SIZE[gl_enum]

    @classmethod
    def get_name_by_type(cls, gl_enum: int) -> str:
        """
        返回标记名称
        """
        return cls._GL_TYPE_TO_NAME[gl_enum]
