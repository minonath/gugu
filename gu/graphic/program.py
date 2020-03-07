import ctypes
import typing

import gu.graphic.gl_api
from .buffer import Buffer
from .gl_api import *
from .member import Attribute, Varying, Uniform, UniformBlock


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

            return (_member_name[:_member_name_size.value].decode(),
                    UniformBlock(program_id, _index, _member_array.value))

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
