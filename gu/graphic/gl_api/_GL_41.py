from .auto_wrap import *

GL_VERSION_4_1 = 1
GL_FIXED = 0x140C
GL_IMPLEMENTATION_COLOR_READ_TYPE = 0x8B9A
GL_IMPLEMENTATION_COLOR_READ_FORMAT = 0x8B9B
GL_LOW_FLOAT = 0x8DF0
GL_MEDIUM_FLOAT = 0x8DF1
GL_HIGH_FLOAT = 0x8DF2
GL_LOW_INT = 0x8DF3
GL_MEDIUM_INT = 0x8DF4
GL_HIGH_INT = 0x8DF5
GL_SHADER_COMPILER = 0x8DFA
GL_SHADER_BINARY_FORMATS = 0x8DF8
GL_NUM_SHADER_BINARY_FORMATS = 0x8DF9
GL_MAX_VERTEX_UNIFORM_VECTORS = 0x8DFB
GL_MAX_VARYING_VECTORS = 0x8DFC
GL_MAX_FRAGMENT_UNIFORM_VECTORS = 0x8DFD
GL_RGB565 = 0x8D62
GL_PROGRAM_BINARY_RETRIEVABLE_HINT = 0x8257
GL_PROGRAM_BINARY_LENGTH = 0x8741
GL_NUM_PROGRAM_BINARY_FORMATS = 0x87FE
GL_PROGRAM_BINARY_FORMATS = 0x87FF
GL_VERTEX_SHADER_BIT = 0x00000001
GL_FRAGMENT_SHADER_BIT = 0x00000002
GL_GEOMETRY_SHADER_BIT = 0x00000004
GL_TESS_CONTROL_SHADER_BIT = 0x00000008
GL_TESS_EVALUATION_SHADER_BIT = 0x00000010
GL_ALL_SHADER_BITS = 0xFFFFFFFF
GL_PROGRAM_SEPARABLE = 0x8258
GL_ACTIVE_PROGRAM = 0x8259
GL_PROGRAM_PIPELINE_BINDING = 0x825A
GL_MAX_VIEWPORTS = 0x825B
GL_VIEWPORT_SUBPIXEL_BITS = 0x825C
GL_VIEWPORT_BOUNDS_RANGE = 0x825D
GL_LAYER_PROVOKING_VERTEX = 0x825E
GL_VIEWPORT_INDEX_PROVOKING_VERTEX = 0x825F
GL_UNDEFINED_VERTEX = 0x8260
PFNGLRELEASESHADERCOMPILERPROC = C(None)
PFNGLSHADERBINARYPROC = C(None, Int, P(UInt), UInt, VoidP, Int)
PFNGLGETSHADERPRECISIONFORMATPROC = C(None, UInt, UInt, P(Int), P(Int))
PFNGLDEPTHRANGEFPROC = C(None, Float, Float)
PFNGLCLEARDEPTHFPROC = C(None, Float)
PFNGLGETPROGRAMBINARYPROC = C(None, UInt, Int, P(Int), P(UInt), VoidP)
PFNGLPROGRAMBINARYPROC = C(None, UInt, UInt, VoidP, Int)
PFNGLPROGRAMPARAMETERIPROC = C(None, UInt, UInt, Int)
PFNGLUSEPROGRAMSTAGESPROC = C(None, UInt, UInt, UInt)
PFNGLACTIVESHADERPROGRAMPROC = C(None, UInt, UInt)
PFNGLCREATESHADERPROGRAMVPROC = C(UInt, UInt, Int, CharP)
PFNGLBINDPROGRAMPIPELINEPROC = C(None, UInt)
PFNGLDELETEPROGRAMPIPELINESPROC = C(None, Int, P(UInt))
PFNGLGENPROGRAMPIPELINESPROC = C(None, Int, P(UInt))
PFNGLISPROGRAMPIPELINEPROC = C(UByte, UInt)
PFNGLGETPROGRAMPIPELINEIVPROC = C(None, UInt, UInt, P(Int))
PFNGLPROGRAMUNIFORM1IPROC = C(None, UInt, Int, Int)
PFNGLPROGRAMUNIFORM1IVPROC = C(None, UInt, Int, Int, P(Int))
PFNGLPROGRAMUNIFORM1FPROC = C(None, UInt, Int, Float)
PFNGLPROGRAMUNIFORM1FVPROC = C(None, UInt, Int, Int, P(Float))
PFNGLPROGRAMUNIFORM1DPROC = C(None, UInt, Int, Double)
PFNGLPROGRAMUNIFORM1DVPROC = C(None, UInt, Int, Int, P(Double))
PFNGLPROGRAMUNIFORM1UIPROC = C(None, UInt, Int, UInt)
PFNGLPROGRAMUNIFORM1UIVPROC = C(None, UInt, Int, Int, P(UInt))
PFNGLPROGRAMUNIFORM2IPROC = C(None, UInt, Int, Int, Int)
PFNGLPROGRAMUNIFORM2IVPROC = C(None, UInt, Int, Int, P(Int))
PFNGLPROGRAMUNIFORM2FPROC = C(None, UInt, Int, Float, Float)
PFNGLPROGRAMUNIFORM2FVPROC = C(None, UInt, Int, Int, P(Float))
PFNGLPROGRAMUNIFORM2DPROC = C(None, UInt, Int, Double, Double)
PFNGLPROGRAMUNIFORM2DVPROC = C(None, UInt, Int, Int, P(Double))
PFNGLPROGRAMUNIFORM2UIPROC = C(None, UInt, Int, UInt, UInt)
PFNGLPROGRAMUNIFORM2UIVPROC = C(None, UInt, Int, Int, P(UInt))
PFNGLPROGRAMUNIFORM3IPROC = C(None, UInt, Int, Int, Int, Int)
PFNGLPROGRAMUNIFORM3IVPROC = C(None, UInt, Int, Int, P(Int))
PFNGLPROGRAMUNIFORM3FPROC = C(None, UInt, Int, Float, Float, Float)
PFNGLPROGRAMUNIFORM3FVPROC = C(None, UInt, Int, Int, P(Float))
PFNGLPROGRAMUNIFORM3DPROC = C(None, UInt, Int, Double, Double, Double)
PFNGLPROGRAMUNIFORM3DVPROC = C(None, UInt, Int, Int, P(Double))
PFNGLPROGRAMUNIFORM3UIPROC = C(None, UInt, Int, UInt, UInt, UInt)
PFNGLPROGRAMUNIFORM3UIVPROC = C(None, UInt, Int, Int, P(UInt))
PFNGLPROGRAMUNIFORM4IPROC = C(None, UInt, Int, Int, Int, Int, Int)
PFNGLPROGRAMUNIFORM4IVPROC = C(None, UInt, Int, Int, P(Int))
PFNGLPROGRAMUNIFORM4FPROC = C(None, UInt, Int, Float, Float, Float, Float)
PFNGLPROGRAMUNIFORM4FVPROC = C(None, UInt, Int, Int, P(Float))
PFNGLPROGRAMUNIFORM4DPROC = C(None, UInt, Int, Double, Double, Double, Double)
PFNGLPROGRAMUNIFORM4DVPROC = C(None, UInt, Int, Int, P(Double))
PFNGLPROGRAMUNIFORM4UIPROC = C(None, UInt, Int, UInt, UInt, UInt, UInt)
PFNGLPROGRAMUNIFORM4UIVPROC = C(None, UInt, Int, Int, P(UInt))
PFNGLPROGRAMUNIFORMMATRIX2FVPROC = C(None, UInt, Int, Int, UByte, P(Float))
PFNGLPROGRAMUNIFORMMATRIX3FVPROC = C(None, UInt, Int, Int, UByte, P(Float))
PFNGLPROGRAMUNIFORMMATRIX4FVPROC = C(None, UInt, Int, Int, UByte, P(Float))
PFNGLPROGRAMUNIFORMMATRIX2DVPROC = C(None, UInt, Int, Int, UByte, P(Double))
PFNGLPROGRAMUNIFORMMATRIX3DVPROC = C(None, UInt, Int, Int, UByte, P(Double))
PFNGLPROGRAMUNIFORMMATRIX4DVPROC = C(None, UInt, Int, Int, UByte, P(Double))
PFNGLPROGRAMUNIFORMMATRIX2X3FVPROC = C(None, UInt, Int, Int, UByte, P(Float))
PFNGLPROGRAMUNIFORMMATRIX3X2FVPROC = C(None, UInt, Int, Int, UByte, P(Float))
PFNGLPROGRAMUNIFORMMATRIX2X4FVPROC = C(None, UInt, Int, Int, UByte, P(Float))
PFNGLPROGRAMUNIFORMMATRIX4X2FVPROC = C(None, UInt, Int, Int, UByte, P(Float))
PFNGLPROGRAMUNIFORMMATRIX3X4FVPROC = C(None, UInt, Int, Int, UByte, P(Float))
PFNGLPROGRAMUNIFORMMATRIX4X3FVPROC = C(None, UInt, Int, Int, UByte, P(Float))
PFNGLPROGRAMUNIFORMMATRIX2X3DVPROC = C(None, UInt, Int, Int, UByte, P(Double))
PFNGLPROGRAMUNIFORMMATRIX3X2DVPROC = C(None, UInt, Int, Int, UByte, P(Double))
PFNGLPROGRAMUNIFORMMATRIX2X4DVPROC = C(None, UInt, Int, Int, UByte, P(Double))
PFNGLPROGRAMUNIFORMMATRIX4X2DVPROC = C(None, UInt, Int, Int, UByte, P(Double))
PFNGLPROGRAMUNIFORMMATRIX3X4DVPROC = C(None, UInt, Int, Int, UByte, P(Double))
PFNGLPROGRAMUNIFORMMATRIX4X3DVPROC = C(None, UInt, Int, Int, UByte, P(Double))
PFNGLVALIDATEPROGRAMPIPELINEPROC = C(None, UInt)
PFNGLGETPROGRAMPIPELINEINFOLOGPROC = C(None, UInt, Int, P(Int), CharP)
PFNGLVERTEXATTRIBL1DPROC = C(None, UInt, Double)
PFNGLVERTEXATTRIBL2DPROC = C(None, UInt, Double, Double)
PFNGLVERTEXATTRIBL3DPROC = C(None, UInt, Double, Double, Double)
PFNGLVERTEXATTRIBL4DPROC = C(None, UInt, Double, Double, Double, Double)
PFNGLVERTEXATTRIBL1DVPROC = C(None, UInt, P(Double))
PFNGLVERTEXATTRIBL2DVPROC = C(None, UInt, P(Double))
PFNGLVERTEXATTRIBL3DVPROC = C(None, UInt, P(Double))
PFNGLVERTEXATTRIBL4DVPROC = C(None, UInt, P(Double))
PFNGLVERTEXATTRIBLPOINTERPROC = C(None, UInt, Int, UInt, Int, VoidP)
PFNGLGETVERTEXATTRIBLDVPROC = C(None, UInt, UInt, P(Double))
PFNGLVIEWPORTARRAYVPROC = C(None, UInt, Int, P(Float))
PFNGLVIEWPORTINDEXEDFPROC = C(None, UInt, Float, Float, Float, Float)
PFNGLVIEWPORTINDEXEDFVPROC = C(None, UInt, P(Float))
PFNGLSCISSORARRAYVPROC = C(None, UInt, Int, P(Int))
PFNGLSCISSORINDEXEDPROC = C(None, UInt, Int, Int, Int, Int)
PFNGLSCISSORINDEXEDVPROC = C(None, UInt, P(Int))
PFNGLDEPTHRANGEARRAYVPROC = C(None, UInt, Int, P(Double))
PFNGLDEPTHRANGEINDEXEDPROC = C(None, UInt, Double, Double)
PFNGLGETFLOATI_VPROC = C(None, UInt, UInt, P(Float))
PFNGLGETDOUBLEI_VPROC = C(None, UInt, UInt, P(Double))
glReleaseShaderCompiler = E('glReleaseShaderCompiler', None)
glShaderBinary = E('glShaderBinary', None, Int, P(UInt), UInt, VoidP, Int)
glGetShaderPrecisionFormat = E('glGetShaderPrecisionFormat', None, UInt, UInt,
                               P(Int), P(Int))
