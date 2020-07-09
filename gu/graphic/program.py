import pathlib
import ctypes


from .object import OpenGLObject
from .member import program_get_member
from ..opengl import *


_shader_directory = pathlib.Path(__file__).parent.joinpath('shader')


def _create_shader(program_id: int, target: int, source: str):
    """ 创建 Shader。 """
    shader_id = glCreateShader(target)

    if not shader_id:
        raise OpenGLError('无法创建(Shader)着色器')

    string = ctypes.create_string_buffer(source.encode())
    char_pp = (ctypes.c_char_p * 1)(ctypes.addressof(string))

    glShaderSource(shader_id, 1, char_pp, None)
    glCompileShader(shader_id)

    compiled = ctypes.c_int()  # GLint()
    glGetShaderiv(shader_id, GL_COMPILE_STATUS, compiled)
    if not compiled:
        log_length = ctypes.c_int()  # GL size i()
        glGetShaderiv(shader_id, GL_INFO_LOG_LENGTH, log_length)
        log = (ctypes.c_char * log_length.value)()
        glGetShaderInfoLog(shader_id, log_length, log_length, log)
        glDeleteShader(shader_id)
        raise OpenGLError(bytes(log).decode())

    glAttachShader(program_id, shader_id)

    return shader_id


def _get_shader(target_file):
    result = dict()

    if target_file.exists():
        with open(target_file, 'r') as f:
            try:
                exec(f.read(), None, result)
            except Exception as e:
                return e

    # 包含有五种 shader 中的几种
    # GL_VERTEX_SHADER
    # GL_FRAGMENT_SHADER
    # GL_GEOMETRY_SHADER
    # GL_TESS_EVALUATION_SHADER
    # GL_TESS_CONTROL_SHADER

    return result


class ProgramManager(object):
    def __repr__(self):
        return self.__class__.__name__

    def __str__(self):
        return str(self.__dict__)


def load_all_program():
    for k in _shader_directory.glob('*'):
        Program(k.stem, k)


program_manager = ProgramManager()


class Program(OpenGLObject):
    def __init__(self, name=None, route=None, **kwargs):
        self._program_name = name
        if kwargs:
            self._program_shader_dict = kwargs
        else:
            if route is None:
                route = _shader_directory.joinpath(name).with_suffix('.py')
            self._program_shader_dict = _get_shader(route)
        if isinstance(self._program_shader_dict, Exception):
            return
        self._program_shader = None
        self._program_id = 0
        self._program_member = None

        OpenGLObject.__init__(self)
        setattr(program_manager, name, self)

    def __call__(self):
        glUseProgram(self._program_id)

    def __repr__(self):
        return self.__string__

    def gl_initialize(self) -> str:
        self._program_id = glCreateProgram()

        if not self._program_id:
            raise OpenGLError('无法创建(Program)渲染程序')

        self._program_shader = tuple(
            _create_shader(self._program_id, gl_getattr(target), source)
            for target, source in self._program_shader_dict.items()
        )

        glLinkProgram(self._program_id)

        linked = ctypes.c_int()  # GLint()
        glGetProgramiv(self._program_id, GL_LINK_STATUS, linked)
        if not linked:
            length = ctypes.c_int()  # GL size i(0)
            glGetProgramiv(self._program_id, GL_INFO_LOG_LENGTH, length)
            log = (ctypes.c_char * length.value)()
            glGetProgramInfoLog(self._program_id, length, length, log)
            glDeleteProgram(self._program_id)
            raise OpenGLError(bytes(log).decode())

        self._program_member = dict(program_get_member(self._program_id))

        return 'program_%d' % self._program_id

    def gl_release(self) -> None:
        for _shader_id in self._program_shader:
            glDetachShader(self._program_id, _shader_id)
            glDeleteShader(_shader_id)

        glDeleteProgram(self._program_id)
        delattr(program_manager, self._program_name)
