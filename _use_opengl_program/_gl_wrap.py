import ctypes
import ctypes.util
import sys


def bind_dynamic_library(lib, fallback=None):  # ver 0.2
    """
    绑定函数

    输入已加载的动态库，返回绑定用函数
    """

    def _bind(name, restype, *arg_types):
        """
        从动态库里绑定函数的函数
        """
        try:
            _func = getattr(lib, name)
            _func.restype = restype
            setattr(_func, 'arg''types', arg_types)

        except AttributeError:  # 绑定失败，返回无效函数
            if fallback:
                _func = fallback(name, restype, *arg_types)  # 这里写参错数数量
            else:
                def _func(*args):  # 无法加载的函数，默认使用这个
                    print('<Error Func>', lib, name, args)

        return _func

    return _bind


if sys.platform in ('win32', 'cygwin'):
    class Ext(object):
        def __init__(self, name, restype, *arg_types):
            self._func = None
            self._name = bytes(ord(c) for c in name)
            self._type = ctypes.WINFUNCTYPE(restype, *arg_types)

        def __call__(self, *args):
            if self._func is None:
                address = _wglGetFunction(self._name)
                if not ctypes.cast(address, ctypes.POINTER(ctypes.c_int)):
                    return None
                self._func = ctypes.cast(address, self._type)
            return self._func(*args)


    gl = bind_dynamic_library(ctypes.windll.opengl32, Ext)
    _wglGetFunction = gl('wglGetP''rocAddress',
                         ctypes.CFUNCTYPE(ctypes.POINTER(ctypes.c_int)),
                         ctypes.c_char_p)
    glu = bind_dynamic_library(ctypes.windll.glu32)


elif sys.platform == 'darwin':
    glu = Ext = gl = bind_dynamic_library(ctypes.cdll.LoadLibrary(
        '/System/Library/Framework/OpenGL.framework/OpenGL'
    ))

else:
    glu = Ext = gl = bind_dynamic_library(ctypes.cdll.LoadLibrary(
        ctypes.util.find_library('OpenGL')
    ))


class OpenGLError(Exception):
    pass

# 这里拿了一些使用到的绑定函数


# gl 11
GL_BYTE = 0x1400
GL_UNSIGNED_BYTE = 0x1401
GL_SHORT = 0x1402
GL_UNSIGNED_SHORT = 0x1403
GL_INT = 0x1404
GL_UNSIGNED_INT = 0x1405
GL_FLOAT = 0x1406
GL_DOUBLE = 0x140a

GL_POINTS = 0x0000
GL_LINES = 0x0001
GL_LINE_LOOP = 0x0002
GL_LINE_STRIP = 0x0003
GL_TRIANGLES = 0x0004
GL_TRIANGLE_STRIP = 0x0005
GL_TRIANGLE_FAN = 0x0006
GL_QUADS = 0x0007
GL_QUAD_STRIP = 0x0008
GL_POLYGON = 0x0009
GL_DEPTH_TEST = 0x0b71
GL_DEPTH_BUFFER_BIT = 0x00000100
GL_COLOR_BUFFER_BIT = 0x00004000
GL_LESS = 0x0201

glClear = gl('glClear', None, ctypes.c_uint)

glEnable = gl('glEnable', None, ctypes.c_uint)

glDepthFunc = gl('glDepthFunc', None, ctypes.c_uint)

# gl 15
GL_ARRAY_BUFFER = 0x8892
GL_ELEMENT_ARRAY_BUFFER = 0x8893

GL_STREAM_DRAW = 0x88e0
GL_STATIC_DRAW = 0x88e4
GL_DYNAMIC_DRAW = 0x88e8

glGenBuffers = gl(
    'glGenBuffers', None,
    ctypes.c_int, ctypes.POINTER(ctypes.c_uint)
)

glBindBuffer = gl('glBindBuffer', None, ctypes.c_uint, ctypes.c_uint)

glBufferData = gl(
    'glBufferData', None,
    ctypes.c_uint, ctypes.c_size_t, ctypes.c_void_p, ctypes.c_uint)

glBufferSubData = gl(
    'glBufferSubData', None,
    ctypes.c_uint, ctypes.c_size_t, ctypes.c_size_t, ctypes.c_void_p
)