glDepthRangef = E('glDepthRangef', None, Float, Float)
glClearDepthf = E('glClearDepthf', None, Float)
glGetProgramBinary = E('glGetProgramBinary', None, UInt, Int, P(Int), P(UInt),
                       VoidP)
glProgramBinary = E('glProgramBinary', None, UInt, UInt, VoidP, Int)
glProgramParameteri = E('glProgramParameteri', None, UInt, UInt, Int)
glUseProgramStages = E('glUseProgramStages', None, UInt, UInt, UInt)
glActiveShaderProgram = E('glActiveShaderProgram', None, UInt, UInt)
glCreateShaderProgramv = E('glCreateShaderProgramv', UInt, UInt, Int, CharP)
glBindProgramPipeline = E('glBindProgramPipeline', None, UInt)
glDeleteProgramPipelines = E('glDeleteProgramPipelines', None, Int, P(UInt))
glGenProgramPipelines = E('glGenProgramPipelines', None, Int, P(UInt))
glIsProgramPipeline = E('glIsProgramPipeline', UByte, UInt)
glGetProgramPipelineiv = E('glGetProgramPipelineiv', None, UInt, UInt, P(Int))
glProgramUniform1i = E('glProgramUniform1i', None, UInt, Int, Int)
glProgramUniform1iv = E('glProgramUniform1iv', None, UInt, Int, Int, P(Int))
glProgramUniform1f = E('glProgramUniform1f', None, UInt, Int, Float)
glProgramUniform1fv = E('glProgramUniform1fv', None, UInt, Int, Int, P(Float))
glProgramUniform1d = E('glProgramUniform1d', None, UInt, Int, Double)
glProgramUniform1dv = E('glProgramUniform1dv', None, UInt, Int, Int,
                        P(Double))
