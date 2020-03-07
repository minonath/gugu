from .auto_wrap import *

GL_VERSION_3_1 = 1
GL_SAMPLER_2D_RECT = 0x8B63
GL_SAMPLER_2D_RECT_SHADOW = 0x8B64
GL_SAMPLER_BUFFER = 0x8DC2
GL_INT_SAMPLER_2D_RECT = 0x8DCD
GL_INT_SAMPLER_BUFFER = 0x8DD0
GL_UNSIGNED_INT_SAMPLER_2D_RECT = 0x8DD5
GL_UNSIGNED_INT_SAMPLER_BUFFER = 0x8DD8
GL_TEXTURE_BUFFER = 0x8C2A
GL_MAX_TEXTURE_BUFFER_SIZE = 0x8C2B
GL_TEXTURE_BINDING_BUFFER = 0x8C2C
GL_TEXTURE_BUFFER_DATA_STORE_BINDING = 0x8C2D
GL_TEXTURE_RECTANGLE = 0x84F5
GL_TEXTURE_BINDING_RECTANGLE = 0x84F6
GL_PROXY_TEXTURE_RECTANGLE = 0x84F7
GL_MAX_RECTANGLE_TEXTURE_SIZE = 0x84F8
GL_R8_SNORM = 0x8F94
GL_RG8_SNORM = 0x8F95
GL_RGB8_SNORM = 0x8F96
GL_RGBA8_SNORM = 0x8F97
GL_R16_SNORM = 0x8F98
GL_RG16_SNORM = 0x8F99
GL_RGB16_SNORM = 0x8F9A
GL_RGBA16_SNORM = 0x8F9B
GL_SIGNED_NORMALIZED = 0x8F9C
GL_PRIMITIVE_RESTART = 0x8F9D
GL_PRIMITIVE_RESTART_INDEX = 0x8F9E
GL_COPY_READ_BUFFER = 0x8F36
GL_COPY_WRITE_BUFFER = 0x8F37
GL_UNIFORM_BUFFER = 0x8A11
GL_UNIFORM_BUFFER_BINDING = 0x8A28
GL_UNIFORM_BUFFER_START = 0x8A29
GL_UNIFORM_BUFFER_SIZE = 0x8A2A
GL_MAX_VERTEX_UNIFORM_BLOCKS = 0x8A2B
GL_MAX_GEOMETRY_UNIFORM_BLOCKS = 0x8A2C
GL_MAX_FRAGMENT_UNIFORM_BLOCKS = 0x8A2D
GL_MAX_COMBINED_UNIFORM_BLOCKS = 0x8A2E
GL_MAX_UNIFORM_BUFFER_BINDINGS = 0x8A2F
GL_MAX_UNIFORM_BLOCK_SIZE = 0x8A30
GL_MAX_COMBINED_VERTEX_UNIFORM_COMPONENTS = 0x8A31
GL_MAX_COMBINED_GEOMETRY_UNIFORM_COMPONENTS = 0x8A32
GL_MAX_COMBINED_FRAGMENT_UNIFORM_COMPONENTS = 0x8A33
GL_UNIFORM_BUFFER_OFFSET_ALIGNMENT = 0x8A34
GL_ACTIVE_UNIFORM_BLOCK_MAX_NAME_LENGTH = 0x8A35
GL_ACTIVE_UNIFORM_BLOCKS = 0x8A36
GL_UNIFORM_TYPE = 0x8A37
GL_UNIFORM_SIZE = 0x8A38
GL_UNIFORM_NAME_LENGTH = 0x8A39
GL_UNIFORM_BLOCK_INDEX = 0x8A3A
GL_UNIFORM_OFFSET = 0x8A3B
GL_UNIFORM_ARRAY_STRIDE = 0x8A3C
GL_UNIFORM_MATRIX_STRIDE = 0x8A3D
GL_UNIFORM_IS_ROW_MAJOR = 0x8A3E
GL_UNIFORM_BLOCK_BINDING = 0x8A3F
GL_UNIFORM_BLOCK_DATA_SIZE = 0x8A40
GL_UNIFORM_BLOCK_NAME_LENGTH = 0x8A41
GL_UNIFORM_BLOCK_ACTIVE_UNIFORMS = 0x8A42
GL_UNIFORM_BLOCK_ACTIVE_UNIFORM_INDICES = 0x8A43
GL_UNIFORM_BLOCK_REFERENCED_BY_VERTEX_SHADER = 0x8A44
GL_UNIFORM_BLOCK_REFERENCED_BY_GEOMETRY_SHADER = 0x8A45
GL_UNIFORM_BLOCK_REFERENCED_BY_FRAGMENT_SHADER = 0x8A46
GL_INVALID_INDEX = 0xFFFFFFFF
PFNGLDRAWARRAYSINSTANCEDPROC = C(None, UInt, Int, Int, Int)
PFNGLDRAWELEMENTSINSTANCEDPROC = C(None, UInt, Int, UInt, VoidP, Int)
PFNGLTEXBUFFERPROC = C(None, UInt, UInt, UInt)
PFNGLPRIMITIVERESTARTINDEXPROC = C(None, UInt)
PFNGLCOPYBUFFERSUBDATAPROC = C(None, UInt, UInt, Size, Size, Size)
PFNGLGETUNIFORMINDICESPROC = C(None, UInt, Int, P(CharP), P(UInt))
PFNGLGETACTIVEUNIFORMSIVPROC = C(None, UInt, Int, P(UInt), UInt, P(Int))
PFNGLGETACTIVEUNIFORMNAMEPROC = C(None, UInt, UInt, Int, P(Int), CharP)
PFNGLGETUNIFORMBLOCKINDEXPROC = C(UInt, UInt, CharP)
PFNGLGETACTIVEUNIFORMBLOCKIVPROC = C(None, UInt, UInt, UInt, P(Int))
PFNGLGETACTIVEUNIFORMBLOCKNAMEPROC = C(None, UInt, UInt, Int, P(Int), CharP)
PFNGLUNIFORMBLOCKBINDINGPROC = C(None, UInt, UInt, UInt)
glDrawArraysInstanced = E('glDrawArraysInstanced', None, UInt, Int, Int, Int)
glDrawElementsInstanced = E(
    'glDrawElementsInstanced', None, UInt, Int, UInt, VoidP, Int)
