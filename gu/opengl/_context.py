import ctypes
from .library import *


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
        self.max_texture_size = 0
        self.default_texture_unit = 0
        self.max_anisotropy = 0
        self.bound_frame_buffer = 0

    def prepare(self):
        _tmp = ctypes.c_int()
        glGetIntegerv(GL_MAJOR_VERSION, _tmp)
        self.gl_version = _tmp.value * 100
        glGetIntegerv(GL_MINOR_VERSION, _tmp)
        self.gl_version += _tmp.value * 10

        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_DST_ALPHA)
        # glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        # glEnable(GL_TEXTURE_CUBE_MAP_SEAMLESS)

        glEnable(GL_PRIMITIVE_RESTART)
        glPrimitiveRestartIndex(-1)

        glGetIntegerv(GL_MAX_SAMPLES, _tmp)
        self.max_samples = _tmp.value

        glGetIntegerv(GL_MAX_INTEGER_SAMPLES, _tmp)
        self.max_integer_samples = _tmp.value

        glGetIntegerv(GL_MAX_COLOR_ATTACHMENTS, _tmp)
        self.max_color_attachments = _tmp.value

        glGetIntegerv(GL_MAX_TEXTURE_IMAGE_UNITS, _tmp)
        self.max_texture_units = _tmp.value

        self.default_texture_unit = GL_TEXTURE0 + self.max_texture_units - 1

        glGetIntegerv(GL_MAX_TEXTURE_SIZE, _tmp)
        self.max_texture_size = _tmp.value

        glGetIntegerv(GL_MAX_TEXTURE_MAX_ANISOTROPY, _tmp)
        self.max_anisotropy = _tmp.value

        glGetIntegerv(GL_DRAW_FRAMEBUFFER_BINDING, _tmp)
        self.bound_frame_buffer = _tmp.value

    def render(self, interval):
        pass


context = _OpenGLContext()
