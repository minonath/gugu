from .object import OpenGLObject
from .texture import Texture

from ..opengl import *


class FrameBuffer(OpenGLObject):
    def __init__(self, color_attachments, depth_attachment):
        color_attachments_len = len(color_attachments)

        if color_attachments_len == 0 and not depth_attachment:
            raise OpenGLError('空的 FrameBuffer')

        for item in color_attachments:
            if isinstance(item, Texture):
                if item is color_attachments[0]:
                    width = item._texture_width
                    height = item._texture_height
                    samples = item._texture_samples
            else:
                pass

        OpenGLObject.__init__(self)

    def __repr__(self):
        return self.__string__

    def gl_initialize(self) -> str:
        pass

    def gl_release(self):
        pass
