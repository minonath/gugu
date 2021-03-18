import ctypes
import io

from gu.opengl import context, Program, VertexArray, Rule
from gu.opengl.library import *
from gu.matrix import Floats, Matrix4, Vector3
from gu.system import resource, gu
from gu.sprite.png_library import read_png

gu.window(title='Point Sprite', width=400, height=300)

glClearColor(0.5, 0.5, 0.5, 1.0)

width, height, mode, data = read_png(io.BytesIO(resource.get('03_test.png')))

sprite_texture = ctypes.c_uint()
glGenTextures(1, sprite_texture)
glActiveTexture(GL_TEXTURE0)
glBindTexture(GL_TEXTURE_2D, sprite_texture)
glTexParameteri(
    GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR
)
glTexParameteri(
    GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR
)

glPixelStorei(GL_PACK_ALIGNMENT, 1)
glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA8,
             width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, data)

VBO = ctypes.c_uint()
glGenBuffers(1, VBO)  # not glCreateBuffers
glBindBuffer(GL_ARRAY_BUFFER, VBO)
vertices = Floats(
    -.9, -.9, .85, -.9, -.9, .85, .9, -.85, .9, .9, -.85, .9, data_nums=12)
glBufferData(GL_ARRAY_BUFFER, vertices.size, vertices, GL_STATIC_DRAW)

VERTEX = """#version 410 core

uniform mat4 model;
uniform mat4 projection;

in vec4 vPosition;

void main() {
    gl_Position = projection * model * vPosition;
    gl_PointSize = 256.0;
}
"""
FRAGMENT = """#version 410 core

uniform sampler2D sprite1;

out vec4 fColor;

void main() {
    fColor = texture(sprite1, gl_PointCoord);
}
"""

PROGRAM = Program(GL_VERTEX_SHADER=VERTEX, GL_FRAGMENT_SHADER=FRAGMENT)
MODEL = glGetUniformLocation(PROGRAM, b"model")
PROJECTION = glGetUniformLocation(PROGRAM, b"projection")
SPRITE = glGetUniformLocation(PROGRAM, b"sprite1")
projection = Matrix4.from_perspective(120, 1.0, 0.1, 100.0)
model = Matrix4.from_look_at(
    Vector3(0, 2, 2), Vector3(0, 0, 0), Vector3(0, 0, 1)
)
glProgramUniformMatrix4fv(PROGRAM, PROJECTION, 1, GL_FALSE, projection)
glProgramUniformMatrix4fv(PROGRAM, MODEL, 1, GL_FALSE, model)
glProgramUniform1ui(PROGRAM, SPRITE, 1, sprite_texture)

glUseProgram(PROGRAM)

VAO = VertexArray(PROGRAM, Rule('vPosition', buffer=VBO, stride=2),)

glEnable(GL_PROGRAM_POINT_SIZE)
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)


def render(interval):
    glClear(GL_COLOR_BUFFER_BIT)
    glBindVertexArray(VAO)
    glDrawArrays(GL_POINTS, 0, 6)


context.render = render