glProgramUniform1ui = E('glProgramUniform1ui', None, UInt, Int, UInt)
glProgramUniform1uiv = E('glProgramUniform1uiv', None, UInt, Int, Int,
                         P(UInt))
glProgramUniform2i = E('glProgramUniform2i', None, UInt, Int, Int, Int)
glProgramUniform2iv = E('glProgramUniform2iv', None, UInt, Int, Int, P(Int))
glProgramUniform2f = E('glProgramUniform2f', None, UInt, Int, Float, Float)
glProgramUniform2fv = E('glProgramUniform2fv', None, UInt, Int, Int, P(Float))
glProgramUniform2d = E('glProgramUniform2d', None, UInt, Int, Double, Double)
glProgramUniform2dv = E('glProgramUniform2dv', None, UInt, Int, Int,
                        P(Double))
glProgramUniform2ui = E('glProgramUniform2ui', None, UInt, Int, UInt, UInt)
glProgramUniform2uiv = E('glProgramUniform2uiv', None, UInt, Int, Int,
                         P(UInt))
glProgramUniform3i = E('glProgramUniform3i', None, UInt, Int, Int, Int, Int)
glProgramUniform3iv = E('glProgramUniform3iv', None, UInt, Int, Int, P(Int))
glProgramUniform3f = E('glProgramUniform3f', None, UInt, Int, Float, Float,
                       Float)
