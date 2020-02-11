class _GlobalVariable(dict):
    def __init__(self):
        dict.__init__(self)
        self.__dict__ = self


gu = _GlobalVariable()


def bind_dynamic_library(lib):
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
            def _func(*args):  # 无法加载的函数使用这个
                print('<Error Func>', lib, name, args)

        return _func

    return _bind
