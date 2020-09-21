import pathlib
import ctypes

from ._member import program_get_member

from ..system import OpenGLObject
from ..opengl import *


_shader_directory = pathlib.Path(__file__).parent.joinpath('shader')


def _create_shader(program_id, target, source):
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


def _get_shader(target_file):
    _result = dict()

    if target_file.exists():
        with open(target_file, 'r') as f:
            try:
                exec(f.read(), None, _result)
            except Exception as _e:
                return _e

    # 包含有五种 shader 中的几种
    # GL_VERTEX_SHADER
    # GL_FRAGMENT_SHADER
    # GL_GEOMETRY_SHADER
    # GL_TESS_EVALUATION_SHADER
    # GL_TESS_CONTROL_SHADER

    return _result


class _ProgramManager(object):
    def __repr__(self):
        return 'programs'

    def __str__(self):
        return str(self.__dict__)


def load_all_program():
    for k in _shader_directory.glob('*'):
        Program(k.stem, k)


programs = _ProgramManager()


class Program(OpenGLObject):
    def __init__(self, name=None, route=None, **kwargs):
        self._program_name = name
        if not kwargs:
            if route is None:
                route = _shader_directory.joinpath(name).with_suffix('.py')
            kwargs = _get_shader(route)

        if isinstance(kwargs, Exception):
            return

        OpenGLObject.__init__(self, kwargs)
        setattr(programs, name, self)

    def _initial(self, shader_dict):
        self._program_id = glCreateProgram()

        if not self._program_id:
            raise OpenGLError('无法创建(Program)渲染程序')

        self._program_shader = tuple(
            _create_shader(self._program_id, gl_getattr(target), source)
            for target, source in shader_dict.items()
        )

        glLinkProgram(self._program_id)

        _linked = ctypes.c_int()  # GLint()
        glGetProgramiv(self._program_id, GL_LINK_STATUS, _linked)
        if not _linked:
            _length = ctypes.c_int()  # GL size i(0)
            glGetProgramiv(self._program_id, GL_INFO_LOG_LENGTH, _length)
            _log = (ctypes.c_char * _length.value)()
            glGetProgramInfoLog(self._program_id, _length, _length, _log)
            glDeleteProgram(self._program_id)
            raise OpenGLError(bytes(_log).decode())

        self._program_member = dict(program_get_member(self._program_id))
        self._string = '<program_{} {}>'.format(
            self._program_id, self._program_name
        )

    def _release(self):
        for _shader_id in self._program_shader:
            glDetachShader(self._program_id, _shader_id)
            glDeleteShader(_shader_id)

        glDeleteProgram(self._program_id)
        delattr(programs, self._program_name)

    def program_use(self):
        glUseProgram(self._program_id)

    def __getattr__(self, item):
        return self._program_member.get(item, None)

    @property
    def program_member(self):
        return self._program_member

__all__ = ['load_all_program', 'programs', 'Program']
