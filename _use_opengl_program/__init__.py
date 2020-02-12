import random

from _how_to_create_a_window._gu_util import gu
from _how_to_create_a_window._objc_library import OBJC, STR, BIND
from _how_to_create_a_window._objc_runtime import object_getClass
from _how_to_create_a_window._objc_constants import *
from _how_to_create_a_window._objc_window import _attach, _create_context, \
    _create_delegate, _create_menu, _create_view, _create_window, _KEY_MAP, \
    _ignore_error, _key_enum

# 这里我找了一些有用的函数绑定
from ._gl_wrap import *

# 这是一个泛用的 ctypes.Array 模块
from ._math_array import Array, Matrix4

# 这是 Buffer
from _use_opengl_program._gl_buffer import Buffer

# 在这里创建 Program 和 VAO
from ._gl_program import Program, VertexArray

_color_shader = """#version 330 core

in vec3 aPos;
in vec3 aCol;

uniform mat4 projection;

out vec4 vertexColor;

void main()
{
    gl_Position = projection * vec4(aPos, 1.0);
    vertexColor = vec4(aCol, 1.0);
}

""", """#version 330 core
out vec4 FragColor;

in vec4 vertexColor;

void main()
{
    FragColor = vertexColor;
}

"""

_instance_shader = """#version 330 core

in vec3 aPos;
in vec3 aCol;
in vec3 offset;

uniform mat4 projection;

out vec4 vertexColor;

void main()
{
    gl_Position = projection * vec4(aPos + offset, 1.0);
    vertexColor = vec4(aCol, 1.0);
}

""", """#version 330 core
out vec4 FragColor;

in vec4 vertexColor;

void main()
{
    FragColor = vertexColor;
}

"""

axis_triangle = (
    -0.1, 0.0, 0.0, 0.5, 0.5, 0.5,
    0.0, -0.1, 0.0, 0.5, 0.5, 0.5,
    0.0, 0.0, -0.1, 0.5, 0.5, 0.5,
    10.0, 0.0, 0.0, 0.5, 1.0, 1.0,  # x 轴绿色
    0.0, 10.0, 0.0, 1.0, 0.5, 1.0,  # y 轴红色
    0.0, 0.0, 10.0, 1.0, 1.0, 0.5,  # z 轴黄色
    0.03, 0.03, 0.03, 0.125, 0.125, 0.125
)
axis_index = (0, 1, 2, 0, 1, 5, 0, 2, 4, 1, 2, 3,
              0, 5, 6, 1, 5, 6, 0, 4, 6, 2, 4, 6,
              1, 3, 6, 2, 3, 6)

random_triangle = tuple(random.random() for _ in range(9))
random_color = tuple((random.random() / 2 + 0.5) for _ in range(9))
instance_offset = tuple(random.random() * 5 for _ in range(60))

meow_pass = Matrix4(
    *Matrix4.matrix_multiply(
        Matrix4.matrix_perspective(60.0, 4 / 3, 0.1, 1000.0),
        Matrix4.matrix_look_at(
            (10.0, 10.0, 10.0), (0.0, 0.0, 0.0), (0.0, 1.0, 0.0)
        ),
    )
)

nya_pass = Matrix4(*meow_pass)


def null_function(*args, **kwargs):
    pass


