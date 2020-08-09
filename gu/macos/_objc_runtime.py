"""
下面是 Runtime 绑定，这里只写了一部分常用的 objc 函数，具体可以参考网址：
https://opensource.apple.com/source/objc4/objc4-756.2/
"""
import ctypes
from ._objc_encoding import objc_encodings
from ..system.other import bind_dynamic_library

# 导入 objc 动态库，并制作 objc 绑定函数
_objc_library = ctypes.cdll.LoadLibrary('/usr/lib/lib''objc.dylib')
objc = bind_dynamic_library(_objc_library)


class _ObjCObject(ctypes.Structure):
    """
    objc_object
    """


# 这是 NSObject 的指针，因为以指针传递所以不需要细节
objc_encodings[b'@'] = Id = ctypes.POINTER(_ObjCObject)


class _ObjCClass(_ObjCObject):
    """
    objc_class
    """


objc_encodings[b'#'] = Class = ctypes.POINTER(_ObjCClass)  # 也是一个指针对象
# SEL 是 c_char_p + some_info，如果用 c_char_p 代替会导致丢失信息
objc_encodings[b':'] = Sel = ctypes.c_void_p

Imp = ctypes.c_void_p  # ctypes.CFUNCTYPE(Id, Id, Sel)
Bool = ctypes.c_bool  # C99 _Bool

# 获取 Sel 所包裹的文本信息，可以用 ctypes.cast(sel, ctypes.c_char_p).value 代替
sel_getName = objc('sel_getName', ctypes.c_char_p, Sel)

# c_char_p str
sel_registerName = objc('sel_registerName', Sel, ctypes.c_char_p)

# Id obj
object_getClassName = objc('object_getClassName', ctypes.c_char_p, Id)


class _ObjCMethod(ctypes.Structure):
    """
    objc_method
    """


Method = ctypes.POINTER(_ObjCMethod)

# Id obj
object_getClass = objc('object_getClass', Class, Id)

# c_char_p name
objc_getClass = objc('objc_getClass', Class, ctypes.c_char_p)

# Class cls
class_getName = objc('class_getName', ctypes.c_char_p, Class)

# Class cls, SEL name
class_getInstanceMethod = objc('class_getInstanceMethod', Method, Class, Sel)

# Class cls, SEL name
class_getClassMethod = objc('class_getClassMethod', Method, Class, Sel)

# Class cls, SEL name, IMP imp, c_char_p types
class_addMethod = objc(
    'class_addMethod', Bool, Class, Sel, Imp, ctypes.c_char_p
)

# Class superclass, c_char_p name, c_size_t extraBytes
objc_allocateClassPair = objc(
    'objc_allocateClassPair', Class, Class, ctypes.c_char_p, ctypes.c_size_t
)

# Class cls
objc_registerClassPair = objc('objc_registerClassPair', None, Class)

# Method m
method_getName = objc('method_getName', Sel, Method)

# Method m
method_getImplementation = objc('method_getImplementation', Imp, Method)

# Method m
method_getTypeEncoding = objc(
    'method_getTypeEncoding', ctypes.c_char_p, Method
)

__all__ = [
    'Id', 'Class', 'Sel', 'Imp', 'Bool', 'sel_getName', 'sel_registerName',
    'object_getClassName', '_ObjCMethod', 'Method', 'object_getClass',
    'objc_getClass', 'class_getName', 'class_getInstanceMethod',
    'class_getClassMethod', 'class_addMethod', 'objc_allocateClassPair',
    'objc_registerClassPair', 'method_getName', 'method_getImplementation',
    'method_getTypeEncoding'
]
