import subprocess
import sys


from ._gu_data import resource


_RUNNING_FILE = 'gu/system/_running.py'  # 新进程启动用脚本的位置


class _Gu:
    """ 用来存放全局的类，是一个单例 """
    def __repr__(self):
        """ 被调用显示的时候，只会显示名称 """

        return 'Gu'

    def __str__(self):
        """ print 的时候可以打印出 __dict__ """

        return str(dict(  # 不显示隐藏内容，特别是 '__builtins__'
            _i for _i in self.__dict__.items() if not _i[0].startswith('_')
        ))

    def __call__(self, *path):
        """ 开启一个新进程窗口，并运行以 path 为基础的模块 """

        subprocess.Popen((sys.executable, _RUNNING_FILE, *path)).wait()

    def _process(self):
        """ 跨进程运行，从某种角度来说，这才是真正的启动函数 """
        from gu.window import Window, input

        if len(sys.argv) > 1:  # 继承 __call__ 的 path 参数，从 sys.argv 调用
            resource.load(*sys.argv[1:])

        self.debug = print
        self.print = print
        self.input = input
        self.window = Window()
        self.window(start=True)


gu = _Gu()

__all__ = ['gu']