glUnmapBuffer = gl('glUnmapBuffer', ctypes.c_ubyte, ctypes.c_uint)

# gl 20
GL_FRAGMENT_SHADER = 0x8b30
GL_VERTEX_SHADER = 0x8b31
GL_FLOAT_VEC2 = 0x8b50
GL_FLOAT_VEC3 = 0x8b51
GL_FLOAT_VEC4 = 0x8b52
GL_INT_VEC2 = 0x8b53
GL_INT_VEC3 = 0x8b54
GL_INT_VEC4 = 0x8b55
GL_BOOL = 0x8b56
GL_BOOL_VEC2 = 0x8b57
GL_BOOL_VEC3 = 0x8b58
GL_BOOL_VEC4 = 0x8b59
GL_FLOAT_MAT2 = 0x8b5a
GL_FLOAT_MAT3 = 0x8b5b
GL_FLOAT_MAT4 = 0x8b5c
GL_SAMPLER_2D = 0x8b5e
GL_SAMPLER_3D = 0x8b5f
GL_SAMPLER_CUBE = 0x8b60
GL_SAMPLER_2D_SHADOW = 0x8b62

GL_COMPILE_STATUS = 0x8b81
GL_LINK_STATUS = 0x8b82
GL_INFO_LOG_LENGTH = 0x8B84

GL_ACTIVE_UNIFORMS = 0x8B86
GL_ACTIVE_ATTRIBUTES = 0x8B89

glAttachShader = Ext('glAttachShader', None, ctypes.c_uint, ctypes.c_uint)

glCompileShader = Ext('glCompileShader', None, ctypes.c_uint)

glCreateProgram = Ext('glCreateProgram', ctypes.c_uint)

glCreateShader = Ext('glCreateShader', ctypes.c_uint, ctypes.c_uint)

glDeleteProgram = Ext('glDeleteProgram', None, ctypes.c_uint)

glDeleteShader = Ext('glDeleteShader', None, ctypes.c_uint)

glDetachShader = Ext('glDetachShader', None, ctypes.c_uint, ctypes.c_uint)

glGetActiveAttrib = Ext(
    'glGetActiveAttrib', None,
    ctypes.c_uint, ctypes.c_uint, ctypes.c_int,
    ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int),
    ctypes.POINTER(ctypes.c_uint), ctypes.c_char_p
)

glGetActiveUniform = Ext(
    'glGetActiveUniform', None,
    ctypes.c_uint, ctypes.c_uint, ctypes.c_size_t,
    ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int),
    ctypes.POINTER(ctypes.c_uint), ctypes.c_char_p
)

glGetAttribLocation = Ext(
    'glGetAttribLocation', ctypes.c_int,
    ctypes.c_uint, ctypes.c_char_p
)

glGetUniformLocation = Ext(
    'glGetUniformLocation', ctypes.c_int,
    ctypes.c_uint, ctypes.c_char_p
)

glGetProgramiv = Ext(
    'glGetProgramiv', None,
    ctypes.c_uint, ctypes.c_uint, ctypes.POINTER(ctypes.c_int)
)

glLinkProgram = Ext('glLinkProgram', None, ctypes.c_uint)

glGetProgramInfoLog = Ext(
    'glGetProgramInfoLog', None,
    ctypes.c_uint, ctypes.c_int, ctypes.POINTER(ctypes.c_int),
    ctypes.c_char_p
)

glGetShaderiv = Ext(
    'glGetShaderiv', None,
    ctypes.c_uint, ctypes.c_uint, ctypes.POINTER(ctypes.c_int)
)

glGetShaderInfoLog = Ext(
    'glGetShaderInfoLog', None,
    ctypes.c_uint, ctypes.c_int, ctypes.POINTER(ctypes.c_int),
    ctypes.c_char_p
)

glShaderSource = Ext(
    'glShaderSource', None,
    ctypes.c_uint, ctypes.c_size_t, ctypes.POINTER(ctypes.c_char_p),
    ctypes.POINTER(ctypes.c_int)
)

glUseProgram = Ext('glUseProgram', None, ctypes.c_uint)

glVertexAttribPointer = Ext(
    'glVertexAttribPointer', None,
    ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_ubyte, ctypes.c_int,
    ctypes.c_void_p
)

glEnableVertexAttribArray = Ext(
    'glEnableVertexAttribArray', None,
    ctypes.c_uint
)

