import threading
from ..system import gu

_prevent_auto_collect = dict()


class OpenGLObjectManager(object):
    def __repr__(self):
        return self.__class__.__name__

    def __str__(self):
        return '警告：请勿调用下列变量的任何方法！\n%s' % self.__dict__

    def __delattr__(self, item):
        def _inner_thread():
            _prevent_auto_collect.pop(item).gl_release()
            super(OpenGLObjectManager, self).__delattr__(item)

        gu.window.window_queue.put((_inner_thread,))


gu.context.objects = gl_objects = OpenGLObjectManager()


class PrintClass(type):
    def __repr__(self):
        return self.__name__

    def __str__(self):
        return self.__name__


class OpenGLObject(metaclass=PrintClass):
    # init 以外所有函数需要在主线程运行，注意不要误用。

    def __init__(self):
        self.__string__ = ''

        def _inner_thread():  # 在这里加入 Manager
            self.__string__ = self.gl_initialize()
            setattr(gl_objects, self.__string__, self)
            _prevent_auto_collect[self.__string__] = self

        if threading.current_thread() == threading.main_thread():
            _inner_thread()  # 如果在其他线程运行的话，会导致问题。
        else:
            gu.window.window_queue.put((_inner_thread,))

    def gl_initialize(self) -> str:
        raise NotImplementedError

    def gl_release(self) -> None:
        raise NotImplementedError


__all__ = ['OpenGLObject']
