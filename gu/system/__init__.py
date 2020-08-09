import subprocess
import sys
import threading

# 作为 __init__ 传递的变量。
from .resource import Resource, default_png
from .other import (
    KEY_MAP, SYSTEM_PLATFORM, Array, PrintClass, bind_dynamic_library,
    null_function, print_exception
)

RUNNING_FILE = 'gu/system/running.py'
DEBUG = 'gu/system/debug.py'


class Gu(object):
    def __repr__(self):  # 被调用显示的时候，只会显示名称。
        return self.__class__.__name__

    def __str__(self):  # print 的时候可以打印出 __dict__ 。
        return str(dict(  # 不显示隐藏内容，特别是 '__builtins__'
            i for i in self.__dict__.items() if not i[0].startswith('_')
        ))

    def __init__(self):
        self.gu = self
        self.print = null_function

    def __call__(self, *path, debug=False):
        if not path:
            debug = True
        try:
            if debug:
                subprocess.Popen((sys.executable, DEBUG, *path)).wait()
            else:
                subprocess.Popen((sys.executable, RUNNING_FILE, *path))
        except KeyboardInterrupt:
            print('KeyboardInterrupt')

    def __loading__(self):
        from ..window import Window, gl_context, window_input
        self.window = window = Window()
        self.context = gl_context
        self.input = window_input

        from ..graphic import gl_objects, program_manager
        self.program = program_manager
        self.context.objects = gl_objects

        return window

    def __process__(self, debug=False):
        window = self.__loading__()  # 窗口不能提前创建，会引起循环导入失败。

        class ConsoleThread(threading.Thread):
            def __del__(self):
                if threading.main_thread().is_alive():
                    window.window_running = False

        if debug:
            ConsoleThread(target=self.__console__, daemon=True).start()
        else:
            ConsoleThread(target=self.__running__, daemon=True).start()

        try:
            window.window_queue.get(block=True)
            window(start=True)
            print()  # 运行结束后换一个行。

        except KeyboardInterrupt:
            pass

    def __running__(self):
        exec_global = self.__dict__.copy()
        if len(sys.argv) > 1:
            resource.load(*sys.argv[1:])

        init = resource.get('__main__.py')
        if init:
            try:
                exec(init, exec_global)
            except Exception as e:
                print_exception(e)

        self.window.window_queue.put(None)

    def __console__(self):
        exec_global = self.__dict__.copy()
        exec_global['print'] = print

        if len(sys.argv) > 1:
            resource.load(*sys.argv[1:])

        init = resource.get('__main__.py')
        if init:
            try:
                exec(init, exec_global)
            except Exception as e:
                print_exception(e)

        self.window.window_queue.put(None)

        while True:
            try:
                command = input('gu>')
                if command and command[-1] in ('\\', ':'):  # 不考虑 () [] {}
                    multi_line = [command]
                    while True:
                        next_line = input('...')
                        if next_line:
                            multi_line.append(next_line)
                        else:
                            break
                    command = '\n'.join(multi_line)

                try:
                    result = eval(command, exec_global)
                    if result:
                        print(result)
                except SyntaxError:
                    try:
                        exec(command, exec_global)
                    except Exception as e:
                        print_exception(e)
                except Exception as e:
                    print_exception(e)
            except Exception as e:
                print_exception(e)
                break


resource = Resource()
gu = Gu()


# def debug():
#     import ctypes
#     def _inner():
#         uniform = gu.program.texture._program_member['m_proj[0]']
#         print(uniform.value)
#         a = Array(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, element_nums=16, element_type=ctypes.c_float)
#         b = Array(5, 4, 3, 2, 1, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, element_nums=16, element_type=ctypes.c_float)
#         uniform.value = a, b
#         print(uniform.value)
#
#     gu.window.window_queue.put((_inner, ))


# gu.debug = True
# import queue
# _debug_list = queue.Queue()
# def null_func(*args, **kwargs):
#     pass
# def gu_print(*args):
#     _debug_list.put(args)
# def debug_info():
#     for m in range(_debug_list.qsize()):
#         print(_debug_list.get())


# gu.debug = False