glProgramUniform3fv = E('glProgramUniform3fv', None, UInt, Int, Int, P(Float))
glProgramUniform3d = E('glProgramUniform3d', None, UInt, Int, Double, Double,
                       Double)
glProgramUniform3dv = E('glProgramUniform3dv', None, UInt, Int, Int,
                        P(Double))
glProgramUniform3ui = E('glProgramUniform3ui', None, UInt, Int, UInt, UInt,
                        UInt)
glProgramUniform3uiv = E('glProgramUniform3uiv', None, UInt, Int, Int,
                         P(UInt))
glProgramUniform4i = E('glProgramUniform4i', None, UInt, Int, Int, Int, Int,
                       Int)
glProgramUniform4iv = E('glProgramUniform4iv', None, UInt, Int, Int, P(Int))
glProgramUniform4f = E('glProgramUniform4f', None, UInt, Int, Float, Float,
                       Float, Float)
glProgramUniform4fv = E('glProgramUniform4fv', None, UInt, Int, Int, P(Float))
glProgramUniform4d = E('glProgramUniform4d', None, UInt, Int, Double, Double,
                       Double, Double)
glProgramUniform4dv = E('glProgramUniform4dv', None, UInt, Int, Int,
                        P(Double))
glProgramUniform4ui = E('glProgramUniform4ui', None, UInt, Int, UInt, UInt,
                        UInt, UInt)
