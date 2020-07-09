import subprocess
import sys
import threading

# 作为 __init__ 传递的变量。
from .resource import Resource, default_png
from .other import (KEY_MAP, SYSTEM_PLATFORM, Array, PrintClass,
                    bind_dynamic_library, print_exception )

RUN_FILE = 'gu/system/running.py'


class Gu(object):
    def __repr__(self):  # 被调用显示的时候，只会显示名称。
        return self.__class__.__name__

    def __str__(self):  # print 的时候可以打印出 __dict__ 。
        return str(dict(  # 不显示隐藏内容，特别是 '__builtins__'
            i for i in self.__dict__.items() if not i[0].startswith('_')
        ))

    def __init__(self):
        self.gu = self

    def __call__(self, *path):
        try:
            if path:
                if debug:
                    subprocess.Popen((sys.executable, RUN_FILE, *path)).wait()
                else:
                    subprocess.Popen((sys.executable, RUN_FILE, *path))
            else:
                subprocess.Popen((sys.executable, RUN_FILE)).wait()
        except KeyboardInterrupt:
            print('KeyboardInterrupt')

    def _new_process(self):
        from ..window import Window, gl_context, window_input
        self.context = gl_context
        self.input = window_input
        self.window = window = Window()
        import gu.graphic

        class ConsoleThread(threading.Thread):
            def __del__(self):
                if threading.main_thread().is_alive():
                    window.window_running = False

        ConsoleThread(target=self._new_thread, daemon=True).start()

        try:
            window(start=True)
            print()

        except KeyboardInterrupt:
            pass

    def _new_thread(self):
        exec_global = self.__dict__.copy()
        if len(sys.argv) > 1:
            resource.load(*sys.argv[1:])

        init = resource.get('__main__.py')
        if init:
            try:
                exec(init, exec_global)
            except Exception as e:
                print_exception(e)

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


# window = Window()
resource = Resource()
gu = Gu()


def debug():
    import ctypes
    def _inner():
        uniform = gu.program.texture._program_member['m_proj[0]']
        print(uniform.value)
        a = Array(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, element_nums=16, element_type=ctypes.c_float)
        b = Array(5, 4, 3, 2, 1, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, element_nums=16, element_type=ctypes.c_float)
        uniform.value = a, b
        print(uniform.value)

    gu.window.window_queue.put((_inner, ))


gu.debug = debug
