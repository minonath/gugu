class WindowPrototype(object):
    def __init__(self, title, size, fps):
        self.window_title = title
        self.window_size = size
        self.mouse_x = 0
        self.mouse_y = 0
        self.window_interval = 1 / (fps + 1)  # 毕竟是小数计算，这个值有点偏差

    # 设置
    def window_set_title(self, title):
        pass

    def window_set_interval(self, interval):
        pass

    def window_set_image(self, image):
        pass

    def window_resize(self, width, height):
        pass

    # 启动
    def window_stop(self):  # 关闭窗口
        pass

    def window_start(self):  # 启动窗口
        pass

    # OpenGL
    def window_gl_init(self):  # 用于继承的 gl 初始化
        pass

    def window_gl_clear(self):  # 用于继承的 gl 清空
        pass

    def window_gl_render(self, interval):  # 用于继承的 gl 渲染
        pass

    # 鼠标
    def mouse_enter(self, mouse_x, mouse_y):  # 对应鼠标进入窗口事件
        pass  # 可以设置鼠标是否隐藏

    def mouse_exit(self, mouse_x, mouse_y):  # 对应鼠标离开窗口事件
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

    def mouse_right_down(self, mouse_x, mouse_y):
        pass

    def mouse_right_dragged(self, mouse_x, mouse_y):
        pass

    def mouse_right_up(self, mouse_x, mouse_y):
        pass

    def mouse_other_down(self, mouse_x, mouse_y):
        pass

    def mouse_other_dragged(self, mouse_x, mouse_y):
        pass

    def mouse_other_up(self, mouse_x, mouse_y):
        pass

    def key_down(self):
        pass

    def key_up(self):
        pass

    def flags_changed(self):
        pass
