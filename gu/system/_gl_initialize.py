import ctypes
import pathlib

from ._other import SYSTEM_PLATFORM, bind_dynamic_library

# OpenGL 使用到的变量类型
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
if SYSTEM_PLATFORM == 1:
    Handle = UInt
elif SYSTEM_PLATFORM == 2:
    Handle = Size
else:
    raise NotImplementedError


class _GLSync(ctypes.Structure):
    ...


GLSync = P(_GLSync)

if SYSTEM_PLATFORM == 1:  # 适配不同的系统
    class E(object):  # 扩展函数调用

        def __init__(self, name, restype, *arg_types):
            self._func = None
            self._name = bytes(ord(_c) for _c in name)
            self._type = ctypes.WINFUNCTYPE(restype, *arg_types)

        def __call__(self, *args):
            if self._func is None:  # 第一次调用勾取函数指针
                _address = _wglGetFunction(self._name)
                if not ctypes.cast(_address, P(Handle)):
                    return None
                self._func = ctypes.cast(_address, self._type)

            return self._func(*args)


    gl = bind_dynamic_library(ctypes.windll.opengl32, E)  # 非扩展函数调用
    _wglGetFunction = gl('wglGetP''rocAddress', C(P(Handle)), CharP)


elif SYSTEM_PLATFORM == 2:
    E = gl = bind_dynamic_library(ctypes.cdll.LoadLibrary(
        '/System/Library/Framework/OpenGL.framework/OpenGL'
    ))

else:
    import ctypes.util

    E = gl = bind_dynamic_library(ctypes.cdll.LoadLibrary(
        ctypes.util.find_library('OpenGL')
    ))

_ShortName = {
    'GL''enum': 'UInt',
    'GL''boolean': 'UByte',
    'GL''bitfield': 'UInt',
    'GL''byte': 'Byte',
    'GLint': 'Int',
    'GL''size''i': 'Int',
    'GLu''byte': 'UByte',
    'GLu''short': 'UShort',
    'GLu''int': 'UInt',
    'GL''float': 'Float',
    'GL''clamp''f': 'Float',
    'GL''clamp''d': 'Double',
    'GL''void': 'None',
    'void': 'None',
    'GL''double': 'Double',
    'GL''short': 'Short',
    'GL''sync': 'GLSync',
    'GL''size''i''ptr': 'Size',
    'GL''int''ptr': 'Size',
    'GL''char': 'Char',
    'GLu''int64': 'UInt64',
    'GLint64': 'Int64',
    '_cl_context': 'None',
    '_cl_event': 'None',
    'GLu''int64EXT': 'UInt64',
    'GL''handleARB': 'Handle',
    'GL''charARB': 'Char',
    'GL''size''i''ptrARB': 'Size',
    'GL''int''ptrARB': 'Size',
    'GL''fixed': 'Int32',
    'GL''int64EXT': 'Int64',
    'GL''eglImageOES': 'VoidP',
    'GL''eglClientBufferEXT': 'VoidP',
    'GL''halfNV': 'UShort',
    'GL''vd''pauSurfaceNV': 'Size',  # Video Decode & Presentation API 4 Unix
}


def _get_translate_of(gl_name):
    """ 把头文件里的特殊变量类型，转换为可识别的变量类型 """

    return _ShortName.get(gl_name, gl_name)


def _get_pointer_of(name):
    """ 转换指针对象 """

    if name == 'None':
        return 'VoidP'
    elif name == 'Char':
        return 'CharP'
    else:
        return 'P(%s)' % name


def _get_constant_of(line):
    """ 从一行 define 中提取常量 """

    _space_split = tuple(_k for _k in line.split(' ') if _k)
    if _space_split[1].startswith('GL_'):
        _constant_name = _space_split[1]
        _constant_value = _space_split[2].replace('u', '').replace('l', '')
        return _constant_name, _constant_value


def _get_function_of(line):
    """ 将一行内容转换为函数方法 """

    _line = line \
        .replace('typedef', ' ') \
        .replace('str''uct', ' ') \
        .replace('GL''API', ' ') \
        .replace('WIN''GDI''API', ' ') \
        .replace('API''ENTRY''P', ', *') \
        .replace('API''ENTRY', ', ') \
        .replace('(', ' ') \
        .replace(')', ' ') \
        .replace(';', ' ') \
        .replace('const', ' ') \
        .replace('*', ' * ')  # 注意 P 和 * 前后都会有问题

    _comma_split = _line.split(',')

    # 返回值
    _return_split = tuple(_k for _k in _comma_split[0].split(' ') if _k)

    if len(_return_split) == 1:
        _function_return = _get_translate_of(_return_split[0])
    elif len(_return_split) == 2 and _return_split[1] == '*':
        _function_return = _get_pointer_of(
            _get_translate_of(_return_split[0]))
    else:
        raise ValueError(_line)  # 暂时还没有返回 void ** 的

    _name_split = tuple(_k for _k in _comma_split[1].split(' ') if _k)

    if _name_split[0] == '*':
        _function_name = _name_split[1]
        _function_argument = _get_translate_of(_name_split[2])
        if len(_name_split) > 3 and _name_split[3] == '*':
            _function_argument = _get_pointer_of(_function_argument)
            if _name_split[4] == '*':
                _function_argument = _get_pointer_of(_function_argument)
    else:
        _function_name = _name_split[0]
        _function_argument = _get_translate_of(_name_split[1])
        if len(_name_split) > 2 and _name_split[2] == '*':
            _function_argument = _get_pointer_of(_function_argument)
            if _name_split[3] == '*':
                _function_argument = _get_pointer_of(_function_argument)

    if len(_comma_split) > 2:  # 后续参数
        _function_argument = [_function_argument]

        for _other in _comma_split[2:]:
            _space_split = tuple(_k for _k in _other.split(' ') if _k)
            _meow = _get_translate_of(_space_split[0])
            if _space_split[1] == '*':
                _meow = _get_pointer_of(_meow)  # 当出现 * 的时候，追加一次确认
                if _space_split[2] == '*':  # 因为会出现 char ** shader 这样的值
                    _meow = _get_pointer_of(_meow)
            _function_argument.append(_meow)

        _function_argument = ', '.join(_function_argument)

    return _function_name, _function_return, _function_argument


