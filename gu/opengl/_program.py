import ctypes
from .library import *


def _shader(program_id, target, source):
    """ 创建 Shader """

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
        _length = ctypes.c_int()  # GL size i()
        glGetShaderiv(_shader_id, GL_INFO_LOG_LENGTH, _length)
        _log = (ctypes.c_char * _length.value)()
        glGetShaderInfoLog(_shader_id, _length, _length, _log)
        glDeleteShader(_shader_id)
        raise OpenGLError(bytes(_log).decode())

    glAttachShader(program_id, _shader_id)

    return _shader_id


class Program:
    def __init__(self, **shader_dict):
        _program_id = glCreateProgram()

        if not _program_id:
            raise OpenGLError('无法创建(Program)渲染程序')

        self._program_shader = tuple(
            _shader(_program_id, gl_getattr(target), source)
            for target, source in shader_dict.items()
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

        self._as_parameter_ = _program_id

    def __del__(self):
        for _shader_id in self._program_shader:
            glDetachShader(self, _shader_id)
            glDeleteShader(_shader_id)

        glDeleteProgram(self)


__all__ = ['Program']