glGetUniformiv = Ext(
    'glGetUniformiv', None,
    ctypes.c_uint, ctypes.c_int, ctypes.c_void_p
)

glGetUniformfv = Ext(
    'glGetUniformfv', None,
    ctypes.c_uint, ctypes.c_int, ctypes.c_void_p
)

# gl 21
GL_FLOAT_MAT2x3 = 0x8b65
GL_FLOAT_MAT2x4 = 0x8b66
GL_FLOAT_MAT3x2 = 0x8b67
GL_FLOAT_MAT3x4 = 0x8b68
GL_FLOAT_MAT4x2 = 0x8b69
GL_FLOAT_MAT4x3 = 0x8b6a

# gl 30
GL_SAMPLER_2D_ARRAY = 0x8dc1
GL_UNSIGNED_INT_VEC2 = 0x8dc6
GL_UNSIGNED_INT_VEC3 = 0x8dc7
GL_UNSIGNED_INT_VEC4 = 0x8dc8

GL_MAP_READ_BIT = 0x0001
GL_MAP_WRITE_BIT = 0x0002

GL_TRANSFORM_FEEDBACK_VARYINGS = 0x8C83

glGetUniformuiv = Ext(
    'glGetUniformuiv', None,
    ctypes.c_uint, ctypes.c_int, ctypes.c_void_p
)

glGetTransformFeedbackVarying = Ext(
    'glGetTransformFeedbackVarying', None,
    ctypes.c_uint, ctypes.c_uint, ctypes.c_int, ctypes.POINTER(ctypes.c_int),
    ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_uint),
    ctypes.c_char_p
)

glVertexAttribIPointer = Ext(
    'glVertexAttribIPointer', None,
    ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_int, ctypes.c_void_p
)

glBindBufferRange = Ext(
    'glBindBufferRange', None,
    ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_size_t,
    ctypes.c_size_t
)

glMapBufferRange = Ext(
    'glMapBufferRange', ctypes.POINTER(ctypes.c_ubyte),
    ctypes.c_uint, ctypes.c_size_t, ctypes.c_size_t, ctypes.c_uint
)

glBindBufferBase = Ext(
    'glBindBufferBase', None,
    ctypes.c_uint, ctypes.c_uint, ctypes.c_uint
)

glBindVertexArray = Ext('glBindVertexArray', None, ctypes.c_uint)

glDeleteVertexArrays = Ext(
    'glDeleteVertexArrays', None,
    ctypes.c_int, ctypes.POINTER(ctypes.c_uint)
)

glGenVertexArrays = Ext(
    'glGenVertexArrays', None,
    ctypes.c_int, ctypes.POINTER(ctypes.c_uint)
)

# gl 31
GL_UNIFORM_BUFFER = 0x8a11
GL_ACTIVE_UNIFORM_BLOCKS = 0x8a36
GL_UNIFORM_BLOCK_DATA_SIZE = 0x8a40

glDrawArraysInstanced = Ext(
    'glDrawArraysInstanced', None,
    ctypes.c_uint, ctypes.c_int, ctypes.c_int, ctypes.c_int
)

glDrawElementsInstanced = Ext(
    'glDrawElementsInstanced', None,
    ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_void_p, ctypes.c_int
)

glUniformBlockBinding = Ext(
    'glUniformBlockBinding', None,
    ctypes.c_uint, ctypes.c_uint, ctypes.c_uint
)
glGetUniformBlockIndex = Ext(
    'glGetUniformBlockIndex', ctypes.c_uint,
    ctypes.c_uint, ctypes.c_char_p
)

glGetActiveUniformBlockiv = Ext(
    'glGetActiveUniformBlockiv', None,
    ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.POINTER(ctypes.c_int)
)

glGetActiveUniformBlockName = Ext(
    'glGetActiveUniformBlockName', None,
    ctypes.c_uint, ctypes.c_uint, ctypes.c_int, ctypes.POINTER(ctypes.c_int),
    ctypes.c_char_p
)

# gl 32
GL_SAMPLER_2D_MULTISAMPLE = 0x9108
GL_GEOMETRY_SHADER = 0x8dd9

# gl 33
glVertexAttribDivisor = Ext(
    'glVertexAttribDivisor', None,
    ctypes.c_uint, ctypes.c_uint
)

