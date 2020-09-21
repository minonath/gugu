import ctypes

try:
    from ..opengl import *
except ModuleNotFoundError:
    from ..system import compile_gl_file  # 修复文件。
    compile_gl_file()
    from ..opengl import *


class _OpenGLContext(object):
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
        # self.project_view = project_matrix(60, 1.5, 0.1, 100)
        # self.camera_view = camera_matrix(1, 1, 1, 0, 0, 0, 1, 0, 0)
        # from ..graphic.program import load_all_program
        # load_all_program()

    def gl_render(self, interval):
        pass


gl_context = _OpenGLContext()

__all__ = ['gl_context']
