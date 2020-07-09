import ctypes
from ._objc_encoding import objc_type_from_encoding, objc_encodings
from ._objc_runtime import *

# 这里把 Foundation 的函数库导入 Runtime 否则 Runtime 里面找不到 NSString 类。
ctypes.cdll.LoadLibrary(
    '/System/Library/Frameworks/Foundation.framework/Foundation'
)

_class_cache = {}
_method_cache = {}


def _objc_method(class_type, get_function, method_name):
    _selector = sel_registerName(method_name)  # 注册 Sel 。

    _method = get_function(class_type, _selector)  # 提取 Method 信息。
    _implementation = method_getImplementation(_method)
    _encoding = method_getTypeEncoding(_method)
    if not _encoding:
        raise ValueError(method_name, '不存在该函数')

    _return_type, _argument_types = objc_type_from_encoding(_encoding)
    _func_type = ctypes.CFUNCTYPE(_return_type, *_argument_types)
    _implementation = ctypes.cast(_implementation, _func_type)

    setattr(_implementation, 'restype', _return_type)
    setattr(_implementation, 'arg''types', _argument_types)
    setattr(_implementation, 'encodings', _encoding)

    return _implementation, _selector


def _objc_class(name_or_instance, method_name):
    method_name = method_name.encode('utf-8')
    if isinstance(name_or_instance, str):  # 表示这是一个类。
        _class_name = name_or_instance.encode('utf-8')

        if _class_name in _class_cache:
            _class_type = _class_cache[_class_name]
        else:
            _class_type = objc_getClass(_class_name)
            if class_getName(_class_type) == b'nil':  # 未拥有相关类会调用错误。
                raise NameError('Class<%s> Not In Runtime.' % _class_name)
            _class_cache[_class_name] = _class_type

        if (_class_name, method_name) in _method_cache:
            _imp, _sel = _method_cache[_class_name, method_name]
        else:
            _imp, _sel = _objc_method(
                _class_type, class_getClassMethod, method_name
            )
            _method_cache[_class_name, method_name] = _imp, _sel

        _first_argument = _class_type

    else:  # 表示这是一个进程
        _class_type = object_getClass(name_or_instance)
        _class_name = class_getName(_class_type)

        if (_class_name, method_name) in _method_cache:
            _imp, _sel = _method_cache[_class_name, method_name]
        else:
            _imp, _sel = _objc_method(
                _class_type, class_getInstanceMethod, method_name
            )
            _method_cache[_class_name, method_name] = _imp, _sel

        _first_argument = name_or_instance

    return _imp, _first_argument, _sel


def _objc_run(name_or_instance, method_name, *args):
    _imp, _first_argument, _sel = _objc_class(name_or_instance, method_name)
    return _imp(_first_argument, _sel, *args)


def _objc_run_with_fit(name_or_instance, method_name, *args):
    # 支持 Structure Union Array，仅做输入辅助用，所以不支持指针

    _imp, _first_argument, _sel = _objc_class(name_or_instance, method_name)
    _fitted = (
        _imp.argtypes[i].auto_fit(a)
        if isinstance(a, tuple) else a
        for i, a in enumerate(args, 2)  # 从第三个开始算
    )
    return _imp(_first_argument, _sel, *_fitted)


def _objc_make_ns_string(text):
    return OBJC('NSString', 'stringWithUTF8String:', text.encode('utf-8'))


def _objc_make_sel(text):
    return sel_registerName(text.encode('utf-8'))


def _objc_create_class(class_name, super_name):
    subclass = objc_getClass(class_name.encode('utf-8'))
    if class_getName(subclass) != b'nil':  # 重复加载会引发错误。
        raise NameError('Class<%s> Is Created.' % class_name)
    superclass = objc_getClass(super_name.encode('utf-8'))
    subclass = objc_allocateClassPair(
        superclass, class_name.encode('utf-8'), 0
    )
    objc_registerClassPair(subclass)
    return subclass


def _objc_bind_method_decorator(class_type, method_name, encoding):
    _class_name = object_getClassName(class_type)
    method_name = method_name.encode('utf-8')
    encoding = encoding.encode('utf-8')

    _method_sel = sel_registerName(method_name)
    _return_type, _argument_types = objc_type_from_encoding(encoding)
    _c_function = ctypes.CFUNCTYPE(_return_type, *_argument_types)

    def _bind(_function):
        _method_cache[_class_name, method_name] = k = _c_function(_function)
        class_addMethod(class_type, _method_sel, k, encoding)
        return _function

    return _bind


def _objc_find_type_encoding(*type_name):
    type_name = tuple(t.encode('utf-8') for t in type_name)
    for name in objc_encodings.keys():
        if name.startswith(b'{'):
            real_name = name[1:name.find(b'=')]
            if real_name in type_name:
                real_type = objc_encodings[name]
                return (name.decode('utf-8'), real_type,
                        ctypes.sizeof(real_type))


OBJC = _objc_run
FIT = _objc_run_with_fit
STR = _objc_make_ns_string
SEL = _objc_make_sel
SUBCLASS = _objc_create_class
BIND = _objc_bind_method_decorator
FIND = _objc_find_type_encoding

__all__ = ['OBJC', 'FIT', 'STR', 'SEL', 'SUBCLASS', 'BIND', 'FIND']
