import subprocess
import sys
import traceback

from ._resource import resource


def _print_exception(e):
    """ 错误输出，在窗口内显示 """
    debug = print

    debug(''.join(traceback.format_exception(e, e, e.__traceback__)))


_RUNNING_FILE = 'gu/system/_running.py'


class _Gu(object):
    """
    用来存放全局的类，是一个 Singleton 单例
    """

    def __repr__(self):
        """ 被调用显示的时候，只会显示名称 """

        return 'Gu'

    def __str__(self):
        """ print 的时候可以打印出 __dict__ """

        return str(dict(  # 不显示隐藏内容，特别是 '__builtins__'
            _i for _i in self.__dict__.items() if not _i[0].startswith('_')
        ))

    def __call__(self, *path):
        """
        开启一个新进程窗口，并运行以 path 为基础的模块
        即使关闭当前进程，也不会影响位于新进程的窗口
        当然，可以直接运行 gu/system/_running.py 就不会多进程启动了
        命令行 python3 gu/system/_running.py path1 path2 ...
        """

        subprocess.Popen((sys.executable, _RUNNING_FILE, *path)).wait()

    def _process(self):
        """ 跨进程运行，从某种角度来说，这个函数才是真正的启动函数 """
        from ..window import Window

        if len(sys.argv) > 1:  # 继承 __call__ 的 path 参数，从 sys.argv 调用
            resource.load(*sys.argv[1:])

        self.debug = _print_exception
        self.print = print

        self.window = Window()
        self.window(start=True)


gu = _Gu()


__all__ = ['gu']