def _pep8_line(single_line):
    """ 简易的修改为 PEP8 格式 """

    if len(single_line) < 79:
        return single_line + '\n'

    _result = []
    _last_line = single_line[-1:] + '\n'
    _handle_line = single_line[:-1]
    _first_line = _handle_line[:78]
    _k = _first_line.find('(') + 1
    if _k == 0:
        _k = _first_line.find('[') + 1

    _result.append(_first_line[:_k])
    _handle_line = '    ' + _handle_line[_k:]

    while len(_handle_line) >= 79:
        _next_line = _handle_line[:78]
        _k = _next_line.rfind(',') + 1
        _result.append(_handle_line[:_k])
        _handle_line = '   ' + _handle_line[_k:]  # 这里只要三个

    _result.append(_handle_line)
    _result.append(_last_line)
    return '\n'.join(_result)


def _write_gl_wrap_file(head_file, target_directory):
    """ 简易的 OpenGL 头文件翻写 """

    _head_file = head_file.open()  # __name__[:__name__.rfind('.')]
    _import_head = 'from gu.system import *\n\n'

    _file_name = None
    _wrap_file = None
    _all_set = []
    _wrap_name = []

    for _line in _head_file.readlines():
        _line = _line.replace('\n', ' ')
        if _line.startswith('#ifndef'):  # 用于分割文件
            _define_name = _line.split(' ')[1]
            if _define_name.startswith('GL_'):
                _underscore_split = _define_name.split('_')
                if _underscore_split[1] == 'VERSION':
                    _version_name = '_GL_{0}{1}'.format(
                        _underscore_split[2], _underscore_split[3])
                    _wrap_name.append(_version_name)
                elif _underscore_split[1] == 'EXT':
                    _version_name = '_{0}'.format(_define_name)
                else:
                    _version_name = '_GL_{0}'.format(_underscore_split[1])
                if _file_name != _version_name:
                    _file_name = _version_name
                    if _wrap_file:
                        _wrap_file.write('\n')
                        _wrap_file.write(_pep8_line(
                            "__all__ = ['%s']" % ("', '".join(_all_set))
                        ))
                        _all_set.clear()
                        _wrap_file.close()
                    _wrap_file = target_directory.joinpath(
                        _file_name).with_suffix('.py').open(mode='w')
                    _wrap_file.write(_import_head)
            continue

        if not _wrap_file:
            continue

        if _line.startswith('#define'):
            _constant = _get_constant_of(_line)
            if _constant:
                _wrap_file.write('%s = %s\n' % _constant)
                _all_set.append(_constant[0])

        elif _line.startswith('GL''API'):
            _a, _b, _c = _get_function_of(_line)
            if _c == 'None':
                _wrap_file.write(_pep8_line(
                    "{0} = E('{0}', {1})".format(_a, _b)
                ))
            else:
                _wrap_file.write(_pep8_line(
                    "{0} = E('{0}', {1}, {2})".format(_a, _b, _c)
                ))
            _all_set.append(_a)

        elif _line.startswith('typedef') and 'API''ENTRY' in _line:
            _a, _b, _c = _get_function_of(_line)
            if _c == 'None':
                _wrap_file.write(_pep8_line(
                    '{0} = C({1})'.format(_a, _b)
                ))
            else:
                _wrap_file.write(_pep8_line(
                    '{0} = C({1}, {2})'.format(_a, _b, _c)
                ))
            _all_set.append(_a)

    if _wrap_file:
        _wrap_file.close()

    _head_file.close()

    return _wrap_name


def compile_gl_file():
    """
    这里写入的 __init__.py 只加载了 CoreGL，扩展需要自己添加，重新进行排版
    """

    _head_file = pathlib.Path('gu/system/_gl_core_arb.h').resolve()
    _target_directory = pathlib.Path('gu/open''gl').resolve()
    if not _target_directory.exists():
        _target_directory.mkdir()

    # 可以从下面网址获得 CoreArb Extension 更新
    # https://github.com/KhronosGroup/OpenGL-Registry/blob/master/api/GL/
    _module_name = _write_gl_wrap_file(_head_file, _target_directory)

    with _target_directory.joinpath('__init__.py').open(mode='w') as _f:
        _f.write(''.join('from .%s import *\n' % k for k in _module_name))
        _f.write('\n\nclass OpenGLError(Exception):\n    ...\n')
        _f.write('\n\ndef gl_getattr(name):\n    return globals().get(name)')
        _f.write('\n\n\ndef gl_tostring(e):\n    ')
        _f.write('return tuple(k for k, v in globals().items() if v == e)\n')


__all__ = [
    'compile_gl_file', 'gl', 'E', 'P', 'C', 'Int', 'UInt', 'Byte', 'UByte',
    'UShort', 'Float', 'VoidP', 'CharP', 'Double', 'Short', 'Size', 'UInt64',
    'Int64', 'Int32', 'Handle', 'GLSync'
]
