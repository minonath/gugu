import ctypes
import queue
import time

from ..geometry import project_matrix, camera_matrix
from ..system import print_exception

try:
    from ..opengl import *
except ModuleNotFoundError:
    from ..opengl.auto_wrap import compile_wrap_file  # 修复文件。
    compile_wrap_file()
    from ..opengl import *


class WindowInput(object):
    def __repr__(self):
        return self.__class__.__name__

    def __init__(self):
        self.mouse_x = 0
        self.mouse_y = 0

    def mouse_enter(self, mouse_x, mouse_y):
        pass

    def mouse_exit(self, mouse_x, mouse_y):
        pass

    def mouse_move(self, delta_x, delta_y):
        pass

    def mouse_scroll_wheel(self, delta_x, delta_y):
        pass

    def mouse_down(self, mouse_x, mouse_y):
        pass

    def mouse_dragged(self, delta_x, delta_y):
        pass

    def mouse_up(self, mouse_x, mouse_y):
        pass

    def right_down(self, mouse_x, mouse_y):
        pass

    def right_dragged(self, delta_x, delta_y):
        pass

    def right_up(self, mouse_x, mouse_y):
        pass

    def other_down(self, mouse_x, mouse_y):
        pass

    def other_dragged(self, delta_x, delta_y):
        pass

    def other_up(self, mouse_x, mouse_y):
        pass

    def resize(self, width, height):
        pass

    def key_input(self, key_code):
        pass


class OpenGLContext(object):
    def __repr__(self):
        return self.__class__.__name__

    def __str__(self):
        return str(self.__dict__)

    def __init__(self):
        self.project_view = 0
        self.camera_view = 0

        self.gl_version = 0
        self.max_samples = 0
        self.max_integer_samples = 0
        self.max_color_attachments = 0
        self.max_texture_units = 0
        self.default_texture_unit = 0
        self.max_anisotropy = 0
        self.bound_frame_buffer = 0

    def prepare(self):
        tmp = ctypes.c_int()
        glGetIntegerv(GL_MAJOR_VERSION, tmp)
        self.gl_version = tmp.value * 100
        glGetIntegerv(GL_MINOR_VERSION, tmp)
        self.gl_version += tmp.value * 10

        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_TEXTURE_CUBE_MAP_SEAMLESS)

        glEnable(GL_PRIMITIVE_RESTART)
        glPrimitiveRestartIndex(-1)

        glGetIntegerv(GL_MAX_SAMPLES, tmp)
        self.max_samples = tmp.value

        glGetIntegerv(GL_MAX_INTEGER_SAMPLES, tmp)
        self.max_integer_samples = tmp.value

        glGetIntegerv(GL_MAX_COLOR_ATTACHMENTS, tmp)
        self.max_color_attachments = tmp.value

        glGetIntegerv(GL_MAX_TEXTURE_IMAGE_UNITS, tmp)
        self.max_texture_units = tmp.value

        self.default_texture_unit = GL_TEXTURE0 + self.max_texture_units - 1

        glGetIntegerv(GL_MAX_TEXTURE_MAX_ANISOTROPY, tmp)
        self.max_anisotropy = tmp.value

        # glGetIntegerv(GL_DRAW_FRAMEBUFFER_BINDING, tmp)
        # self.bound_frame_buffer = tmp.value
        self.project_view = project_matrix(60, 1.5, 0.1, 100)
        self.camera_view = camera_matrix(1, 1, 1, 0, 0, 0, 1, 0, 0)
        from ..graphic.program import load_all_program
        load_all_program()

    def gl_init(self):  # gl 初始化，参数获取。
        pass

    def gl_clear(self):
        pass

    def gl_render(self, interval):
        pass


window_input = WindowInput()
gl_context = OpenGLContext()


QUEUE_LENGTH = 27


class WindowPrototype(object):
    def __repr__(self):
        return self.__class__.__name__

    def __init__(self):
        self.window_title = 'Gu'
        self.window_image = None
        self.window_size = [800, 600]

        self.window_running = False
        self.window_clock = 0
        self.window_interval = 0
        self.window_queue = queue.Queue()

    def _window_sleep(self):
        """ 沉睡一段时间，控制帧数。 """
        current_clock = time.perf_counter()  # 当前时间
        frame_clock = current_clock - self.window_clock  # 上一帧实际经历的时间
        sleep_clock = self.window_interval - frame_clock  # 需要沉睡的时间
        if sleep_clock > 0:  # 判断是否掉帧了
            time.sleep(sleep_clock)  # 没有掉帧就沉睡
        current_clock = time.perf_counter()  # 再次计算当前时间
        interval_clock = current_clock - self.window_clock  # 本次跨越的帧数
        self.window_clock = current_clock  # 记录
        return interval_clock  # 返回间隔时间

    def _window_pull(self):
        size = self.window_queue.qsize()
        if size:
            size = size > QUEUE_LENGTH and QUEUE_LENGTH or size
            while size:
                size -= 1
                cmd = self.window_queue.get_nowait()
                try:
                    cmd and cmd[0](*cmd[1:])
                except Exception as e:
                    print_exception(e)

    def __call__(self, **kwargs):
        mask = 0
        if 'title' in kwargs:
            self.window_title = kwargs['title']
            mask |= 0b1
        if 'image' in kwargs:
            self.window_image = kwargs['image']
            mask |= 0b10
        if 'width' in kwargs:
            self.window_size[0] = kwargs['width']
            mask |= 0b100
        if 'height' in kwargs:
            self.window_size[1] = kwargs['height']
            mask |= 0b100

        if 'fps' in kwargs:
            self.window_interval = 1 / (kwargs['fps'] + 1)

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


__all__ = ['window_input', 'gl_context', 'WindowPrototype']
