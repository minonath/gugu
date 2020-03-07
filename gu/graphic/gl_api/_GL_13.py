from .auto_wrap import *

GL_VERSION_1_3 = 1
GL_TEXTURE0 = 0x84C0
GL_TEXTURE1 = 0x84C1
GL_TEXTURE2 = 0x84C2
GL_TEXTURE3 = 0x84C3
GL_TEXTURE4 = 0x84C4
GL_TEXTURE5 = 0x84C5
GL_TEXTURE6 = 0x84C6
GL_TEXTURE7 = 0x84C7
GL_TEXTURE8 = 0x84C8
GL_TEXTURE9 = 0x84C9
GL_TEXTURE10 = 0x84CA
GL_TEXTURE11 = 0x84CB
GL_TEXTURE12 = 0x84CC
GL_TEXTURE13 = 0x84CD
GL_TEXTURE14 = 0x84CE
GL_TEXTURE15 = 0x84CF
GL_TEXTURE16 = 0x84D0
GL_TEXTURE17 = 0x84D1
GL_TEXTURE18 = 0x84D2
GL_TEXTURE19 = 0x84D3
GL_TEXTURE20 = 0x84D4
GL_TEXTURE21 = 0x84D5
GL_TEXTURE22 = 0x84D6
GL_TEXTURE23 = 0x84D7
GL_TEXTURE24 = 0x84D8
GL_TEXTURE25 = 0x84D9
GL_TEXTURE26 = 0x84DA
GL_TEXTURE27 = 0x84DB
GL_TEXTURE28 = 0x84DC
GL_TEXTURE29 = 0x84DD
GL_TEXTURE30 = 0x84DE
GL_TEXTURE31 = 0x84DF
GL_ACTIVE_TEXTURE = 0x84E0
GL_MULTISAMPLE = 0x809D
GL_SAMPLE_ALPHA_TO_COVERAGE = 0x809E
GL_SAMPLE_ALPHA_TO_ONE = 0x809F
GL_SAMPLE_COVERAGE = 0x80A0
GL_SAMPLE_BUFFERS = 0x80A8
GL_SAMPLES = 0x80A9
GL_SAMPLE_COVERAGE_VALUE = 0x80AA
GL_SAMPLE_COVERAGE_INVERT = 0x80AB
GL_TEXTURE_CUBE_MAP = 0x8513
GL_TEXTURE_BINDING_CUBE_MAP = 0x8514
GL_TEXTURE_CUBE_MAP_POSITIVE_X = 0x8515
GL_TEXTURE_CUBE_MAP_NEGATIVE_X = 0x8516
GL_TEXTURE_CUBE_MAP_POSITIVE_Y = 0x8517
GL_TEXTURE_CUBE_MAP_NEGATIVE_Y = 0x8518
GL_TEXTURE_CUBE_MAP_POSITIVE_Z = 0x8519
GL_TEXTURE_CUBE_MAP_NEGATIVE_Z = 0x851A
GL_PROXY_TEXTURE_CUBE_MAP = 0x851B
GL_MAX_CUBE_MAP_TEXTURE_SIZE = 0x851C
GL_COMPRESSED_RGB = 0x84ED
GL_COMPRESSED_RGBA = 0x84EE
GL_TEXTURE_COMPRESSION_HINT = 0x84EF
GL_TEXTURE_COMPRESSED_IMAGE_SIZE = 0x86A0
GL_TEXTURE_COMPRESSED = 0x86A1
GL_NUM_COMPRESSED_TEXTURE_FORMATS = 0x86A2
GL_COMPRESSED_TEXTURE_FORMATS = 0x86A3
GL_CLAMP_TO_BORDER = 0x812D
PFNGLACTIVETEXTUREPROC = C(None, UInt)
PFNGLSAMPLECOVERAGEPROC = C(None, Float, UByte)
PFNGLCOMPRESSEDTEXIMAGE3DPROC = C(
    None, UInt, Int, UInt, Int, Int, Int, Int, Int, VoidP)
PFNGLCOMPRESSEDTEXIMAGE2DPROC = C(
    None, UInt, Int, UInt, Int, Int, Int, Int, VoidP)
PFNGLCOMPRESSEDTEXIMAGE1DPROC = C(None, UInt, Int, UInt, Int, Int, Int, VoidP)
PFNGLCOMPRESSEDTEXSUBIMAGE3DPROC = C(
    None, UInt, Int, Int, Int, Int, Int, Int, Int, UInt, Int, VoidP)
PFNGLCOMPRESSEDTEXSUBIMAGE2DPROC = C(
    None, UInt, Int, Int, Int, Int, Int, UInt, Int, VoidP)
PFNGLCOMPRESSEDTEXSUBIMAGE1DPROC = C(
    None, UInt, Int, Int, Int, UInt, Int, VoidP)
