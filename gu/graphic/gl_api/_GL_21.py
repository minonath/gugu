from .auto_wrap import *

GL_VERSION_2_1 = 1
GL_PIXEL_PACK_BUFFER = 0x88EB
GL_PIXEL_UNPACK_BUFFER = 0x88EC
GL_PIXEL_PACK_BUFFER_BINDING = 0x88ED
GL_PIXEL_UNPACK_BUFFER_BINDING = 0x88EF
GL_FLOAT_MAT2x3 = 0x8B65
GL_FLOAT_MAT2x4 = 0x8B66
GL_FLOAT_MAT3x2 = 0x8B67
GL_FLOAT_MAT3x4 = 0x8B68
GL_FLOAT_MAT4x2 = 0x8B69
GL_FLOAT_MAT4x3 = 0x8B6A
GL_SRGB = 0x8C40
GL_SRGB8 = 0x8C41
GL_SRGB_ALPHA = 0x8C42
GL_SRGB8_ALPHA8 = 0x8C43
GL_COMPRESSED_SRGB = 0x8C48
GL_COMPRESSED_SRGB_ALPHA = 0x8C49
PFNGLUNIFORMMATRIX2X3FVPROC = C(None, Int, Int, UByte, P(Float))
PFNGLUNIFORMMATRIX3X2FVPROC = C(None, Int, Int, UByte, P(Float))
PFNGLUNIFORMMATRIX2X4FVPROC = C(None, Int, Int, UByte, P(Float))
PFNGLUNIFORMMATRIX4X2FVPROC = C(None, Int, Int, UByte, P(Float))
PFNGLUNIFORMMATRIX3X4FVPROC = C(None, Int, Int, UByte, P(Float))
PFNGLUNIFORMMATRIX4X3FVPROC = C(None, Int, Int, UByte, P(Float))
glUniformMatrix2x3fv = E('glUniformMatrix2x3fv', None, Int, Int, UByte,
                         P(Float))
glUniformMatrix3x2fv = E('glUniformMatrix3x2fv', None, Int, Int, UByte,
                         P(Float))
glUniformMatrix2x4fv = E('glUniformMatrix2x4fv', None, Int, Int, UByte,
                         P(Float))
glUniformMatrix4x2fv = E('glUniformMatrix4x2fv', None, Int, Int, UByte,
                         P(Float))
glUniformMatrix3x4fv = E('glUniformMatrix3x4fv', None, Int, Int, UByte,
                         P(Float))
glUniformMatrix4x3fv = E('glUniformMatrix4x3fv', None, Int, Int, UByte,
                         P(Float))

__all__ = [
    'GL_VERSION_2_1', 'GL_PIXEL_PACK_BUFFER', 'GL_PIXEL_UNPACK_BUFFER',
    'GL_PIXEL_PACK_BUFFER_BINDING', 'GL_PIXEL_UNPACK_BUFFER_BINDING',
    'GL_FLOAT_MAT2x3', 'GL_FLOAT_MAT2x4', 'GL_FLOAT_MAT3x2',
    'GL_FLOAT_MAT3x4', 'GL_FLOAT_MAT4x2', 'GL_FLOAT_MAT4x3', 'GL_SRGB',
    'GL_SRGB8', 'GL_SRGB_ALPHA', 'GL_SRGB8_ALPHA8', 'GL_COMPRESSED_SRGB',
    'GL_COMPRESSED_SRGB_ALPHA', 'PFNGLUNIFORMMATRIX2X3FVPROC',
    'PFNGLUNIFORMMATRIX3X2FVPROC', 'PFNGLUNIFORMMATRIX2X4FVPROC',
    'PFNGLUNIFORMMATRIX4X2FVPROC', 'PFNGLUNIFORMMATRIX3X4FVPROC',
    'PFNGLUNIFORMMATRIX4X3FVPROC', 'glUniformMatrix2x3fv',
    'glUniformMatrix3x2fv', 'glUniformMatrix2x4fv', 'glUniformMatrix4x2fv',
    'glUniformMatrix3x4fv', 'glUniformMatrix4x3fv'
]
