from .auto_wrap import *

GL_VERSION_1_1 = 1
GL_COLOR_LOGIC_OP = 0x0BF2
GL_POLYGON_OFFSET_UNITS = 0x2A00
GL_POLYGON_OFFSET_POINT = 0x2A01
GL_POLYGON_OFFSET_LINE = 0x2A02
GL_POLYGON_OFFSET_FILL = 0x8037
GL_POLYGON_OFFSET_FACTOR = 0x8038
GL_TEXTURE_BINDING_1D = 0x8068
GL_TEXTURE_BINDING_2D = 0x8069
GL_TEXTURE_INTERNAL_FORMAT = 0x1003
GL_TEXTURE_RED_SIZE = 0x805C
GL_TEXTURE_GREEN_SIZE = 0x805D
GL_TEXTURE_BLUE_SIZE = 0x805E
GL_TEXTURE_ALPHA_SIZE = 0x805F
GL_DOUBLE = 0x140A
GL_PROXY_TEXTURE_1D = 0x8063
GL_PROXY_TEXTURE_2D = 0x8064
GL_R3_G3_B2 = 0x2A10
GL_RGB4 = 0x804F
GL_RGB5 = 0x8050
GL_RGB8 = 0x8051
GL_RGB10 = 0x8052
GL_RGB12 = 0x8053
GL_RGB16 = 0x8054
GL_RGBA2 = 0x8055
GL_RGBA4 = 0x8056
GL_RGB5_A1 = 0x8057
GL_RGBA8 = 0x8058
GL_RGB10_A2 = 0x8059
GL_RGBA12 = 0x805A
GL_RGBA16 = 0x805B
GL_VERTEX_ARRAY = 0x8074
PFNGLDRAWARRAYSPROC = C(None, UInt, Int, Int)
PFNGLDRAWELEMENTSPROC = C(None, UInt, Int, UInt, VoidP)
PFNGLGETPOINTERVPROC = C(None, UInt, P(VoidP))
PFNGLPOLYGONOFFSETPROC = C(None, Float, Float)
PFNGLCOPYTEXIMAGE1DPROC = C(None, UInt, Int, UInt, Int, Int, Int, Int)
PFNGLCOPYTEXIMAGE2DPROC = C(None, UInt, Int, UInt, Int, Int, Int, Int, Int)
PFNGLCOPYTEXSUBIMAGE1DPROC = C(None, UInt, Int, Int, Int, Int, Int)
PFNGLCOPYTEXSUBIMAGE2DPROC = C(None, UInt, Int, Int, Int, Int, Int, Int, Int)
PFNGLTEXSUBIMAGE1DPROC = C(None, UInt, Int, Int, Int, UInt, UInt, VoidP)
PFNGLTEXSUBIMAGE2DPROC = C(
    None, UInt, Int, Int, Int, Int, Int, UInt, UInt, VoidP)
PFNGLBINDTEXTUREPROC = C(None, UInt, UInt)
PFNGLDELETETEXTURESPROC = C(None, Int, P(UInt))
PFNGLGENTEXTURESPROC = C(None, Int, P(UInt))
PFNGLISTEXTUREPROC = C(UByte, UInt)
glDrawArrays = E('glDrawArrays', None, UInt, Int, Int)
glDrawElements = E('glDrawElements', None, UInt, Int, UInt, VoidP)
glGetPointerv = E('glGetPointerv', None, UInt, P(VoidP))
glPolygonOffset = E('glPolygonOffset', None, Float, Float)
glCopyTexImage1D = E(
    'glCopyTexImage1D', None, UInt, Int, UInt, Int, Int, Int, Int)
glCopyTexImage2D = E(
    'glCopyTexImage2D', None, UInt, Int, UInt, Int, Int, Int, Int, Int)
glCopyTexSubImage1D = E(
    'glCopyTexSubImage1D', None, UInt, Int, Int, Int, Int, Int)
glCopyTexSubImage2D = E(
    'glCopyTexSubImage2D', None, UInt, Int, Int, Int, Int, Int, Int, Int)
glTexSubImage1D = E(
    'glTexSubImage1D', None, UInt, Int, Int, Int, UInt, UInt, VoidP)
glTexSubImage2D = E(
    'glTexSubImage2D', None, UInt, Int, Int, Int, Int, Int, UInt, UInt, VoidP)
glBindTexture = E('glBindTexture', None, UInt, UInt)
glDeleteTextures = E('glDeleteTextures', None, Int, P(UInt))
glGenTextures = E('glGenTextures', None, Int, P(UInt))
glIsTexture = E('glIsTexture', UByte, UInt)

__all__ = [
    'GL_VERSION_1_1', 'GL_COLOR_LOGIC_OP', 'GL_POLYGON_OFFSET_UNITS',
    'GL_POLYGON_OFFSET_POINT', 'GL_POLYGON_OFFSET_LINE',
    'GL_POLYGON_OFFSET_FILL', 'GL_POLYGON_OFFSET_FACTOR',
    'GL_TEXTURE_BINDING_1D', 'GL_TEXTURE_BINDING_2D',
    'GL_TEXTURE_INTERNAL_FORMAT', 'GL_TEXTURE_RED_SIZE',
    'GL_TEXTURE_GREEN_SIZE', 'GL_TEXTURE_BLUE_SIZE', 'GL_TEXTURE_ALPHA_SIZE',
    'GL_DOUBLE', 'GL_PROXY_TEXTURE_1D', 'GL_PROXY_TEXTURE_2D', 'GL_R3_G3_B2',
    'GL_RGB4', 'GL_RGB5', 'GL_RGB8', 'GL_RGB10', 'GL_RGB12', 'GL_RGB16',
    'GL_RGBA2', 'GL_RGBA4', 'GL_RGB5_A1', 'GL_RGBA8', 'GL_RGB10_A2',
    'GL_RGBA12', 'GL_RGBA16', 'GL_VERTEX_ARRAY', 'PFNGLDRAWARRAYSPROC',
    'PFNGLDRAWELEMENTSPROC', 'PFNGLGETPOINTERVPROC', 'PFNGLPOLYGONOFFSETPROC',
    'PFNGLCOPYTEXIMAGE1DPROC', 'PFNGLCOPYTEXIMAGE2DPROC',
    'PFNGLCOPYTEXSUBIMAGE1DPROC', 'PFNGLCOPYTEXSUBIMAGE2DPROC',
    'PFNGLTEXSUBIMAGE1DPROC', 'PFNGLTEXSUBIMAGE2DPROC',
    'PFNGLBINDTEXTUREPROC', 'PFNGLDELETETEXTURESPROC', 'PFNGLGENTEXTURESPROC',
    'PFNGLISTEXTUREPROC', 'glDrawArrays', 'glDrawElements', 'glGetPointerv',
    'glPolygonOffset', 'glCopyTexImage1D', 'glCopyTexImage2D',
    'glCopyTexSubImage1D', 'glCopyTexSubImage2D', 'glTexSubImage1D',
    'glTexSubImage2D', 'glBindTexture', 'glDeleteTextures', 'glGenTextures',
    'glIsTexture'
]