glProgramUniform4uiv = E('glProgramUniform4uiv', None, UInt, Int, Int,
                         P(UInt))
glProgramUniformMatrix2fv = E('glProgramUniformMatrix2fv', None, UInt, Int,
                              Int, UByte, P(Float))
glProgramUniformMatrix3fv = E('glProgramUniformMatrix3fv', None, UInt, Int,
                              Int, UByte, P(Float))
glProgramUniformMatrix4fv = E('glProgramUniformMatrix4fv', None, UInt, Int,
                              Int, UByte, P(Float))
glProgramUniformMatrix2dv = E('glProgramUniformMatrix2dv', None, UInt, Int,
                              Int, UByte, P(Double))
glProgramUniformMatrix3dv = E('glProgramUniformMatrix3dv', None, UInt, Int,
                              Int, UByte, P(Double))
glProgramUniformMatrix4dv = E('glProgramUniformMatrix4dv', None, UInt, Int,
                              Int, UByte, P(Double))
glProgramUniformMatrix2x3fv = E('glProgramUniformMatrix2x3fv', None, UInt,
                                Int, Int, UByte, P(Float))
glProgramUniformMatrix3x2fv = E('glProgramUniformMatrix3x2fv', None, UInt,
                                Int, Int, UByte, P(Float))
glProgramUniformMatrix2x4fv = E('glProgramUniformMatrix2x4fv', None, UInt,
                                Int, Int, UByte, P(Float))
glProgramUniformMatrix4x2fv = E('glProgramUniformMatrix4x2fv', None, UInt,
                                Int, Int, UByte, P(Float))
glProgramUniformMatrix3x4fv = E('glProgramUniformMatrix3x4fv', None, UInt,
                                Int, Int, UByte, P(Float))
glProgramUniformMatrix4x3fv = E('glProgramUniformMatrix4x3fv', None, UInt,
                                Int, Int, UByte, P(Float))
glProgramUniformMatrix2x3dv = E('glProgramUniformMatrix2x3dv', None, UInt,
                                Int, Int, UByte, P(Double))
glProgramUniformMatrix3x2dv = E('glProgramUniformMatrix3x2dv', None, UInt,
                                Int, Int, UByte, P(Double))
glProgramUniformMatrix2x4dv = E('glProgramUniformMatrix2x4dv', None, UInt,
                                Int, Int, UByte, P(Double))
glProgramUniformMatrix4x2dv = E('glProgramUniformMatrix4x2dv', None, UInt,
                                Int, Int, UByte, P(Double))
glProgramUniformMatrix3x4dv = E('glProgramUniformMatrix3x4dv', None, UInt,
                                Int, Int, UByte, P(Double))
glProgramUniformMatrix4x3dv = E('glProgramUniformMatrix4x3dv', None, UInt,
                                Int, Int, UByte, P(Double))
glValidateProgramPipeline = E('glValidateProgramPipeline', None, UInt)
glGetProgramPipelineInfoLog = E('glGetProgramPipelineInfoLog', None, UInt,
                                Int, P(Int), CharP)
glVertexAttribL1d = E('glVertexAttribL1d', None, UInt, Double)
glVertexAttribL2d = E('glVertexAttribL2d', None, UInt, Double, Double)
glVertexAttribL3d = E('glVertexAttribL3d', None, UInt, Double, Double, Double)
glVertexAttribL4d = E('glVertexAttribL4d', None, UInt, Double, Double, Double,
                      Double)
glVertexAttribL1dv = E('glVertexAttribL1dv', None, UInt, P(Double))
glVertexAttribL2dv = E('glVertexAttribL2dv', None, UInt, P(Double))
glVertexAttribL3dv = E('glVertexAttribL3dv', None, UInt, P(Double))
glVertexAttribL4dv = E('glVertexAttribL4dv', None, UInt, P(Double))
glVertexAttribLPointer = E('glVertexAttribLPointer', None, UInt, Int, UInt,
                           Int, VoidP)