# gl 40
GL_DOUBLE_VEC2 = 0x8ffc
GL_DOUBLE_VEC3 = 0x8ffd
GL_DOUBLE_VEC4 = 0x8ffe
GL_DOUBLE_MAT2 = 0x8f46
GL_DOUBLE_MAT3 = 0x8f47
GL_DOUBLE_MAT4 = 0x8f48
GL_DOUBLE_MAT2x3 = 0x8f49
GL_DOUBLE_MAT2x4 = 0x8f4a
GL_DOUBLE_MAT3x2 = 0x8f4b
GL_DOUBLE_MAT3x4 = 0x8f4c
GL_DOUBLE_MAT4x2 = 0x8f4d
GL_DOUBLE_MAT4x3 = 0x8f4e

GL_TESS_EVALUATION_SHADER = 0x8e87
GL_TESS_CONTROL_SHADER = 0x8e88

glGetUniformdv = Ext(
    'glGetUniformdv', None,
    ctypes.c_uint, ctypes.c_int, ctypes.c_void_p
)

# gl 41
glVertexAttribLPointer = Ext(
    'glVertexAttribLPointer', None,
    ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_int, ctypes.c_void_p
)

glProgramUniform1iv = Ext(
    'glProgramUniform1iv', None,
    ctypes.c_uint, ctypes.c_int, ctypes.c_int, ctypes.c_void_p
)

glProgramUniform1fv = Ext(
    'glProgramUniform1fv', None,
    ctypes.c_uint, ctypes.c_int, ctypes.c_int, ctypes.c_void_p
)

glProgramUniform1dv = Ext(
    'glProgramUniform1dv', None,
    ctypes.c_uint, ctypes.c_int, ctypes.c_int, ctypes.c_void_p
)

glProgramUniform1uiv = Ext(
    'glProgramUniform1uiv', None,
    ctypes.c_uint, ctypes.c_int, ctypes.c_int, ctypes.c_void_p
)

glProgramUniform2iv = Ext(
    'glProgramUniform2iv', None,
    ctypes.c_uint, ctypes.c_int, ctypes.c_int, ctypes.c_void_p
)

glProgramUniform2fv = Ext(
    'glProgramUniform2fv', None,
    ctypes.c_uint, ctypes.c_int, ctypes.c_int, ctypes.c_void_p
)

glProgramUniform2dv = Ext(
    'glProgramUniform2dv', None,
    ctypes.c_uint, ctypes.c_int, ctypes.c_int, ctypes.c_void_p
)

glProgramUniform2uiv = Ext(
    'glProgramUniform2uiv', None,
    ctypes.c_uint, ctypes.c_int, ctypes.c_int, ctypes.c_void_p
)

glProgramUniform3iv = Ext(
    'glProgramUniform3iv', None,
    ctypes.c_uint, ctypes.c_int, ctypes.c_int, ctypes.c_void_p
)

glProgramUniform3fv = Ext(
    'glProgramUniform3fv', None,
    ctypes.c_uint, ctypes.c_int, ctypes.c_int, ctypes.c_void_p
)

glProgramUniform3dv = Ext(
    'glProgramUniform3dv', None,
    ctypes.c_uint, ctypes.c_int, ctypes.c_int, ctypes.c_void_p
)

glProgramUniform3uiv = Ext(
    'glProgramUniform3uiv', None,
    ctypes.c_uint, ctypes.c_int, ctypes.c_int, ctypes.c_void_p
)

glProgramUniform4iv = Ext(
    'glProgramUniform4iv', None,
    ctypes.c_uint, ctypes.c_int, ctypes.c_int, ctypes.c_void_p
)

glProgramUniform4fv = Ext(
    'glProgramUniform4fv', None,
    ctypes.c_uint, ctypes.c_int, ctypes.c_int, ctypes.c_void_p
)

glProgramUniform4dv = Ext(
    'glProgramUniform4dv', None,
    ctypes.c_uint, ctypes.c_int, ctypes.c_int, ctypes.c_void_p
)

glProgramUniform4uiv = Ext(
    'glProgramUniform4uiv', None,
    ctypes.c_uint, ctypes.c_int, ctypes.c_int, ctypes.c_void_p
)