PFNGLGETCOMPRESSEDTEXIMAGEPROC = C(None, UInt, Int, VoidP)
glActiveTexture = E('glActiveTexture', None, UInt)
glSampleCoverage = E('glSampleCoverage', None, Float, UByte)
glCompressedTexImage3D = E('glCompressedTexImage3D', None, UInt, Int, UInt,
                           Int, Int, Int, Int, Int, VoidP)
glCompressedTexImage2D = E('glCompressedTexImage2D', None, UInt, Int, UInt,
                           Int, Int, Int, Int, VoidP)
glCompressedTexImage1D = E(
    'glCompressedTexImage1D', None, UInt, Int, UInt, Int, Int, Int, VoidP)
glCompressedTexSubImage3D = E('glCompressedTexSubImage3D', None, UInt, Int,
                              Int, Int, Int, Int, Int, Int, UInt, Int, VoidP)
glCompressedTexSubImage2D = E('glCompressedTexSubImage2D', None, UInt, Int,
                              Int, Int, Int, Int, UInt, Int, VoidP)
glCompressedTexSubImage1D = E('glCompressedTexSubImage1D', None, UInt, Int,
                              Int, Int, UInt, Int, VoidP)
glGetCompressedTexImage = E('glGetCompressedTexImage', None, UInt, Int, VoidP)

__all__ = [
    'GL_VERSION_1_3', 'GL_TEXTURE0', 'GL_TEXTURE1', 'GL_TEXTURE2',
    'GL_TEXTURE3', 'GL_TEXTURE4', 'GL_TEXTURE5', 'GL_TEXTURE6', 'GL_TEXTURE7',
    'GL_TEXTURE8', 'GL_TEXTURE9', 'GL_TEXTURE10', 'GL_TEXTURE11',
    'GL_TEXTURE12', 'GL_TEXTURE13', 'GL_TEXTURE14', 'GL_TEXTURE15',
    'GL_TEXTURE16', 'GL_TEXTURE17', 'GL_TEXTURE18', 'GL_TEXTURE19',
    'GL_TEXTURE20', 'GL_TEXTURE21', 'GL_TEXTURE22', 'GL_TEXTURE23',
    'GL_TEXTURE24', 'GL_TEXTURE25', 'GL_TEXTURE26', 'GL_TEXTURE27',
    'GL_TEXTURE28', 'GL_TEXTURE29', 'GL_TEXTURE30', 'GL_TEXTURE31',
    'GL_ACTIVE_TEXTURE', 'GL_MULTISAMPLE', 'GL_SAMPLE_ALPHA_TO_COVERAGE',
    'GL_SAMPLE_ALPHA_TO_ONE', 'GL_SAMPLE_COVERAGE', 'GL_SAMPLE_BUFFERS',
    'GL_SAMPLES', 'GL_SAMPLE_COVERAGE_VALUE', 'GL_SAMPLE_COVERAGE_INVERT',
    'GL_TEXTURE_CUBE_MAP', 'GL_TEXTURE_BINDING_CUBE_MAP',
    'GL_TEXTURE_CUBE_MAP_POSITIVE_X', 'GL_TEXTURE_CUBE_MAP_NEGATIVE_X',
    'GL_TEXTURE_CUBE_MAP_POSITIVE_Y', 'GL_TEXTURE_CUBE_MAP_NEGATIVE_Y',
    'GL_TEXTURE_CUBE_MAP_POSITIVE_Z', 'GL_TEXTURE_CUBE_MAP_NEGATIVE_Z',
    'GL_PROXY_TEXTURE_CUBE_MAP', 'GL_MAX_CUBE_MAP_TEXTURE_SIZE',
    'GL_COMPRESSED_RGB', 'GL_COMPRESSED_RGBA', 'GL_TEXTURE_COMPRESSION_HINT',
    'GL_TEXTURE_COMPRESSED_IMAGE_SIZE', 'GL_TEXTURE_COMPRESSED',
    'GL_NUM_COMPRESSED_TEXTURE_FORMATS', 'GL_COMPRESSED_TEXTURE_FORMATS',
    'GL_CLAMP_TO_BORDER', 'PFNGLACTIVETEXTUREPROC', 'PFNGLSAMPLECOVERAGEPROC',
    'PFNGLCOMPRESSEDTEXIMAGE3DPROC', 'PFNGLCOMPRESSEDTEXIMAGE2DPROC',
    'PFNGLCOMPRESSEDTEXIMAGE1DPROC', 'PFNGLCOMPRESSEDTEXSUBIMAGE3DPROC',
    'PFNGLCOMPRESSEDTEXSUBIMAGE2DPROC', 'PFNGLCOMPRESSEDTEXSUBIMAGE1DPROC',
    'PFNGLGETCOMPRESSEDTEXIMAGEPROC', 'glActiveTexture', 'glSampleCoverage',
    'glCompressedTexImage3D', 'glCompressedTexImage2D',
    'glCompressedTexImage1D', 'glCompressedTexSubImage3D',
    'glCompressedTexSubImage2D', 'glCompressedTexSubImage1D',
    'glGetCompressedTexImage'
]
