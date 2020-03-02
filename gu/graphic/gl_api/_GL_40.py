from .auto_wrap import *

GL_VERSION_4_0 = 1
GL_SAMPLE_SHADING = 0x8C36
GL_MIN_SAMPLE_SHADING_VALUE = 0x8C37
GL_MIN_PROGRAM_TEXTURE_GATHER_OFFSET = 0x8E5E
GL_MAX_PROGRAM_TEXTURE_GATHER_OFFSET = 0x8E5F
GL_TEXTURE_CUBE_MAP_ARRAY = 0x9009
GL_TEXTURE_BINDING_CUBE_MAP_ARRAY = 0x900A
GL_PROXY_TEXTURE_CUBE_MAP_ARRAY = 0x900B
GL_SAMPLER_CUBE_MAP_ARRAY = 0x900C
GL_SAMPLER_CUBE_MAP_ARRAY_SHADOW = 0x900D
GL_INT_SAMPLER_CUBE_MAP_ARRAY = 0x900E
GL_UNSIGNED_INT_SAMPLER_CUBE_MAP_ARRAY = 0x900F
GL_DRAW_INDIRECT_BUFFER = 0x8F3F
GL_DRAW_INDIRECT_BUFFER_BINDING = 0x8F43
GL_GEOMETRY_SHADER_INVOCATIONS = 0x887F
GL_MAX_GEOMETRY_SHADER_INVOCATIONS = 0x8E5A
GL_MIN_FRAGMENT_INTERPOLATION_OFFSET = 0x8E5B
GL_MAX_FRAGMENT_INTERPOLATION_OFFSET = 0x8E5C
GL_FRAGMENT_INTERPOLATION_OFFSET_BITS = 0x8E5D
GL_MAX_VERTEX_STREAMS = 0x8E71
GL_DOUBLE_VEC2 = 0x8FFC
GL_DOUBLE_VEC3 = 0x8FFD
GL_DOUBLE_VEC4 = 0x8FFE
GL_DOUBLE_MAT2 = 0x8F46
GL_DOUBLE_MAT3 = 0x8F47
GL_DOUBLE_MAT4 = 0x8F48
GL_DOUBLE_MAT2x3 = 0x8F49
GL_DOUBLE_MAT2x4 = 0x8F4A
GL_DOUBLE_MAT3x2 = 0x8F4B
GL_DOUBLE_MAT3x4 = 0x8F4C
GL_DOUBLE_MAT4x2 = 0x8F4D
GL_DOUBLE_MAT4x3 = 0x8F4E
GL_ACTIVE_SUBROUTINES = 0x8DE5
GL_ACTIVE_SUBROUTINE_UNIFORMS = 0x8DE6
GL_ACTIVE_SUBROUTINE_UNIFORM_LOCATIONS = 0x8E47
GL_ACTIVE_SUBROUTINE_MAX_LENGTH = 0x8E48
GL_ACTIVE_SUBROUTINE_UNIFORM_MAX_LENGTH = 0x8E49
GL_MAX_SUBROUTINES = 0x8DE7
GL_MAX_SUBROUTINE_UNIFORM_LOCATIONS = 0x8DE8
GL_NUM_COMPATIBLE_SUBROUTINES = 0x8E4A
GL_COMPATIBLE_SUBROUTINES = 0x8E4B
GL_PATCHES = 0x000E
GL_PATCH_VERTICES = 0x8E72
GL_PATCH_DEFAULT_INNER_LEVEL = 0x8E73
GL_PATCH_DEFAULT_OUTER_LEVEL = 0x8E74
GL_TESS_CONTROL_OUTPUT_VERTICES = 0x8E75
GL_TESS_GEN_MODE = 0x8E76
GL_TESS_GEN_SPACING = 0x8E77
GL_TESS_GEN_VERTEX_ORDER = 0x8E78
GL_TESS_GEN_POINT_MODE = 0x8E79
GL_ISOLINES = 0x8E7A
GL_FRACTIONAL_ODD = 0x8E7B
GL_FRACTIONAL_EVEN = 0x8E7C
GL_MAX_PATCH_VERTICES = 0x8E7D
GL_MAX_TESS_GEN_LEVEL = 0x8E7E
GL_MAX_TESS_CONTROL_UNIFORM_COMPONENTS = 0x8E7F
GL_MAX_TESS_EVALUATION_UNIFORM_COMPONENTS = 0x8E80
GL_MAX_TESS_CONTROL_TEXTURE_IMAGE_UNITS = 0x8E81
GL_MAX_TESS_EVALUATION_TEXTURE_IMAGE_UNITS = 0x8E82
GL_MAX_TESS_CONTROL_OUTPUT_COMPONENTS = 0x8E83
GL_MAX_TESS_PATCH_COMPONENTS = 0x8E84
GL_MAX_TESS_CONTROL_TOTAL_OUTPUT_COMPONENTS = 0x8E85
GL_MAX_TESS_EVALUATION_OUTPUT_COMPONENTS = 0x8E86
GL_MAX_TESS_CONTROL_UNIFORM_BLOCKS = 0x8E89
GL_MAX_TESS_EVALUATION_UNIFORM_BLOCKS = 0x8E8A
GL_MAX_TESS_CONTROL_INPUT_COMPONENTS = 0x886C
GL_MAX_TESS_EVALUATION_INPUT_COMPONENTS = 0x886D
GL_MAX_COMBINED_TESS_CONTROL_UNIFORM_COMPONENTS = 0x8E1E
GL_MAX_COMBINED_TESS_EVALUATION_UNIFORM_COMPONENTS = 0x8E1F
GL_UNIFORM_BLOCK_REFERENCED_BY_TESS_CONTROL_SHADER = 0x84F0
GL_UNIFORM_BLOCK_REFERENCED_BY_TESS_EVALUATION_SHADER = 0x84F1
GL_TESS_EVALUATION_SHADER = 0x8E87
GL_TESS_CONTROL_SHADER = 0x8E88
GL_TRANSFORM_FEEDBACK = 0x8E22
GL_TRANSFORM_FEEDBACK_BUFFER_PAUSED = 0x8E23
GL_TRANSFORM_FEEDBACK_BUFFER_ACTIVE = 0x8E24
GL_TRANSFORM_FEEDBACK_BINDING = 0x8E25
GL_MAX_TRANSFORM_FEEDBACK_BUFFERS = 0x8E70
PFNGLMINSAMPLESHADINGPROC = C(None, Float)
PFNGLBLENDEQUATIONIPROC = C(None, UInt, UInt)
PFNGLBLENDEQUATIONSEPARATEIPROC = C(None, UInt, UInt, UInt)
PFNGLBLENDFUNCIPROC = C(None, UInt, UInt, UInt)
PFNGLBLENDFUNCSEPARATEIPROC = C(None, UInt, UInt, UInt, UInt, UInt)
PFNGLDRAWARRAYSINDIRECTPROC = C(None, UInt, VoidP)
PFNGLDRAWELEMENTSINDIRECTPROC = C(None, UInt, UInt, VoidP)
PFNGLUNIFORM1DPROC = C(None, Int, Double)
PFNGLUNIFORM2DPROC = C(None, Int, Double, Double)
PFNGLUNIFORM3DPROC = C(None, Int, Double, Double, Double)
PFNGLUNIFORM4DPROC = C(None, Int, Double, Double, Double, Double)
PFNGLUNIFORM1DVPROC = C(None, Int, Int, P(Double))
PFNGLUNIFORM2DVPROC = C(None, Int, Int, P(Double))
PFNGLUNIFORM3DVPROC = C(None, Int, Int, P(Double))
PFNGLUNIFORM4DVPROC = C(None, Int, Int, P(Double))
PFNGLUNIFORMMATRIX2DVPROC = C(None, Int, Int, UByte, P(Double))
PFNGLUNIFORMMATRIX3DVPROC = C(None, Int, Int, UByte, P(Double))
PFNGLUNIFORMMATRIX4DVPROC = C(None, Int, Int, UByte, P(Double))
PFNGLUNIFORMMATRIX2X3DVPROC = C(None, Int, Int, UByte, P(Double))
PFNGLUNIFORMMATRIX2X4DVPROC = C(None, Int, Int, UByte, P(Double))
PFNGLUNIFORMMATRIX3X2DVPROC = C(None, Int, Int, UByte, P(Double))
PFNGLUNIFORMMATRIX3X4DVPROC = C(None, Int, Int, UByte, P(Double))
PFNGLUNIFORMMATRIX4X2DVPROC = C(None, Int, Int, UByte, P(Double))
PFNGLUNIFORMMATRIX4X3DVPROC = C(None, Int, Int, UByte, P(Double))
PFNGLGETUNIFORMDVPROC = C(None, UInt, Int, P(Double))
PFNGLGETSUBROUTINEUNIFORMLOCATIONPROC = C(Int, UInt, UInt, CharP)
PFNGLGETSUBROUTINEINDEXPROC = C(UInt, UInt, UInt, CharP)
PFNGLGETACTIVESUBROUTINEUNIFORMIVPROC = C(None, UInt, UInt, UInt, UInt,
                                          P(Int))
