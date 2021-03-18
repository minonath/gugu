import ctypes

from gu.matrix import Floats
from gu.opengl import context, Program, VertexArray, Rule
from gu.opengl.library import *
from gu.window import input
from gu.system import key_map, key_name, gu

gu.window(title='Press M or Other', width=400, height=300)

VBO = ctypes.c_uint()
glGenBuffers(1, VBO)  # not glCreateBuffers
glBindBuffer(GL_ARRAY_BUFFER, VBO)
vertices = Floats(
    -.9, -.9, .85, -.9, -.9, .85, .9, -.85, .9, .9, -.85, .9, data_nums=12)
glBufferData(GL_ARRAY_BUFFER, vertices.size, vertices, GL_STATIC_DRAW)

VERTEX = """#version 410 core

layout(location=0) in vec4 vPosition;

void main() {
    gl_Position = vPosition;
}
"""
FRAGMENT = """#version 410 core

out vec4 fColor;

void main() {
    fColor = vec4(0.5, 0.4, 0.8, 1.0);
}
"""
PROGRAM = Program(GL_VERTEX_SHADER=VERTEX, GL_FRAGMENT_SHADER=FRAGMENT)
glUseProgram(PROGRAM)

VAO = VertexArray(PROGRAM, Rule('vPosition', buffer=VBO, stride=2))


def render(interval):
    glClear(GL_COLOR_BUFFER_BIT)
    glBindVertexArray(VAO)
    glDrawArrays(GL_TRIANGLES, 0, vertices.nums)
    glFlush()


MODE = GL_FILL


def key_press(key_code, shift_ctrl_alt):
    print(key_name[key_code])
    if key_code == key_map['M']:
        global MODE
        MODE = GL_LINE if MODE == GL_FILL else GL_FILL
        glPolygonMode(GL_FRONT_AND_BACK, MODE)


context.render = render
input.key_press = key_press
