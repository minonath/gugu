import ctypes
import typing

import gu.graphic.gl_api
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


class _Attribute(object):
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


class _Varying(object):
    """
    仅在显卡内部流转的变量类型

    因为无法读取，所以没什么作用，OpenGL 3.0 后移除了
    """

    def __init__(self, index, size):
        self.__string__ = '<Varying:{} size:{}>'.format(index, size)

    def __repr__(self):
        return self.__string__


class _Uniform(object):
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


class _UniformBlock(object):
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
        _UniformBlock._uniform_binding += 1

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


class Program(object):
    _SHADER_TARGETS = (
        GL_VERTEX_SHADER,
        GL_FRAGMENT_SHADER,
        GL_GEOMETRY_SHADER,
        GL_TESS_EVALUATION_SHADER,
        GL_TESS_CONTROL_SHADER
    )

    def __init__(self, *shader_list):
        _program_id = glCreateProgram()

        if not _program_id:
            raise OpenGLError('无法创建(Program)渲染程序')

        self._program_shader = tuple(
            self._program_create_shader(_program_id, _target, _source)
            for _source, _target in zip(shader_list, self._SHADER_TARGETS)
            if _source
        )

        glLinkProgram(_program_id)

        _linked = ctypes.c_int()  # GLint()
        glGetProgramiv(_program_id, GL_LINK_STATUS, _linked)
        if not _linked:
            _length = ctypes.c_int()  # GL size i(0)
            glGetProgramiv(_program_id, GL_INFO_LOG_LENGTH, _length)
            _log = (ctypes.c_char * _length.value)()
            glGetProgramInfoLog(_program_id, _length, _length, _log)
            glDeleteProgram(_program_id)
            raise OpenGLError(bytes(_log).decode())

        self._program_id = _program_id

        self._program_member = dict(self._program_get_member(_program_id))

    def __del__(self):
        for _shader_id in self._program_shader:
            glDetachShader(self._program_id, _shader_id)
            glDeleteShader(_shader_id)

        glDeleteProgram(self._program_id)

    def __str__(self):
        return '<Program:{} {}>'.format(
            self._program_id, self._program_member)

    def __call__(self, **kwargs):
        glUseProgram(self._program_id)

        for _name, _value in kwargs.items():
            self._program_member[_name].value = _value

    @staticmethod
    def _program_create_shader(program_id: int, target: int, source: str):
        """ 创建 Shader。 """
        _shader_id = glCreateShader(target)

        if not _shader_id:
            raise OpenGLError('无法创建(Shader)着色器')

        _string = ctypes.create_string_buffer(source.encode())
        _char_pp = (ctypes.c_char_p * 1)(ctypes.addressof(_string))

        glShaderSource(_shader_id, 1, _char_pp, None)
        glCompileShader(_shader_id)

        _compiled = ctypes.c_int()  # GLint()
        glGetShaderiv(_shader_id, GL_COMPILE_STATUS, _compiled)
        if not _compiled:
            _log_length = ctypes.c_int()  # GL size i()
            glGetShaderiv(_shader_id, GL_INFO_LOG_LENGTH, _log_length)
            _log = (ctypes.c_char * _log_length.value)()
            glGetShaderInfoLog(_shader_id, _log_length, _log_length, _log)
            glDeleteShader(_shader_id)
            raise OpenGLError(bytes(_log).decode())

        glAttachShader(program_id, _shader_id)

        return _shader_id

    @staticmethod
    def _program_get_member(program_id: int) -> typing.Generator:
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
                _Attribute(_location, _member_array.value, _member_type.value)
            )

        glGetProgramiv(program_id, GL_TRANSFORM_FEEDBACK_VARYINGS, _number)
        for _i in range(_number.value):
            glGetTransformFeedbackVarying(
                program_id, _i, _NAME_LENGTH, _member_name_size,
                _member_array, _member_type, _member_name
            )

            yield (_member_name[:_member_name_size.value].decode(),
                   _Varying(_i, _member_array.value))

        glGetProgramiv(program_id, GL_ACTIVE_UNIFORMS, _number)
        for _i in range(_number.value):
            glGetActiveUniform(
                program_id, _i, _NAME_LENGTH, _member_name_size,
                _member_array, _member_type, _member_name
            )
            _location = glGetUniformLocation(program_id, _member_name)

            yield (_member_name[:_member_name_size.value].decode(),
                   _Uniform(program_id, _location,
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

            return (_member_name[:_member_name_size.value].decode(),
                    _UniformBlock(program_id, _index, _member_array.value))

    def program_get_location(self, *attribute_name: str) -> typing.Generator:
        """
        通过指定 attribute 名称获取相应 location 序列的迭代
        """
        for _name in attribute_name:
            for _info in self._program_member[_name].attribute_get_info():
                yield _info


class VertexArray(object):
    def __init__(self, program: Program, mode: str, *content_data: tuple,
                 index: typing.Optional[Buffer] = None):
        """
        创建一个 VAO 并且绑定 IndexBuffer VertexBuffer InstanceBuffer

        无论是将多个 buffer 绑定到一个 attribute 上，还是将一个 buffer 绑定到多个
        attribute，都是通过 location 来进行的。因此将 attribute 转化为 location
        然后再由 buffer 绑定，就不会出现混乱的情况了。

        从内存角度上这样解释：
        |------------|------------|---------------------------|
        |  buffer 0  |  buffer 1  |         buffer  2         |
        |------------|------------|-------------|-------------|
        | location 0 | location 1 | location 2  | location 3  |
        |------------|------------|-------------|-------------|
        |               attribute 0             | attribute 1 |
        |-------------------------|-------------|-------------|

        因此，这里需要一个将 attribute 转化为 location 的函数
        """
        _vertex_array_id = ctypes.c_uint()  # GL u int
        glGenVertexArrays(1, _vertex_array_id)

        if not _vertex_array_id:
            raise OpenGLError('无法创建(VertexArray)顶点数组')

        glBindVertexArray(_vertex_array_id)

        _vertices = 0  # 作为 VAO 的顶点数
        _instances = 1  # 作为 VAO 的实例数

        for _buffers, _attributes, _divisor in content_data:
            if isinstance(_buffers, Buffer):
                _buffers = (_buffers,)

            if _divisor == 0:
                _t = min(_b.buffer_group_number for _b in _buffers)
                _vertices = min(_t, _vertices) if _vertices else _t
            else:
                _t = min(_b.buffer_group_number for _b in _buffers) * _divisor
                _instances = min(_t, _instances) if _instances != 1 else _t

            if isinstance(_attributes, str):
                _location = program.program_get_location(_attributes)
            else:
                _location = program.program_get_location(*_attributes)

            for _b in _buffers:
                # 绑定前需要指定当前 buffer
                _b.buffer_bind()
                _b.buffer_bind_location(_location, _divisor)

        if index:
            index.buffer_bind()
            self._vertex_array_ebo_type = index.buffer_type
            self._vertex_array_ebo_number = index.buffer_group_number

        self._vertex_array_id = _vertex_array_id
        self._vertex_array_index = index
        self._vertex_array_mode = getattr(gu.graphic.gl_api, mode)
        self._vertex_array_vertices = _vertices
        self._vertex_array_instances = _instances

        glBindVertexArray(0)

        self.__string__ = \
            '<VertexArray:{} {} vertices:{} instances:{} index:{}>'.format(
                _vertex_array_id.value, mode, _vertices, _instances, index
            )

    def __del__(self):
        glDeleteVertexArrays(1, self._vertex_array_id)

    def __repr__(self):
        return self.__string__

    def __call__(self):  # 调用绘制 VAO
        glBindVertexArray(self._vertex_array_id)

        if self._vertex_array_index:
            # 绘制标记，绘制的索引数量，索引的类型，起始位置，绘制的实例数量
            glDrawElementsInstanced(
                self._vertex_array_mode,
                self._vertex_array_ebo_number,
                self._vertex_array_ebo_type,
                0,
                self._vertex_array_instances
            )

        else:
            # 绘制标记，缓存的起始位置，缓存中顶点的数量，绘制的实例数量
            glDrawArraysInstanced(
                self._vertex_array_mode,
                0,
                self._vertex_array_vertices,
                self._vertex_array_instances
            )