PFNGLGETACTIVESUBROUTINEUNIFORMNAMEPROC = C(None, UInt, UInt, UInt, Int,
                                            P(Int), CharP)
PFNGLGETACTIVESUBROUTINENAMEPROC = C(None, UInt, UInt, UInt, Int, P(Int),
                                     CharP)
PFNGLUNIFORMSUBROUTINESUIVPROC = C(None, UInt, Int, P(UInt))
PFNGLGETUNIFORMSUBROUTINEUIVPROC = C(None, UInt, Int, P(UInt))
PFNGLGETPROGRAMSTAGEIVPROC = C(None, UInt, UInt, UInt, P(Int))
PFNGLPATCHPARAMETERIPROC = C(None, UInt, Int)
PFNGLPATCHPARAMETERFVPROC = C(None, UInt, P(Float))
PFNGLBINDTRANSFORMFEEDBACKPROC = C(None, UInt, UInt)
PFNGLDELETETRANSFORMFEEDBACKSPROC = C(None, Int, P(UInt))
PFNGLGENTRANSFORMFEEDBACKSPROC = C(None, Int, P(UInt))
PFNGLISTRANSFORMFEEDBACKPROC = C(UByte, UInt)
PFNGLPAUSETRANSFORMFEEDBACKPROC = C(None)
PFNGLRESUMETRANSFORMFEEDBACKPROC = C(None)
PFNGLDRAWTRANSFORMFEEDBACKPROC = C(None, UInt, UInt)
PFNGLDRAWTRANSFORMFEEDBACKSTREAMPROC = C(None, UInt, UInt, UInt)
PFNGLBEGINQUERYINDEXEDPROC = C(None, UInt, UInt, UInt)
PFNGLENDQUERYINDEXEDPROC = C(None, UInt, UInt)
PFNGLGETQUERYINDEXEDIVPROC = C(None, UInt, UInt, UInt, P(Int))
glMinSampleShading = E('glMinSampleShading', None, Float)
glBlendEquationi = E('glBlendEquationi', None, UInt, UInt)
glBlendEquationSeparatei = E('glBlendEquationSeparatei', None, UInt, UInt,
                             UInt)
