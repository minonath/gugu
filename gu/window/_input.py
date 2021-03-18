class _WindowInput(object):
    def __repr__(self):
        return 'Input'

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

    def key_press(self, key_code, shift_ctrl_alt):
        pass

    def key_release(self, key_code, shift_ctrl_alt):
        pass


input = _WindowInput()
