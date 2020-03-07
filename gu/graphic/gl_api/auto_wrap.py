import pathlib
import ctypes
from gu.system import gu

if gu.platform == 0:
    class E(object):
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


    gl = gu.bind_dynamic_library(ctypes.windll.opengl32, E)
    _wglGetFunction = gl('wglGetP''rocAddress',
                         ctypes.CFUNCTYPE(ctypes.POINTER(ctypes.c_int)),
                         ctypes.c_char_p)


elif gu.platform == 1:
    E = gl = gu.bind_dynamic_library(ctypes.cdll.LoadLibrary(
        '/System/Library/Framework/OpenGL.framework/OpenGL'
    ))

else:
    import ctypes.util

    E = gl = gu.bind_dynamic_library(ctypes.cdll.LoadLibrary(
        ctypes.util.find_library('OpenGL')
    ))


Int = ctypes.c_int
UInt = ctypes.c_uint
Byte = ctypes.c_byte
UByte = ctypes.c_ubyte
UShort = ctypes.c_ushort
Float = ctypes.c_float
VoidP = ctypes.c_void_p
CharP = ctypes.c_char_p
P = ctypes.POINTER
C = ctypes.CFUNCTYPE
Double = ctypes.c_double
Short = ctypes.c_short
Size = ctypes.c_size_t
UInt64 = ctypes.c_uint64
Int64 = ctypes.c_int64
Int32 = ctypes.c_int32
Handle = Size if gu.platform == 1 else UInt


class __GLSync(ctypes.Structure):
    ...


GLSync = ctypes.POINTER(__GLSync)


_ShortName = {
    'GLenum': 'UInt',
    'GLboolean': 'UByte',
    'GLbitfield': 'UInt',
    'GLbyte': 'Byte',
    'GLint': 'Int',
    'GLsizei': 'Int',
    'GLubyte': 'UByte',
    'GLushort': 'UShort',
    'GLuint': 'UInt',
    'GLfloat': 'Float',
    'GLclampf': 'Float',
    'GLclampd': 'Double',
    'GLvoid': 'None',
    'void': 'None',
    'GLdouble': 'Double',
    'GLshort': 'Short',
    'GLsync': 'GLSync',
    'GLsizeiptr': 'Size',
    'GLintptr': 'Size',
    'GLchar': 'Char',
    'GLuint64': 'UInt64',
    'GLint64': 'Int64',
    '_cl_context': 'None',
    '_cl_event': 'None',
    'GLuint64EXT': 'UInt64',
    'GLhandleARB': 'Handle',
    'GLcharARB': 'Char',
    'GLsizeiptrARB': 'Size',
    'GLintptrARB': 'Size',
    'GLfixed': 'Int32',
    'GLint64EXT': 'Int64',
    'GLeglImageOES': 'VoidP',
    'GLeglClientBufferEXT': 'VoidP',
    'GLhalfNV': 'UShort',
    'GLvdpauSurfaceNV': 'Size',
}


def _get_translate_of(gl_name):
    return _ShortName.get(gl_name, gl_name)


def _get_pointer_of(name):
    if name == 'None':
        return 'VoidP'
    elif name == 'Char':
        return 'CharP'
    else:
        return 'P(%s)' % name


def _get_constant_of(line):
    """
    从一行 define 中提取常量
    """
    space_split = tuple(k for k in line.split(' ') if k)
    if space_split[1].startswith('GL_'):
        constant_name = space_split[1]
        constant_value = space_split[2].replace('u', '').replace('l', '')
        return constant_name, constant_value