glBlendFunci = E('glBlendFunci', None, UInt, UInt, UInt)
glBlendFuncSeparatei = E('glBlendFuncSeparatei', None, UInt, UInt, UInt, UInt,
                         UInt)
glDrawArraysIndirect = E('glDrawArraysIndirect', None, UInt, VoidP)
glDrawElementsIndirect = E('glDrawElementsIndirect', None, UInt, UInt, VoidP)
glUniform1d = E('glUniform1d', None, Int, Double)
glUniform2d = E('glUniform2d', None, Int, Double, Double)
glUniform3d = E('glUniform3d', None, Int, Double, Double, Double)
glUniform4d = E('glUniform4d', None, Int, Double, Double, Double, Double)
glUniform1dv = E('glUniform1dv', None, Int, Int, P(Double))
glUniform2dv = E('glUniform2dv', None, Int, Int, P(Double))
glUniform3dv = E('glUniform3dv', None, Int, Int, P(Double))
glUniform4dv = E('glUniform4dv', None, Int, Int, P(Double))
glUniformMatrix2dv = E('glUniformMatrix2dv', None, Int, Int, UByte, P(Double))
glUniformMatrix3dv = E('glUniformMatrix3dv', None, Int, Int, UByte, P(Double))
glUniformMatrix4dv = E('glUniformMatrix4dv', None, Int, Int, UByte, P(Double))
glUniformMatrix2x3dv = E('glUniformMatrix2x3dv', None, Int, Int, UByte,
                         P(Double))
glUniformMatrix2x4dv = E('glUniformMatrix2x4dv', None, Int, Int, UByte,
                         P(Double))