class TestWindow(object):
    def __init__(self):
        self._press_map = dict((k, null_function) for k in _KEY_MAP.keys())
        self.color_program = None
        self.instance_program = None
        self.color_vao = None
        self.instance_vao = None

    def gl_init(self):
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LESS)
        self.color_program = Program(*_color_shader)
        self.color_program(projection=meow_pass)

        _a0 = Buffer(axis_triangle, GL_FLOAT, GL_ARRAY_BUFFER,
                     GL_STATIC_DRAW, 6)

        _a1 = Buffer(axis_index, GL_UNSIGNED_BYTE, GL_ELEMENT_ARRAY_BUFFER,
                     GL_STATIC_DRAW)

        self.color_vao = VertexArray(
            self.color_program,
            GL_TRIANGLES,
            (_a0, ('aPos', 'aCol'), 0),
            index=_a1
        )

        self.instance_program = Program(*_instance_shader)
        self.instance_program(projection=nya_pass)

        _b0 = Buffer(random_triangle, GL_FLOAT, GL_ARRAY_BUFFER,
                     GL_STATIC_DRAW, 3)

        _b1 = Buffer(random_color, GL_FLOAT, GL_ARRAY_BUFFER,
                     GL_STATIC_DRAW, 3)

        _b2 = Buffer(instance_offset, GL_FLOAT, GL_ARRAY_BUFFER,
                     GL_STATIC_DRAW, 3)

        self.instance_vao = VertexArray(
            self.instance_program, GL_TRIANGLES,
            ((_b0, _b1), ('aPos', 'aCol'), 0),
            (_b2, 'offset', 1)
        )

        print(self.color_vao)
        print(self.instance_vao)

        # 测试一下 Buffer

        b = Buffer(16, GL_UNSIGNED_BYTE, GL_ELEMENT_ARRAY_BUFFER,
                   GL_DYNAMIC_DRAW)
        print(b)
        m = Matrix4(1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6,
                    array_type=ctypes.c_ubyte)
        b.buffer_write(m)
        print(b.buffer_read())
        b.buffer_clear(chunk=Array(0, 9, array_length=2,
                                   array_type=ctypes.c_ubyte))
        print(b.buffer_read())

    def gl_clear(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    def gl_render(self):
        # meow_pass(*Matrix4.matrix_multiply(
        #     meow_pass, left_rotate
        # ))
        # self.color_program(projection=meow_pass)
        self.color_program()
        self.color_vao()
        self.instance_program()
        self.instance_vao()

    def key_down(self, key_code):
        m = self._press_map[key_code]
        if isinstance(m, str):
            print('press', m)
        else:
            m()

    def key_up(self, key_code):
        pass

    def window_bind_press_function(self, name):
        key_code = _key_enum['kVK_ANSI_' + name]

        def wrap(function):
            self._press_map[key_code] = function
            return function

        return wrap


test_window = TestWindow()


# 我需要设计一个好点的按键接收器
@test_window.window_bind_press_function('A')
def up():
    meow_pass[12] -= 0.1
    nya_pass[12] -= 0.1
    test_window.color_program(projection=meow_pass)
    test_window.instance_program(projection=nya_pass)


@test_window.window_bind_press_function('S')
def down():
    meow_pass[13] -= 0.1
    nya_pass[13] -= 0.1
    test_window.color_program(projection=meow_pass)
    test_window.instance_program(projection=nya_pass)


@test_window.window_bind_press_function('D')
def right():
    meow_pass[12] += 0.1
    nya_pass[12] += 0.1
    test_window.color_program(projection=meow_pass)
    test_window.instance_program(projection=nya_pass)


@test_window.window_bind_press_function('W')
def top():
    meow_pass[13] += 0.1
    nya_pass[13] += 0.1
    test_window.color_program(projection=meow_pass)
    test_window.instance_program(projection=nya_pass)


left_rotate = Matrix4.matrix_rotation_y(1)
right_rotate = Matrix4.matrix_rotation_y(-1)


@test_window.window_bind_press_function('E')
def rotate_right():
    meow_pass(*Matrix4.matrix_multiply(
        meow_pass, right_rotate
    ))
    nya_pass(*Matrix4.matrix_multiply(
        nya_pass, right_rotate
    ))
    test_window.color_program(projection=meow_pass)
    test_window.instance_program(projection=nya_pass)


@test_window.window_bind_press_function('Q')
def rotate_left():
    meow_pass(*Matrix4.matrix_multiply(
        meow_pass, left_rotate
    ))
    nya_pass(*Matrix4.matrix_multiply(
        nya_pass, left_rotate
    ))
    test_window.color_program(projection=meow_pass)
    test_window.instance_program(projection=nya_pass)


def create_mac_window(gl_obj=test_window):
    pool = OBJC(OBJC('NSAutoreleasePool', 'alloc'), 'init')
    app = OBJC('NSApplication', 'sharedApplication')

    if not OBJC(app, 'isRunning'):
        _ignore_error()
        _create_menu(app)
        context = _create_context()
        window, area = _create_window((0, 0, 800, 600))
        view, tracking_area, = _create_view(area)

        # 这里做鼠标的绑定
        _bind_mouse_action(window, view)

        delegate = _create_delegate()
        OBJC(window, 'setDelegate:', delegate)

        _attach(window, view, context)

        OBJC(window, 'setTitle:', STR('Gu'))

        OBJC(app, 'finishLaunching')
        OBJC(app, 'activateIgnoringOtherApps:', True)
        OBJC(context, 'makeCurrentContext')
        gl_obj.context = context
        gl_obj.gl_init()
        while gu.meow:
            while True:
                OBJC(context, 'makeCurrentContext')
                gl_obj.gl_clear()
                gl_obj.gl_render()
                OBJC(context, 'flushBuffer')
                event = OBJC(
                    app, 'nextEventMatchingMask:untilDate:inMode:de''queue:',
                    NSAnyEventMask, OBJC('NSDate', 'distantPast'),
                    NSDefaultRunLoopMode, True)
                if not event:
                    break

                event_type = OBJC(event, 'type')
                OBJC(app, 'sendEvent:', event)

                if event_type == NSKeyDown:  # not OBJC(event, 'isARepeat'):
                    gl_obj.key_down(OBJC(event, 'keyCode'))
                elif event_type == NSKeyUp:
                    gl_obj.key_up(OBJC(event, 'keyCode'))
                elif event_type == NSFlagsChanged:
                    _flags = {1 << 1: 'LeftShift',
                              1 << 2: 'RightShift',
                              1 << 0: 'LeftControl',
                              1 << 13: 'RightControl',
                              1 << 5: 'LeftAlt',
                              1 << 6: 'RightAlt',
                              1 << 3: 'LeftCommand',
                              1 << 4: 'RightCommand'}
                    for k, v in _flags.items():
                        if OBJC(event, 'modifierFlags') & k:
                            print(v)

            OBJC(app, 'updateWindows')

    OBJC(pool, 'drain')


def _bind_mouse_action(window, view):
    win_class = object_getClass(window)
    view_class = object_getClass(view)

    @BIND(win_class, 'canBecomeKeyWindow', 'B16@0:8')
    def call(cls, sel):
        return True

    # @BIND(view_class, 'mouseMoved:', 'v24@0:8@16')
    # def call(cls, sel, notification):
    #     in_window = OBJC(notification, 'locationInWindow')
    #     dx, dy = in_window.mem_0, in_window.mem_1
    #     print('mouseMoved', dx, dy)

    @BIND(view_class, 'mouseDown:', 'v24@0:8@16')
    def call(cls, sel, notification):
        in_window = OBJC(notification, 'locationInWindow')
        dx, dy = in_window.mem_0, in_window.mem_1
        test_window.dx, test_window.dy = dx, dy
        print('mouseDown', dx, dy)

    @BIND(view_class, 'mouseDragged:', 'v24@0:8@16')
    def call(cls, sel, notification):
        # 这里有个奇怪的问题，就是 mac 触控板有时候不反应这个事件，但是鼠标还是正常的。
        # 在多次拖拽后，就会产生这个问题，即是用鼠标后还是不会反应回来，
        # 经过测试，是消息通道卡住了，触控版的消息队列比鼠标少一些，太多事件会导致阻塞。
        # 需要加快这个消息的处理才行。之后用异步操作来解决。

        in_window = OBJC(notification, 'locationInWindow')
        dx, dy = in_window.mem_0, in_window.mem_1
        ddx = dx - test_window.dx
        ddy = dy - test_window.dy
        test_window.dx, test_window.dy = dx, dy
        # print('mouseDragged', ddx, ddy)
        m = Matrix4.matrix_rotation_y(-ddx)
        meow_pass(*Matrix4.matrix_multiply(meow_pass, m))
        nya_pass(*Matrix4.matrix_multiply(nya_pass, m))
        test_window.color_program(projection=meow_pass)
        test_window.instance_program(projection=nya_pass)
        print(meow_pass)

    @BIND(view_class, 'mouseUp:', 'v24@0:8@16')
    def call(cls, sel, notification):
        in_window = OBJC(notification, 'locationInWindow')
        dx, dy = in_window.mem_0, in_window.mem_1

    @BIND(view_class, 'rightMouseDown:', 'v24@0:8@16')
    def call(cls, sel, notification):
        in_window = OBJC(notification, 'locationInWindow')
        dx, dy = in_window.mem_0, in_window.mem_1
        print('rightMouseDown', dx, dy)

    @BIND(view_class, 'rightMouseDragged:', 'v24@0:8@16')
    def call(cls, sel, notification):
        in_window = OBJC(notification, 'locationInWindow')
        dx, dy = in_window.mem_0, in_window.mem_1
        print('rightMouseDragged', dx, dy)

    @BIND(view_class, 'rightMouseUp:', 'v24@0:8@16')
    def call(cls, sel, notification):
        in_window = OBJC(notification, 'locationInWindow')
        dx, dy = in_window.mem_0, in_window.mem_1
        print('rightMouseUp', dx, dy)

    @BIND(view_class, 'otherMouseDown:', 'v24@0:8@16')
    def call(cls, sel, notification):
        in_window = OBJC(notification, 'locationInWindow')
        dx, dy = in_window.mem_0, in_window.mem_1
        print('otherMouseDown', dx, dy)

    @BIND(view_class, 'otherMouseDragged:', 'v24@0:8@16')
    def call(cls, sel, notification):
        in_window = OBJC(notification, 'locationInWindow')
        dx, dy = in_window.mem_0, in_window.mem_1
        print('otherMouseDragged', dx, dy)

    @BIND(view_class, 'otherMouseUp:', 'v24@0:8@16')
    def call(cls, sel, notification):
        in_window = OBJC(notification, 'locationInWindow')
        dx, dy = in_window.mem_0, in_window.mem_1
        print('otherMouseUp', dx, dy)

    @BIND(view_class, 'mouseEntered:', 'v24@0:8@16')
    def call(cls, sel, notification):
        print('mouseEntered')

    @BIND(view_class, 'mouseExited:', 'v24@0:8@16')
    def call(cls, sel, notification):
        print('mouseExited')