glProgramUniformMatrix2fv = Ext(
    'glProgramUniformMatrix2fv', None,
    ctypes.c_uint, ctypes.c_int, ctypes.c_int, ctypes.c_ubyte, ctypes.c_void_p
)

glProgramUniformMatrix3fv = Ext(
    'glProgramUniformMatrix3fv', None,
    ctypes.c_uint, ctypes.c_int, ctypes.c_int, ctypes.c_ubyte, ctypes.c_void_p
)

glProgramUniformMatrix4fv = Ext(
    'glProgramUniformMatrix4fv', None,
    ctypes.c_uint, ctypes.c_int, ctypes.c_int, ctypes.c_ubyte, ctypes.c_void_p
)

glProgramUniformMatrix2dv = Ext(
    'glProgramUniformMatrix2dv', None,
    ctypes.c_uint, ctypes.c_int, ctypes.c_int, ctypes.c_ubyte, ctypes.c_void_p
)

glProgramUniformMatrix3dv = Ext(
    'glProgramUniformMatrix3dv', None,
    ctypes.c_uint, ctypes.c_int, ctypes.c_int, ctypes.c_ubyte, ctypes.c_void_p
)

glProgramUniformMatrix4dv = Ext(
    'glProgramUniformMatrix4dv', None,
    ctypes.c_uint, ctypes.c_int, ctypes.c_int, ctypes.c_ubyte, ctypes.c_void_p
)

glProgramUniformMatrix2x3fv = Ext(
    'glProgramUniformMatrix2x3fv', None,
    ctypes.c_uint, ctypes.c_int, ctypes.c_int, ctypes.c_ubyte, ctypes.c_void_p
)

glProgramUniformMatrix3x2fv = Ext(
    'glProgramUniformMatrix3x2fv', None,
    ctypes.c_uint, ctypes.c_int, ctypes.c_int, ctypes.c_ubyte, ctypes.c_void_p
)

glProgramUniformMatrix2x4fv = Ext(
    'glProgramUniformMatrix2x4fv', None,
    ctypes.c_uint, ctypes.c_int, ctypes.c_int, ctypes.c_ubyte, ctypes.c_void_p
)

glProgramUniformMatrix4x2fv = Ext(
    'glProgramUniformMatrix4x2fv', None,
    ctypes.c_uint, ctypes.c_int, ctypes.c_int, ctypes.c_ubyte, ctypes.c_void_p
)

glProgramUniformMatrix3x4fv = Ext(
    'glProgramUniformMatrix3x4fv', None,
    ctypes.c_uint, ctypes.c_int, ctypes.c_int, ctypes.c_ubyte, ctypes.c_void_p
)

glProgramUniformMatrix4x3fv = Ext(
    'glProgramUniformMatrix4x3fv', None,
    ctypes.c_uint, ctypes.c_int, ctypes.c_int, ctypes.c_ubyte, ctypes.c_void_p
)

glProgramUniformMatrix2x3dv = Ext(
    'glProgramUniformMatrix2x3dv', None,
    ctypes.c_uint, ctypes.c_int, ctypes.c_int, ctypes.c_ubyte, ctypes.c_void_p
)

glProgramUniformMatrix3x2dv = Ext(
    'glProgramUniformMatrix3x2dv', None,
    ctypes.c_uint, ctypes.c_int, ctypes.c_int, ctypes.c_ubyte, ctypes.c_void_p
)

glProgramUniformMatrix2x4dv = Ext(
    'glProgramUniformMatrix2x4dv', None,
    ctypes.c_uint, ctypes.c_int, ctypes.c_int, ctypes.c_ubyte, ctypes.c_void_p
)

glProgramUniformMatrix4x2dv = Ext(
    'glProgramUniformMatrix4x2dv', None,
    ctypes.c_uint, ctypes.c_int, ctypes.c_int, ctypes.c_ubyte, ctypes.c_void_p
)

glProgramUniformMatrix3x4dv = Ext(
    'glProgramUniformMatrix3x4dv', None,
    ctypes.c_uint, ctypes.c_int, ctypes.c_int, ctypes.c_ubyte, ctypes.c_void_p
)

glProgramUniformMatrix4x3dv = Ext(
    'glProgramUniformMatrix4x3dv', None,
    ctypes.c_uint, ctypes.c_int, ctypes.c_int, ctypes.c_ubyte, ctypes.c_void_p
)