glUniformMatrix3x2dv = E('glUniformMatrix3x2dv', None, Int, Int, UByte,
                         P(Double))
glUniformMatrix3x4dv = E('glUniformMatrix3x4dv', None, Int, Int, UByte,
                         P(Double))
glUniformMatrix4x2dv = E('glUniformMatrix4x2dv', None, Int, Int, UByte,
                         P(Double))
glUniformMatrix4x3dv = E('glUniformMatrix4x3dv', None, Int, Int, UByte,
                         P(Double))
glGetUniformdv = E('glGetUniformdv', None, UInt, Int, P(Double))
glGetSubroutineUniformLocation = E('glGetSubroutineUniformLocation', Int,
                                   UInt, UInt, CharP)
glGetSubroutineIndex = E('glGetSubroutineIndex', UInt, UInt, UInt, CharP)
glGetActiveSubroutineUniformiv = E('glGetActiveSubroutineUniformiv', None,
                                   UInt, UInt, UInt, UInt, P(Int))
glGetActiveSubroutineUniformName = E('glGetActiveSubroutineUniformName', None,
                                     UInt, UInt, UInt, Int, P(Int), CharP)
glGetActiveSubroutineName = E('glGetActiveSubroutineName', None, UInt, UInt,
                              UInt, Int, P(Int), CharP)
glUniformSubroutinesuiv = E('glUniformSubroutinesuiv', None, UInt, Int,
                            P(UInt))
glGetUniformSubroutineuiv = E('glGetUniformSubroutineuiv', None, UInt, Int,
                              P(UInt))
glGetProgramStageiv = E('glGetProgramStageiv', None, UInt, UInt, UInt, P(Int))
glPatchParameteri = E('glPatchParameteri', None, UInt, Int)
glPatchParameterfv = E('glPatchParameterfv', None, UInt, P(Float))
glBindTransformFeedback = E('glBindTransformFeedback', None, UInt, UInt)
glDeleteTransformFeedbacks = E('glDeleteTransformFeedbacks', None, Int,
                               P(UInt))
glGenTransformFeedbacks = E('glGenTransformFeedbacks', None, Int, P(UInt))
glIsTransformFeedback = E('glIsTransformFeedback', UByte, UInt)
glPauseTransformFeedback = E('glPauseTransformFeedback', None)
glResumeTransformFeedback = E('glResumeTransformFeedback', None)
glDrawTransformFeedback = E('glDrawTransformFeedback', None, UInt, UInt)
glDrawTransformFeedbackStream = E('glDrawTransformFeedbackStream', None, UInt,
                                  UInt, UInt)
glBeginQueryIndexed = E('glBeginQueryIndexed', None, UInt, UInt, UInt)
glEndQueryIndexed = E('glEndQueryIndexed', None, UInt, UInt)
glGetQueryIndexediv = E('glGetQueryIndexediv', None, UInt, UInt, UInt, P(Int))