def _get_function_of(line):
    line = line.replace('typedef', ' ')
    line = line.replace('struct', ' ')
    line = line.replace('GLAPI', ' ')
    line = line.replace('WINGDIAPI', ' ')
    line = line.replace('APIENTRYP', ', *')  # 注意 P
    line = line.replace('APIENTRY', ', ')
    line = line.replace('(', ' ')
    line = line.replace(')', ' ')
    line = line.replace(';', ' ')
    line = line.replace('const', ' ')
    line = line.replace('*', ' * ')  # 前后都会有问题
    comma_split = line.split(',')
    return_split = tuple(k for k in comma_split[0].split(' ') if k)  # 返回值

    if len(return_split) == 1:
        function_return = _get_translate_of(return_split[0])
    elif len(return_split) == 2 and return_split[1] == '*':
        function_return = _get_pointer_of(_get_translate_of(return_split[0]))
    else:
        raise ValueError(line)  # 暂时还没有返回 void ** 的

    name_split = tuple(k for k in comma_split[1].split(' ') if k)

    if name_split[0] == '*':
        function_name = name_split[1]
        function_argument = _get_translate_of(name_split[2])
        if len(name_split) > 3 and name_split[3] == '*':
            function_argument = _get_pointer_of(function_argument)
            if name_split[4] == '*':
                function_argument = _get_pointer_of(function_argument)
    else:
        function_name = name_split[0]
        function_argument = _get_translate_of(name_split[1])
        if len(name_split) > 2 and name_split[2] == '*':
            function_argument = _get_pointer_of(function_argument)
            if name_split[3] == '*':
                function_argument = _get_pointer_of(function_argument)

    if len(comma_split) > 2:  # 后续参数
        function_argument = [function_argument]

        for other in comma_split[2:]:
            space_split = tuple(k for k in other.split(' ') if k)
            meow = _get_translate_of(space_split[0])
            if space_split[1] == '*':
                meow = _get_pointer_of(meow)  # 当出现 * 的时候，追加一次 * 确认
                if space_split[2] == '*':  # 因为会出现 char ** shader 这样的值
                    meow = _get_pointer_of(meow)
            function_argument.append(meow)

        function_argument = ', '.join(function_argument)

    return function_name, function_return, function_argument


_current_directory = pathlib.Path(__file__).resolve().parent
_gl_wrap_name = []
_import_head = 'from %s import *\n\n' % __name__[__name__.rfind('.'):]


def _write_gl_wrap_file(head_file):
    head_file = _current_directory.joinpath(head_file).open()
    file_name = None
    wrap_file = None
    all_set = []

    for line in head_file.readlines():
        line = line.replace('\n', ' ')
        if line.startswith('#ifndef'):  # 用于分割文件
            define_name = line.split(' ')[1]
            if define_name.startswith('GL_'):
                underscore_split = define_name.split('_')
                if underscore_split[1] == 'VERSION':
                    version_name = '_GL_{0}{1}'.format(
                        underscore_split[2], underscore_split[3])
                    _gl_wrap_name.append(version_name)
                elif underscore_split[1] == 'EXT':
                    version_name = '_{0}'.format(define_name)
                else:
                    version_name = '_GL_{0}'.format(underscore_split[1])
                if file_name != version_name:
                    file_name = version_name
                    if wrap_file:
                        wrap_file.write("\n__all__ = ['%s']\n" % (
                            "', '".join(all_set)))
                        all_set.clear()
                        wrap_file.close()
                    wrap_file = _current_directory.joinpath(
                        file_name).with_suffix('.py').open(mode='w')
                    wrap_file.write(_import_head)
            continue

        if not wrap_file:
            continue

        if line.startswith('#define'):
            constant = _get_constant_of(line)
            if constant:
                wrap_file.write('%s = %s\n' % constant)
                all_set.append(constant[0])

        elif line.startswith('GLAPI'):
            a, b, c = _get_function_of(line)
            if c == 'None':
                wrap_file.write("{0} = E('{0}', {1})\n".format(a, b))
            else:
                wrap_file.write("{0} = E('{0}', {1}, {2})\n".format(a, b, c))
            all_set.append(a)

        elif line.startswith('typedef') and 'APIENTRY' in line:
            a, b, c = _get_function_of(line)
            if c == 'None':
                wrap_file.write("{0} = C({1})\n".format(a, b))
            else:
                wrap_file.write("{0} = C({1}, {2})\n".format(a, b, c))
            all_set.append(a)

    if wrap_file:
        wrap_file.close()

    head_file.close()


def compile_wrap_file():
    """
    这里写入的 __init__.py 只加载了 CoreGL，扩展需要自己添加，重新进行排版
    """
    _gl_wrap_name.clear()

    # 这两个文件是从 ming-w64 里复制出来的
    # _write_gl_wrap_file('gl_from_mingw64.h')
    # _write_gl_wrap_file('glext_from_mingw64.h')

    # 可以从下面网址获得 Extension 更新
    # github.com/KhronosGroup/OpenGL-Registry/blob/master/api/GL/glext.h
    # _write_gl_wrap_file('glext_from_khronos.h')

    # github.com/KhronosGroup/OpenGL-Registry/blob/master/api/GL/glcorearb.h
    _write_gl_wrap_file('glcorearb_from_khronos.h')

    with _current_directory.joinpath('__init__.py').open(mode='w') as f:
        f.write(''.join('from .%s import *\n' % k for k in _gl_wrap_name))
        f.write('\n\nclass OpenGLError(Exception):\n    ...\n')
