from gu import gu
from gu.opengl import *
from gu.graphic.program import Program

GL_VERTEX_SHADER = '#version 410\n\nin vec3 in_position;\n' \
                   'in vec3 in_normal;\nin vec2 in_texcoord_0;\n\n' \
                   'uniform mat4 m_proj[2];\n// uniform mat4 m_model;\n' \
                   'uniform mat4 m_cam;\n\nout vec3 normal;\nout vec2 uv;\n' \
                   'out vec3 pos;\n\nvoid main() {\n' \
                   '    mat4 mv = m_cam * m_proj[1]; // m_model;\n' \
                   '    vec4 p = mv * vec4(in_position, 1.0);\n' \
                   '    gl_Position = m_proj[0] * p;\n' \
                   '    mat3 m_normal = transpose(inverse(mat3(mv)));\n' \
                   '    normal = m_normal * in_normal;\n' \
                   '    uv = in_texcoord_0;\n    pos = p.xyz;\n}\n'
GL_FRAGMENT_SHADER = '#version 330\n\nout vec4 fragColor;\n' \
                     'uniform sampler2D texture0;\n\nin vec3 normal;\n' \
                     'in vec3 pos;\nin vec2 uv;\n\nvoid main()\n{\n' \
                     '    float l = dot(normalize(-pos), normalize(normal));' \
                     '\n    vec4 color = texture(texture0, uv);\n' \
                     '    fragColor = color * 0.25 + color * 0.75 * abs(l);' \
                     '\n}\n\n'


def gl_init():
    print('我被初始化了')
    Program(name='meow', GL_VERTEX_SHADER=GL_VERTEX_SHADER, GL_FRAGMENT_SHADER=GL_FRAGMENT_SHADER)


def gl_clear():
    glClear(GL_COLOR_BUFFER_BIT)


def gl_render(interval):
    # print('meow',interval)
    pass


gu.context.gl_init = gl_init
gu.context.gl_clear = gl_clear
gu.context.gl_render = gl_render
