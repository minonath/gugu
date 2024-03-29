from .._types import *

GL_VERSION_4_4 = 1
GL_MAX_VERTEX_ATTRIB_STRIDE = 0x82E5
GL_PRIMITIVE_RESTART_FOR_PATCHES_SUPPORTED = 0x8221
GL_TEXTURE_BUFFER_BINDING = 0x8C2A
GL_MAP_PERSISTENT_BIT = 0x0040
GL_MAP_COHERENT_BIT = 0x0080
GL_DYNAMIC_STORAGE_BIT = 0x0100
GL_CLIENT_STORAGE_BIT = 0x0200
GL_CLIENT_MAPPED_BUFFER_BARRIER_BIT = 0x00004000
GL_BUFFER_IMMUTABLE_STORAGE = 0x821F
GL_BUFFER_STORAGE_FLAGS = 0x8220
GL_CLEAR_TEXTURE = 0x9365
GL_LOCATION_COMPONENT = 0x934A
GL_TRANSFORM_FEEDBACK_BUFFER_INDEX = 0x934B
GL_TRANSFORM_FEEDBACK_BUFFER_STRIDE = 0x934C
GL_QUERY_BUFFER = 0x9192
GL_QUERY_BUFFER_BARRIER_BIT = 0x00008000
GL_QUERY_BUFFER_BINDING = 0x9193
GL_QUERY_RESULT_NO_WAIT = 0x9194
GL_MIRROR_CLAMP_TO_EDGE = 0x8743
PFNGLBUFFERSTORAGEPROC = C(None, UInt, Size, VoidP, UInt)
PFNGLCLEARTEXIMAGEPROC = C(None, UInt, Int, UInt, UInt, VoidP)
PFNGLCLEARTEXSUBIMAGEPROC = C(
    None, UInt, Int, Int, Int, Int, Int, Int, Int, UInt, UInt, VoidP
)
PFNGLBINDBUFFERSBASEPROC = C(None, UInt, UInt, Int, P(UInt))
PFNGLBINDBUFFERSRANGEPROC = C(
    None, UInt, UInt, Int, P(UInt), P(Size), P(Size)
)
PFNGLBINDTEXTURESPROC = C(None, UInt, Int, P(UInt))
PFNGLBINDSAMPLERSPROC = C(None, UInt, Int, P(UInt))
PFNGLBINDIMAGETEXTURESPROC = C(None, UInt, Int, P(UInt))
PFNGLBINDVERTEXBUFFERSPROC = C(None, UInt, Int, P(UInt), P(Size), P(Int))
glBufferStorage = E('glBufferStorage', None, UInt, Size, VoidP, UInt)
glClearTexImage = E('glClearTexImage', None, UInt, Int, UInt, UInt, VoidP)
glClearTexSubImage = E(
    'glClearTexSubImage', None, UInt, Int, Int, Int, Int, Int, Int, Int, UInt,
    UInt, VoidP
)
glBindBuffersBase = E('glBindBuffersBase', None, UInt, UInt, Int, P(UInt))
glBindBuffersRange = E(
    'glBindBuffersRange', None, UInt, UInt, Int, P(UInt), P(Size), P(Size)
)
glBindTextures = E('glBindTextures', None, UInt, Int, P(UInt))
glBindSamplers = E('glBindSamplers', None, UInt, Int, P(UInt))
glBindImageTextures = E('glBindImageTextures', None, UInt, Int, P(UInt))
glBindVertexBuffers = E(
    'glBindVertexBuffers', None, UInt, Int, P(UInt), P(Size), P(Int)
)

__all__ = [
    'GL_VERSION_4_4', 'GL_MAX_VERTEX_ATTRIB_STRIDE',
    'GL_PRIMITIVE_RESTART_FOR_PATCHES_SUPPORTED', 'GL_TEXTURE_BUFFER_BINDING',
    'GL_MAP_PERSISTENT_BIT', 'GL_MAP_COHERENT_BIT', 'GL_DYNAMIC_STORAGE_BIT',
    'GL_CLIENT_STORAGE_BIT', 'GL_CLIENT_MAPPED_BUFFER_BARRIER_BIT',
    'GL_BUFFER_IMMUTABLE_STORAGE', 'GL_BUFFER_STORAGE_FLAGS',
    'GL_CLEAR_TEXTURE', 'GL_LOCATION_COMPONENT',
    'GL_TRANSFORM_FEEDBACK_BUFFER_INDEX',
    'GL_TRANSFORM_FEEDBACK_BUFFER_STRIDE', 'GL_QUERY_BUFFER',
    'GL_QUERY_BUFFER_BARRIER_BIT', 'GL_QUERY_BUFFER_BINDING',
    'GL_QUERY_RESULT_NO_WAIT', 'GL_MIRROR_CLAMP_TO_EDGE',
    'PFNGLBUFFERSTORAGEPROC', 'PFNGLCLEARTEXIMAGEPROC',
    'PFNGLCLEARTEXSUBIMAGEPROC', 'PFNGLBINDBUFFERSBASEPROC',
    'PFNGLBINDBUFFERSRANGEPROC', 'PFNGLBINDTEXTURESPROC',
    'PFNGLBINDSAMPLERSPROC', 'PFNGLBINDIMAGETEXTURESPROC',
    'PFNGLBINDVERTEXBUFFERSPROC', 'glBufferStorage', 'glClearTexImage',
    'glClearTexSubImage', 'glBindBuffersBase', 'glBindBuffersRange',
    'glBindTextures', 'glBindSamplers', 'glBindImageTextures',
    'glBindVertexBuffers'
]
