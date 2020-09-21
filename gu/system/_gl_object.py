import threading

from ._base import gu


class _OpenGLObjectManager(object):
    """ 用于管理 OpenGL 显卡对象，也是一个单例 """

    def __repr__(self):
        return 'OpenGLObjectManager'

    def __str__(self):
        return str(self.__dict__)

    def __setattr__(self, key, value):
        def _gl_destroy():
            getattr(value, '_release')()
            delattr(self, key)

        setattr(value, 'gl_destroy', _gl_destroy)
        object.__setattr__(self, key, value)

    def seek(self, name):
        for _obj in self.__dict__.values():
            if str(_obj) == name:
                return _obj


gl_objects = _OpenGLObjectManager()


def _main_thread(func):
    def _wrap(*args, **kwargs):
        if threading.current_thread() == threading.main_thread():  # 主线程
            # and gu.window.window_running):  # 线程开启前
            func(*args, **kwargs)
        else:
            gu.window(func, *args, **kwargs)  # 需要 gu 有 queue 方法

    return _wrap


class _OpenGLObjectMeta(type):
    """ OpenGL 对象元类，确保所有对象相关的函数都在主线程运行 """

    def __new__(mcs, name, bases, namespace):
        for _k, _v in namespace.copy().items():
            if not _k.startswith('__') and callable(_v):
                namespace[_k] = _main_thread(_v)

        return type.__new__(mcs, name, bases, namespace)


class OpenGLObject(metaclass=_OpenGLObjectMeta):
    """
    OpenGL 对象类
    因为线程的特殊性质，所有方法都不能有稳定的返回值，所以统一不设置返回值
    """

    def __repr__(self):
        return self.__class__.__name__  # 会被继承

    def __str__(self):
        return self._string

    def __init__(self, *args, **kwargs):
        _index_name = hex(id(self))  # 用自身的内存指针做索引
        self._string = '<object at %s>' % _index_name  # 可以进行修改
        setattr(gl_objects, _index_name, self)
        self._initial(*args, **kwargs)

    def _initial(self, *args, **kwargs):
        """ 需要重新给 self._string 赋值 """

        raise NotImplementedError

    def _release(self):
        """
        回收用函数，主动使用用 gl_object.gl_destroy()
        直接运行这个函数可以清除显卡序列，但是 gl_objects 缓存无法去除
        """

        raise NotImplementedError

    def gl_destroy(self):
        ...


__all__ = ['gl_objects', 'OpenGLObject']
