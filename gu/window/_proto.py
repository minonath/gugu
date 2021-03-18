import queue
import time

from ._input import input

from ..system import resource, gu, null
from ..opengl import context

_QUEUE_LENGTH = 27


class Prototype(object):
    def __repr__(self):
        return self.__class__.__name__

    def __init__(self):
        self.window_running = False

        self._window_title = 'Gu'
        self._window_image = None
        self._window_size = [800, 600]

        self._window_clock = 0
        self._window_interval = 0
        self._window_queue = queue.Queue()

    def _window_sleep(self):
        """ 沉睡一段时间，控制帧数。 """
        _current_clock = time.perf_counter()  # 当前时间
        _frame_clock = _current_clock - self._window_clock  # 上一帧实际经历时间
        _sleep_clock = self._window_interval - _frame_clock  # 需要沉睡的时间
        if _sleep_clock > 0:  # 判断是否掉帧了
            time.sleep(_sleep_clock)  # 没有掉帧就沉睡
        _current_clock = time.perf_counter()  # 再次计算当前时间
        _interval_clock = _current_clock - self._window_clock  # 本次跨越的帧数
        self._window_clock = _current_clock  # 记录
        return _interval_clock  # 返回间隔时间

    def _window_pull(self):
        _size = self._window_queue.qsize()
        if _size:
            _size = _size > _QUEUE_LENGTH and _QUEUE_LENGTH or _size
            while _size:
                _size -= 1
                _cmd = self._window_queue.get_nowait()
                try:
                    _cmd and _cmd[0](*_cmd[1], **_cmd[2])  # 必须三个对象。
                except Exception as e:
                    gu.debug(e)

    def _window_push(self, func, *args, **kwargs):
        self._window_queue.put((func, args, kwargs))

    @staticmethod
    def _window_prepare():
        _exec_global = gu.__dict__.copy()  # 程序的全局就是这个类的变量空间
        _init = resource.get('__main__.py')  # 载入资源文件的启动脚本
        if _init:
            try:
                exec(_init, _exec_global)
            except Exception as e:
                gu.debug(e)

        context.gl_render = _exec_global.get('gl_render', null)

    def __call__(self, func=None, *args, **kwargs):
        if func:  # 如果有 func 就按照 sync 进行
            self._window_queue.put((func, args, kwargs))  # 和 push 一致

        else:  # 没有 func 则设置窗口参数
            mask = 0
            if 'title' in kwargs:
                self._window_title = kwargs['title']
                mask |= 0b1
            if 'image' in kwargs:
                self._window_image = kwargs['image']
                mask |= 0b10
            if 'width' in kwargs:
                self._window_size[0] = kwargs['width']
                mask |= 0b100
            if 'height' in kwargs:
                self._window_size[1] = kwargs['height']
                mask |= 0b100

            if 'fps' in kwargs:
                self._window_interval = 1 / (kwargs['fps'] + 1)

            if self.window_running:
                mask & 0b1 and self._window_set_title()
                mask & 0b10 and self._window_set_image()
                mask & 0b100 and self._window_set_size()
            else:
                if 'start' in kwargs and kwargs['start']:
                    self._window_start()

    def _window_start(self):
        raise NotImplementedError

    def _window_set_title(self):
        raise NotImplementedError

    def _window_set_image(self):
        raise NotImplementedError

    def _window_set_size(self):
        raise NotImplementedError


__all__ = ['input', 'Prototype']
