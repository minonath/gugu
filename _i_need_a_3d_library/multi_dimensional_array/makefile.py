"""
通过加载本模块，导入一些底层的三维函数。
如果没有编译好的文件 (_loadfile.py, _array.dll) 则尝试一次编译，需要准备好环境。
相应的，这两个文件如果编译错误，需要手动删除。

cmake_file:

cmake_minimum_required(VERSION 3.15)
project(multi_dimensional_array C)

set(CMAKE_C_STANDARD 99)

add_library(multi_dimensional_array SHARED _matrix3.c _matrix4.c _quaternion.c
        _vector2.c _vector3.c _vector4.c)
"""

import os
import shutil
import sys

if sys.platform in ('win32', 'cygwin'):
    _library_name = '_array.dll'
elif sys.platform == 'darwin':
    _library_name = '_array.dylib'
else:
    _library_name = '_array.so'

_file_path = os.path.dirname(__file__)

_python_files = ('_matrix3', '_matrix4', '_quaternion',
                 '_vector2', '_vector3', '_vector4')

_library_path = os.path.join(_file_path, _library_name)


def _gcc_make(target):
    _path = os.path.dirname(__file__)

    _objects = []
    _sources = []

    for _source_name in _python_files:
        _py_name = os.path.join(_path, _source_name) + '.py'
        _c_name = os.path.join(_path, _source_name) + '.c'
        _o_name = os.path.join(_path, _source_name) + '.o'
        shutil.copy(_py_name, _c_name)
        os.system('gcc -std=c99 -c %s -o %s' % (_c_name, _o_name))
        _objects.append(_o_name)
        _sources.append(_c_name)

    os.system('gcc -Wall -shared %s -o %s' % (' '.join(_objects), target))
    for _source_name in _sources + _objects:
        os.remove(_source_name)


_target_file = os.path.join(_file_path, '_loadfile.py')

_target_head = """from ._array import VOIDP, FLT, UNSIGNED
from .makefile import _library_path, _gcc_make
import ctypes
import os

__all__ = [
    """

_target_tail = """}

if not os.path.exists(_library_path):
    _gcc_make(_library_path)

try:
    _gu3d = ctypes.cdll.LoadLibrary(_library_path)

    for _name, (_restype, _args_type) in __functions__.items():
        try:
            _function_imp = getattr(_gu3d, _name)
            setattr(_function_imp, 'restype', _restype)
            setattr(_function_imp, 'arg''types', _args_type)
            globals()[_name] = _function_imp
        except AttributeError:
            print(_name)

except OSError:
    from ._matrix3 import *
    from ._matrix4 import *
    from ._quaternion import *
    from ._vector2 import *
    from ._vector3 import *
    from ._vector4 import *
"""


def _create_loadfile(target):
    _module_path = __name__[:__name__.rfind('.')]

    __import__(_module_path + '._matrix3')
    __import__(_module_path + '._matrix4')
    __import__(_module_path + '._quaternion')
    __import__(_module_path + '._vector2')
    __import__(_module_path + '._vector3')
    __import__(_module_path + '._vector4')

    from ._array import _functions, _types

    _lines_0, _lines_1 = [], []

    try:
        with open(target, 'w') as _f:
            _f.write(_target_head)
            for _name, (_restype, _arg_types) in _functions.items():
                _restype = _types[_restype]
                _arg_types = ', '.join(_types[_arg] for _arg in _arg_types)
                _tuple = _name, _restype, _arg_types
                _line = "'%s': (%s, [%s])" % _tuple
                if len(_line) > 75:
                    _line = "'%s':\n        (%s, [%s])" % _tuple
                _lines_0.append("'%s'" % _name)
                _lines_1.append(_line)

            _f.write(',\n    '.join(_lines_0))
            _f.write('\n]\n\n__functions__ = {\n    ')
            _f.write(',\n    '.join(_lines_1))
            _f.write(_target_tail)
    except OSError:
        # 无法写入，放弃写入 p_loadfile，同时因为没有调用 d_array 所以不会生成动态库。
        pass


try:
    from ._loadfile import *

except ModuleNotFoundError:
    _create_loadfile(_target_file)
    try:
        from ._loadfile import *

    except ModuleNotFoundError:
        from ._matrix3 import *
        from ._matrix4 import *
        from ._quaternion import *
        from ._vector2 import *
        from ._vector3 import *
        from ._vector4 import *
