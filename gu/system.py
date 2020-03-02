import sys


class Gu(dict):
    if sys.platform in ('win32', 'cygwin'):
        platform = 0
    elif sys.platform == 'darwin':
        platform = 1
    else:
        platform = 2

    def __init__(self):
        dict.__init__(self)
        self.__dict__ = self

    @staticmethod
    def bind_dynamic_library(lib, fallback=None):
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
                    _func = fallback(name, restype, *arg_types)
                else:
                    def _func(*args):  # 无法加载的函数，默认使用这个
                        print('<Error Func>', lib, name, args)

            return _func

        return _bind


gu = Gu()