glTexBuffer = E('glTexBuffer', None, UInt, UInt, UInt)
glPrimitiveRestartIndex = E('glPrimitiveRestartIndex', None, UInt)
glCopyBufferSubData = E(
    'glCopyBufferSubData', None, UInt, UInt, Size, Size, Size)
glGetUniformIndices = E(
    'glGetUniformIndices', None, UInt, Int, P(CharP), P(UInt))
glGetActiveUniformsiv = E(
    'glGetActiveUniformsiv', None, UInt, Int, P(UInt), UInt, P(Int))
glGetActiveUniformName = E(
    'glGetActiveUniformName', None, UInt, UInt, Int, P(Int), CharP)
glGetUniformBlockIndex = E('glGetUniformBlockIndex', UInt, UInt, CharP)
glGetActiveUniformBlockiv = E(
    'glGetActiveUniformBlockiv', None, UInt, UInt, UInt, P(Int))
glGetActiveUniformBlockName = E(
    'glGetActiveUniformBlockName', None, UInt, UInt, Int, P(Int), CharP)
glUniformBlockBinding = E('glUniformBlockBinding', None, UInt, UInt, UInt)

__all__ = [
    'GL_VERSION_3_1', 'GL_SAMPLER_2D_RECT', 'GL_SAMPLER_2D_RECT_SHADOW',
    'GL_SAMPLER_BUFFER', 'GL_INT_SAMPLER_2D_RECT', 'GL_INT_SAMPLER_BUFFER',
    'GL_UNSIGNED_INT_SAMPLER_2D_RECT', 'GL_UNSIGNED_INT_SAMPLER_BUFFER',
    'GL_TEXTURE_BUFFER', 'GL_MAX_TEXTURE_BUFFER_SIZE',
    'GL_TEXTURE_BINDING_BUFFER', 'GL_TEXTURE_BUFFER_DATA_STORE_BINDING',
    'GL_TEXTURE_RECTANGLE', 'GL_TEXTURE_BINDING_RECTANGLE',
    'GL_PROXY_TEXTURE_RECTANGLE', 'GL_MAX_RECTANGLE_TEXTURE_SIZE',
    'GL_R8_SNORM', 'GL_RG8_SNORM', 'GL_RGB8_SNORM', 'GL_RGBA8_SNORM',
    'GL_R16_SNORM', 'GL_RG16_SNORM', 'GL_RGB16_SNORM', 'GL_RGBA16_SNORM',
    'GL_SIGNED_NORMALIZED', 'GL_PRIMITIVE_RESTART',
    'GL_PRIMITIVE_RESTART_INDEX', 'GL_COPY_READ_BUFFER',
    'GL_COPY_WRITE_BUFFER', 'GL_UNIFORM_BUFFER', 'GL_UNIFORM_BUFFER_BINDING',
    'GL_UNIFORM_BUFFER_START', 'GL_UNIFORM_BUFFER_SIZE',
    'GL_MAX_VERTEX_UNIFORM_BLOCKS', 'GL_MAX_GEOMETRY_UNIFORM_BLOCKS',
    'GL_MAX_FRAGMENT_UNIFORM_BLOCKS', 'GL_MAX_COMBINED_UNIFORM_BLOCKS',
    'GL_MAX_UNIFORM_BUFFER_BINDINGS', 'GL_MAX_UNIFORM_BLOCK_SIZE',
    'GL_MAX_COMBINED_VERTEX_UNIFORM_COMPONENTS',
    'GL_MAX_COMBINED_GEOMETRY_UNIFORM_COMPONENTS',
    'GL_MAX_COMBINED_FRAGMENT_UNIFORM_COMPONENTS',
    'GL_UNIFORM_BUFFER_OFFSET_ALIGNMENT',
    'GL_ACTIVE_UNIFORM_BLOCK_MAX_NAME_LENGTH', 'GL_ACTIVE_UNIFORM_BLOCKS',
    'GL_UNIFORM_TYPE', 'GL_UNIFORM_SIZE', 'GL_UNIFORM_NAME_LENGTH',
    'GL_UNIFORM_BLOCK_INDEX', 'GL_UNIFORM_OFFSET', 'GL_UNIFORM_ARRAY_STRIDE',
    'GL_UNIFORM_MATRIX_STRIDE', 'GL_UNIFORM_IS_ROW_MAJOR',
    'GL_UNIFORM_BLOCK_BINDING', 'GL_UNIFORM_BLOCK_DATA_SIZE',
    'GL_UNIFORM_BLOCK_NAME_LENGTH', 'GL_UNIFORM_BLOCK_ACTIVE_UNIFORMS',
    'GL_UNIFORM_BLOCK_ACTIVE_UNIFORM_INDICES',
    'GL_UNIFORM_BLOCK_REFERENCED_BY_VERTEX_SHADER',
    'GL_UNIFORM_BLOCK_REFERENCED_BY_GEOMETRY_SHADER',
    'GL_UNIFORM_BLOCK_REFERENCED_BY_FRAGMENT_SHADER', 'GL_INVALID_INDEX',
    'PFNGLDRAWARRAYSINSTANCEDPROC', 'PFNGLDRAWELEMENTSINSTANCEDPROC',
    'PFNGLTEXBUFFERPROC', 'PFNGLPRIMITIVERESTARTINDEXPROC',
    'PFNGLCOPYBUFFERSUBDATAPROC', 'PFNGLGETUNIFORMINDICESPROC',
    'PFNGLGETACTIVEUNIFORMSIVPROC', 'PFNGLGETACTIVEUNIFORMNAMEPROC',
    'PFNGLGETUNIFORMBLOCKINDEXPROC', 'PFNGLGETACTIVEUNIFORMBLOCKIVPROC',
    'PFNGLGETACTIVEUNIFORMBLOCKNAMEPROC', 'PFNGLUNIFORMBLOCKBINDINGPROC',
    'glDrawArraysInstanced', 'glDrawElementsInstanced', 'glTexBuffer',
    'glPrimitiveRestartIndex', 'glCopyBufferSubData', 'glGetUniformIndices',
    'glGetActiveUniformsiv', 'glGetActiveUniformName',
    'glGetUniformBlockIndex', 'glGetActiveUniformBlockiv',
    'glGetActiveUniformBlockName', 'glUniformBlockBinding'
]