glGetVertexAttribLdv = E('glGetVertexAttribLdv', None, UInt, UInt, P(Double))
glViewportArrayv = E('glViewportArrayv', None, UInt, Int, P(Float))
glViewportIndexedf = E('glViewportIndexedf', None, UInt, Float, Float, Float,
                       Float)
glViewportIndexedfv = E('glViewportIndexedfv', None, UInt, P(Float))
glScissorArrayv = E('glScissorArrayv', None, UInt, Int, P(Int))
glScissorIndexed = E('glScissorIndexed', None, UInt, Int, Int, Int, Int)
glScissorIndexedv = E('glScissorIndexedv', None, UInt, P(Int))
glDepthRangeArrayv = E('glDepthRangeArrayv', None, UInt, Int, P(Double))
glDepthRangeIndexed = E('glDepthRangeIndexed', None, UInt, Double, Double)
glGetFloati_v = E('glGetFloati_v', None, UInt, UInt, P(Float))
glGetDoublei_v = E('glGetDoublei_v', None, UInt, UInt, P(Double))

__all__ = [
    'GL_VERSION_4_1', 'GL_FIXED', 'GL_IMPLEMENTATION_COLOR_READ_TYPE',
    'GL_IMPLEMENTATION_COLOR_READ_FORMAT', 'GL_LOW_FLOAT', 'GL_MEDIUM_FLOAT',
    'GL_HIGH_FLOAT', 'GL_LOW_INT', 'GL_MEDIUM_INT', 'GL_HIGH_INT',
    'GL_SHADER_COMPILER', 'GL_SHADER_BINARY_FORMATS',
    'GL_NUM_SHADER_BINARY_FORMATS', 'GL_MAX_VERTEX_UNIFORM_VECTORS',
    'GL_MAX_VARYING_VECTORS', 'GL_MAX_FRAGMENT_UNIFORM_VECTORS', 'GL_RGB565',
    'GL_PROGRAM_BINARY_RETRIEVABLE_HINT', 'GL_PROGRAM_BINARY_LENGTH',
    'GL_NUM_PROGRAM_BINARY_FORMATS', 'GL_PROGRAM_BINARY_FORMATS',
    'GL_VERTEX_SHADER_BIT', 'GL_FRAGMENT_SHADER_BIT',
    'GL_GEOMETRY_SHADER_BIT', 'GL_TESS_CONTROL_SHADER_BIT',
    'GL_TESS_EVALUATION_SHADER_BIT', 'GL_ALL_SHADER_BITS',
    'GL_PROGRAM_SEPARABLE', 'GL_ACTIVE_PROGRAM',
    'GL_PROGRAM_PIPELINE_BINDING', 'GL_MAX_VIEWPORTS',
    'GL_VIEWPORT_SUBPIXEL_BITS', 'GL_VIEWPORT_BOUNDS_RANGE',
    'GL_LAYER_PROVOKING_VERTEX', 'GL_VIEWPORT_INDEX_PROVOKING_VERTEX',
    'GL_UNDEFINED_VERTEX', 'PFNGLRELEASESHADERCOMPILERPROC',
    'PFNGLSHADERBINARYPROC', 'PFNGLGETSHADERPRECISIONFORMATPROC',
    'PFNGLDEPTHRANGEFPROC', 'PFNGLCLEARDEPTHFPROC',
    'PFNGLGETPROGRAMBINARYPROC', 'PFNGLPROGRAMBINARYPROC',
    'PFNGLPROGRAMPARAMETERIPROC', 'PFNGLUSEPROGRAMSTAGESPROC',
    'PFNGLACTIVESHADERPROGRAMPROC', 'PFNGLCREATESHADERPROGRAMVPROC',
    'PFNGLBINDPROGRAMPIPELINEPROC', 'PFNGLDELETEPROGRAMPIPELINESPROC',
    'PFNGLGENPROGRAMPIPELINESPROC', 'PFNGLISPROGRAMPIPELINEPROC',
    'PFNGLGETPROGRAMPIPELINEIVPROC', 'PFNGLPROGRAMUNIFORM1IPROC',
    'PFNGLPROGRAMUNIFORM1IVPROC', 'PFNGLPROGRAMUNIFORM1FPROC',
    'PFNGLPROGRAMUNIFORM1FVPROC', 'PFNGLPROGRAMUNIFORM1DPROC',
    'PFNGLPROGRAMUNIFORM1DVPROC', 'PFNGLPROGRAMUNIFORM1UIPROC',
    'PFNGLPROGRAMUNIFORM1UIVPROC', 'PFNGLPROGRAMUNIFORM2IPROC',
    'PFNGLPROGRAMUNIFORM2IVPROC', 'PFNGLPROGRAMUNIFORM2FPROC',
    'PFNGLPROGRAMUNIFORM2FVPROC', 'PFNGLPROGRAMUNIFORM2DPROC',
    'PFNGLPROGRAMUNIFORM2DVPROC', 'PFNGLPROGRAMUNIFORM2UIPROC',
    'PFNGLPROGRAMUNIFORM2UIVPROC', 'PFNGLPROGRAMUNIFORM3IPROC',
    'PFNGLPROGRAMUNIFORM3IVPROC', 'PFNGLPROGRAMUNIFORM3FPROC',
    'PFNGLPROGRAMUNIFORM3FVPROC', 'PFNGLPROGRAMUNIFORM3DPROC',
    'PFNGLPROGRAMUNIFORM3DVPROC', 'PFNGLPROGRAMUNIFORM3UIPROC',
    'PFNGLPROGRAMUNIFORM3UIVPROC', 'PFNGLPROGRAMUNIFORM4IPROC',
    'PFNGLPROGRAMUNIFORM4IVPROC', 'PFNGLPROGRAMUNIFORM4FPROC',
    'PFNGLPROGRAMUNIFORM4FVPROC', 'PFNGLPROGRAMUNIFORM4DPROC',
    'PFNGLPROGRAMUNIFORM4DVPROC', 'PFNGLPROGRAMUNIFORM4UIPROC',
    'PFNGLPROGRAMUNIFORM4UIVPROC', 'PFNGLPROGRAMUNIFORMMATRIX2FVPROC',
    'PFNGLPROGRAMUNIFORMMATRIX3FVPROC', 'PFNGLPROGRAMUNIFORMMATRIX4FVPROC',
    'PFNGLPROGRAMUNIFORMMATRIX2DVPROC', 'PFNGLPROGRAMUNIFORMMATRIX3DVPROC',
    'PFNGLPROGRAMUNIFORMMATRIX4DVPROC', 'PFNGLPROGRAMUNIFORMMATRIX2X3FVPROC',
    'PFNGLPROGRAMUNIFORMMATRIX3X2FVPROC',
    'PFNGLPROGRAMUNIFORMMATRIX2X4FVPROC',
    'PFNGLPROGRAMUNIFORMMATRIX4X2FVPROC',
    'PFNGLPROGRAMUNIFORMMATRIX3X4FVPROC',
    'PFNGLPROGRAMUNIFORMMATRIX4X3FVPROC',
    'PFNGLPROGRAMUNIFORMMATRIX2X3DVPROC',
    'PFNGLPROGRAMUNIFORMMATRIX3X2DVPROC',
    'PFNGLPROGRAMUNIFORMMATRIX2X4DVPROC',
    'PFNGLPROGRAMUNIFORMMATRIX4X2DVPROC',
    'PFNGLPROGRAMUNIFORMMATRIX3X4DVPROC',
    'PFNGLPROGRAMUNIFORMMATRIX4X3DVPROC', 'PFNGLVALIDATEPROGRAMPIPELINEPROC',
    'PFNGLGETPROGRAMPIPELINEINFOLOGPROC', 'PFNGLVERTEXATTRIBL1DPROC',
    'PFNGLVERTEXATTRIBL2DPROC', 'PFNGLVERTEXATTRIBL3DPROC',
    'PFNGLVERTEXATTRIBL4DPROC', 'PFNGLVERTEXATTRIBL1DVPROC',
    'PFNGLVERTEXATTRIBL2DVPROC', 'PFNGLVERTEXATTRIBL3DVPROC',
    'PFNGLVERTEXATTRIBL4DVPROC', 'PFNGLVERTEXATTRIBLPOINTERPROC',
    'PFNGLGETVERTEXATTRIBLDVPROC', 'PFNGLVIEWPORTARRAYVPROC',
    'PFNGLVIEWPORTINDEXEDFPROC', 'PFNGLVIEWPORTINDEXEDFVPROC',
    'PFNGLSCISSORARRAYVPROC', 'PFNGLSCISSORINDEXEDPROC',
    'PFNGLSCISSORINDEXEDVPROC', 'PFNGLDEPTHRANGEARRAYVPROC',
    'PFNGLDEPTHRANGEINDEXEDPROC', 'PFNGLGETFLOATI_VPROC',
    'PFNGLGETDOUBLEI_VPROC', 'glReleaseShaderCompiler', 'glShaderBinary',
    'glGetShaderPrecisionFormat', 'glDepthRangef', 'glClearDepthf',
    'glGetProgramBinary', 'glProgramBinary', 'glProgramParameteri',
    'glUseProgramStages', 'glActiveShaderProgram', 'glCreateShaderProgramv',
    'glBindProgramPipeline', 'glDeleteProgramPipelines',
    'glGenProgramPipelines', 'glIsProgramPipeline', 'glGetProgramPipelineiv',
    'glProgramUniform1i', 'glProgramUniform1iv', 'glProgramUniform1f',
    'glProgramUniform1fv', 'glProgramUniform1d', 'glProgramUniform1dv',
    'glProgramUniform1ui', 'glProgramUniform1uiv', 'glProgramUniform2i',
    'glProgramUniform2iv', 'glProgramUniform2f', 'glProgramUniform2fv',
    'glProgramUniform2d', 'glProgramUniform2dv', 'glProgramUniform2ui',
    'glProgramUniform2uiv', 'glProgramUniform3i', 'glProgramUniform3iv',
    'glProgramUniform3f', 'glProgramUniform3fv', 'glProgramUniform3d',
    'glProgramUniform3dv', 'glProgramUniform3ui', 'glProgramUniform3uiv',
    'glProgramUniform4i', 'glProgramUniform4iv', 'glProgramUniform4f',
    'glProgramUniform4fv', 'glProgramUniform4d', 'glProgramUniform4dv',
    'glProgramUniform4ui', 'glProgramUniform4uiv',
    'glProgramUniformMatrix2fv', 'glProgramUniformMatrix3fv',
    'glProgramUniformMatrix4fv', 'glProgramUniformMatrix2dv',
    'glProgramUniformMatrix3dv', 'glProgramUniformMatrix4dv',
    'glProgramUniformMatrix2x3fv', 'glProgramUniformMatrix3x2fv',
    'glProgramUniformMatrix2x4fv', 'glProgramUniformMatrix4x2fv',
    'glProgramUniformMatrix3x4fv', 'glProgramUniformMatrix4x3fv',
    'glProgramUniformMatrix2x3dv', 'glProgramUniformMatrix3x2dv',
    'glProgramUniformMatrix2x4dv', 'glProgramUniformMatrix4x2dv',
    'glProgramUniformMatrix3x4dv', 'glProgramUniformMatrix4x3dv',
    'glValidateProgramPipeline', 'glGetProgramPipelineInfoLog',
    'glVertexAttribL1d', 'glVertexAttribL2d', 'glVertexAttribL3d',
    'glVertexAttribL4d', 'glVertexAttribL1dv', 'glVertexAttribL2dv',
    'glVertexAttribL3dv', 'glVertexAttribL4dv', 'glVertexAttribLPointer',
    'glGetVertexAttribLdv', 'glViewportArrayv', 'glViewportIndexedf',
    'glViewportIndexedfv', 'glScissorArrayv', 'glScissorIndexed',
    'glScissorIndexedv', 'glDepthRangeArrayv', 'glDepthRangeIndexed',
    'glGetFloati_v', 'glGetDoublei_v'
]
