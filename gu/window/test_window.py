from gu.window import Window
from gu.geometry import *
from gu.graphic.program import *

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

meow_pass = (
        Matrix4.from_perspective(60.0, 4 / 3, 0.1, 1000.0) *
        Matrix4.from_look_at(
            (10.0, 10.0, 10.0), (0.0, 0.0, 0.0), (0.0, 1.0, 0.0)
        )
    )


class Meow(Window):
    def __init__(self):
        Window.__init__(self)
        self.color_program = None
        self.instance_program = None
        self.color_vao = None
        self.instance_vao = None

    def window_gl_init(self):
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LESS)
        self.color_program = Program(*_color_shader)
        self.color_program(projection=meow_pass)

        _a0 = Buffer(axis_triangle, 'GL_FLOAT', 'GL_ARRAY_BUFFER',
                     'GL_STATIC_DRAW', 6)

        _a1 = Buffer(axis_index, 'GL_UNSIGNED_BYTE',
                     'GL_ELEMENT_ARRAY_BUFFER', 'GL_STATIC_DRAW')

        self.color_vao = VertexArray(
            self.color_program,
            'GL_TRIANGLES',
            (_a0, ('aPos', 'aCol'), 0),
            index=_a1
        )

    def window_gl_clear(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    def window_gl_render(self, interval):
        self.color_program()
        self.color_vao()


def test():
    Meow().window_start()