__all__ = [
    'GL_VERSION_4_0', 'GL_SAMPLE_SHADING', 'GL_MIN_SAMPLE_SHADING_VALUE',
    'GL_MIN_PROGRAM_TEXTURE_GATHER_OFFSET',
    'GL_MAX_PROGRAM_TEXTURE_GATHER_OFFSET', 'GL_TEXTURE_CUBE_MAP_ARRAY',
    'GL_TEXTURE_BINDING_CUBE_MAP_ARRAY', 'GL_PROXY_TEXTURE_CUBE_MAP_ARRAY',
    'GL_SAMPLER_CUBE_MAP_ARRAY', 'GL_SAMPLER_CUBE_MAP_ARRAY_SHADOW',
    'GL_INT_SAMPLER_CUBE_MAP_ARRAY', 'GL_UNSIGNED_INT_SAMPLER_CUBE_MAP_ARRAY',
    'GL_DRAW_INDIRECT_BUFFER', 'GL_DRAW_INDIRECT_BUFFER_BINDING',
    'GL_GEOMETRY_SHADER_INVOCATIONS', 'GL_MAX_GEOMETRY_SHADER_INVOCATIONS',
    'GL_MIN_FRAGMENT_INTERPOLATION_OFFSET',
    'GL_MAX_FRAGMENT_INTERPOLATION_OFFSET',
    'GL_FRAGMENT_INTERPOLATION_OFFSET_BITS', 'GL_MAX_VERTEX_STREAMS',
    'GL_DOUBLE_VEC2', 'GL_DOUBLE_VEC3', 'GL_DOUBLE_VEC4', 'GL_DOUBLE_MAT2',
    'GL_DOUBLE_MAT3', 'GL_DOUBLE_MAT4', 'GL_DOUBLE_MAT2x3',
    'GL_DOUBLE_MAT2x4', 'GL_DOUBLE_MAT3x2', 'GL_DOUBLE_MAT3x4',
    'GL_DOUBLE_MAT4x2', 'GL_DOUBLE_MAT4x3', 'GL_ACTIVE_SUBROUTINES',
    'GL_ACTIVE_SUBROUTINE_UNIFORMS', 'GL_ACTIVE_SUBROUTINE_UNIFORM_LOCATIONS',
    'GL_ACTIVE_SUBROUTINE_MAX_LENGTH',
    'GL_ACTIVE_SUBROUTINE_UNIFORM_MAX_LENGTH', 'GL_MAX_SUBROUTINES',
    'GL_MAX_SUBROUTINE_UNIFORM_LOCATIONS', 'GL_NUM_COMPATIBLE_SUBROUTINES',
    'GL_COMPATIBLE_SUBROUTINES', 'GL_PATCHES', 'GL_PATCH_VERTICES',
    'GL_PATCH_DEFAULT_INNER_LEVEL', 'GL_PATCH_DEFAULT_OUTER_LEVEL',
    'GL_TESS_CONTROL_OUTPUT_VERTICES', 'GL_TESS_GEN_MODE',
    'GL_TESS_GEN_SPACING', 'GL_TESS_GEN_VERTEX_ORDER',
    'GL_TESS_GEN_POINT_MODE', 'GL_ISOLINES', 'GL_FRACTIONAL_ODD',
    'GL_FRACTIONAL_EVEN', 'GL_MAX_PATCH_VERTICES', 'GL_MAX_TESS_GEN_LEVEL',
    'GL_MAX_TESS_CONTROL_UNIFORM_COMPONENTS',
    'GL_MAX_TESS_EVALUATION_UNIFORM_COMPONENTS',
    'GL_MAX_TESS_CONTROL_TEXTURE_IMAGE_UNITS',
    'GL_MAX_TESS_EVALUATION_TEXTURE_IMAGE_UNITS',
    'GL_MAX_TESS_CONTROL_OUTPUT_COMPONENTS', 'GL_MAX_TESS_PATCH_COMPONENTS',
    'GL_MAX_TESS_CONTROL_TOTAL_OUTPUT_COMPONENTS',
    'GL_MAX_TESS_EVALUATION_OUTPUT_COMPONENTS',
    'GL_MAX_TESS_CONTROL_UNIFORM_BLOCKS',
    'GL_MAX_TESS_EVALUATION_UNIFORM_BLOCKS',
    'GL_MAX_TESS_CONTROL_INPUT_COMPONENTS',
    'GL_MAX_TESS_EVALUATION_INPUT_COMPONENTS',
    'GL_MAX_COMBINED_TESS_CONTROL_UNIFORM_COMPONENTS',
    'GL_MAX_COMBINED_TESS_EVALUATION_UNIFORM_COMPONENTS',
    'GL_UNIFORM_BLOCK_REFERENCED_BY_TESS_CONTROL_SHADER',
    'GL_UNIFORM_BLOCK_REFERENCED_BY_TESS_EVALUATION_SHADER',
    'GL_TESS_EVALUATION_SHADER', 'GL_TESS_CONTROL_SHADER',
    'GL_TRANSFORM_FEEDBACK', 'GL_TRANSFORM_FEEDBACK_BUFFER_PAUSED',
    'GL_TRANSFORM_FEEDBACK_BUFFER_ACTIVE', 'GL_TRANSFORM_FEEDBACK_BINDING',
    'GL_MAX_TRANSFORM_FEEDBACK_BUFFERS', 'PFNGLMINSAMPLESHADINGPROC',
    'PFNGLBLENDEQUATIONIPROC', 'PFNGLBLENDEQUATIONSEPARATEIPROC',
    'PFNGLBLENDFUNCIPROC', 'PFNGLBLENDFUNCSEPARATEIPROC',
    'PFNGLDRAWARRAYSINDIRECTPROC', 'PFNGLDRAWELEMENTSINDIRECTPROC',
    'PFNGLUNIFORM1DPROC', 'PFNGLUNIFORM2DPROC', 'PFNGLUNIFORM3DPROC',
    'PFNGLUNIFORM4DPROC', 'PFNGLUNIFORM1DVPROC', 'PFNGLUNIFORM2DVPROC',
    'PFNGLUNIFORM3DVPROC', 'PFNGLUNIFORM4DVPROC', 'PFNGLUNIFORMMATRIX2DVPROC',
    'PFNGLUNIFORMMATRIX3DVPROC', 'PFNGLUNIFORMMATRIX4DVPROC',
    'PFNGLUNIFORMMATRIX2X3DVPROC', 'PFNGLUNIFORMMATRIX2X4DVPROC',
    'PFNGLUNIFORMMATRIX3X2DVPROC', 'PFNGLUNIFORMMATRIX3X4DVPROC',
    'PFNGLUNIFORMMATRIX4X2DVPROC', 'PFNGLUNIFORMMATRIX4X3DVPROC',
    'PFNGLGETUNIFORMDVPROC', 'PFNGLGETSUBROUTINEUNIFORMLOCATIONPROC',
    'PFNGLGETSUBROUTINEINDEXPROC', 'PFNGLGETACTIVESUBROUTINEUNIFORMIVPROC',
    'PFNGLGETACTIVESUBROUTINEUNIFORMNAMEPROC',
    'PFNGLGETACTIVESUBROUTINENAMEPROC', 'PFNGLUNIFORMSUBROUTINESUIVPROC',
    'PFNGLGETUNIFORMSUBROUTINEUIVPROC', 'PFNGLGETPROGRAMSTAGEIVPROC',
    'PFNGLPATCHPARAMETERIPROC', 'PFNGLPATCHPARAMETERFVPROC',
    'PFNGLBINDTRANSFORMFEEDBACKPROC', 'PFNGLDELETETRANSFORMFEEDBACKSPROC',
    'PFNGLGENTRANSFORMFEEDBACKSPROC', 'PFNGLISTRANSFORMFEEDBACKPROC',
    'PFNGLPAUSETRANSFORMFEEDBACKPROC', 'PFNGLRESUMETRANSFORMFEEDBACKPROC',
    'PFNGLDRAWTRANSFORMFEEDBACKPROC', 'PFNGLDRAWTRANSFORMFEEDBACKSTREAMPROC',
    'PFNGLBEGINQUERYINDEXEDPROC', 'PFNGLENDQUERYINDEXEDPROC',
    'PFNGLGETQUERYINDEXEDIVPROC', 'glMinSampleShading', 'glBlendEquationi',
    'glBlendEquationSeparatei', 'glBlendFunci', 'glBlendFuncSeparatei',
    'glDrawArraysIndirect', 'glDrawElementsIndirect', 'glUniform1d',
    'glUniform2d', 'glUniform3d', 'glUniform4d', 'glUniform1dv',
    'glUniform2dv', 'glUniform3dv', 'glUniform4dv', 'glUniformMatrix2dv',
    'glUniformMatrix3dv', 'glUniformMatrix4dv', 'glUniformMatrix2x3dv',
    'glUniformMatrix2x4dv', 'glUniformMatrix3x2dv', 'glUniformMatrix3x4dv',
    'glUniformMatrix4x2dv', 'glUniformMatrix4x3dv', 'glGetUniformdv',
    'glGetSubroutineUniformLocation', 'glGetSubroutineIndex',
    'glGetActiveSubroutineUniformiv', 'glGetActiveSubroutineUniformName',
    'glGetActiveSubroutineName', 'glUniformSubroutinesuiv',
    'glGetUniformSubroutineuiv', 'glGetProgramStageiv', 'glPatchParameteri',
    'glPatchParameterfv', 'glBindTransformFeedback',
    'glDeleteTransformFeedbacks', 'glGenTransformFeedbacks',
    'glIsTransformFeedback', 'glPauseTransformFeedback',
    'glResumeTransformFeedback', 'glDrawTransformFeedback',
    'glDrawTransformFeedbackStream', 'glBeginQueryIndexed',
    'glEndQueryIndexed', 'glGetQueryIndexediv'
]
