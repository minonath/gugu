from .auto_wrap import *

GL_VERSION_2_0 = 1
GL_BLEND_EQUATION_RGB = 0x8009
GL_VERTEX_ATTRIB_ARRAY_ENABLED = 0x8622
GL_VERTEX_ATTRIB_ARRAY_SIZE = 0x8623
GL_VERTEX_ATTRIB_ARRAY_STRIDE = 0x8624
GL_VERTEX_ATTRIB_ARRAY_TYPE = 0x8625
GL_CURRENT_VERTEX_ATTRIB = 0x8626
GL_VERTEX_PROGRAM_POINT_SIZE = 0x8642
GL_VERTEX_ATTRIB_ARRAY_POINTER = 0x8645
GL_STENCIL_BACK_FUNC = 0x8800
GL_STENCIL_BACK_FAIL = 0x8801
GL_STENCIL_BACK_PASS_DEPTH_FAIL = 0x8802
GL_STENCIL_BACK_PASS_DEPTH_PASS = 0x8803
GL_MAX_DRAW_BUFFERS = 0x8824
GL_DRAW_BUFFER0 = 0x8825
GL_DRAW_BUFFER1 = 0x8826
GL_DRAW_BUFFER2 = 0x8827
GL_DRAW_BUFFER3 = 0x8828
GL_DRAW_BUFFER4 = 0x8829
GL_DRAW_BUFFER5 = 0x882A
GL_DRAW_BUFFER6 = 0x882B
GL_DRAW_BUFFER7 = 0x882C
GL_DRAW_BUFFER8 = 0x882D
GL_DRAW_BUFFER9 = 0x882E
GL_DRAW_BUFFER10 = 0x882F
GL_DRAW_BUFFER11 = 0x8830
GL_DRAW_BUFFER12 = 0x8831
GL_DRAW_BUFFER13 = 0x8832
GL_DRAW_BUFFER14 = 0x8833
GL_DRAW_BUFFER15 = 0x8834
GL_BLEND_EQUATION_ALPHA = 0x883D
GL_MAX_VERTEX_ATTRIBS = 0x8869
GL_VERTEX_ATTRIB_ARRAY_NORMALIZED = 0x886A
GL_MAX_TEXTURE_IMAGE_UNITS = 0x8872
GL_FRAGMENT_SHADER = 0x8B30
GL_VERTEX_SHADER = 0x8B31
GL_MAX_FRAGMENT_UNIFORM_COMPONENTS = 0x8B49
GL_MAX_VERTEX_UNIFORM_COMPONENTS = 0x8B4A
GL_MAX_VARYING_FLOATS = 0x8B4B
GL_MAX_VERTEX_TEXTURE_IMAGE_UNITS = 0x8B4C
GL_MAX_COMBINED_TEXTURE_IMAGE_UNITS = 0x8B4D
GL_SHADER_TYPE = 0x8B4F
GL_FLOAT_VEC2 = 0x8B50
GL_FLOAT_VEC3 = 0x8B51
GL_FLOAT_VEC4 = 0x8B52
GL_INT_VEC2 = 0x8B53
GL_INT_VEC3 = 0x8B54
GL_INT_VEC4 = 0x8B55
GL_BOOL = 0x8B56
GL_BOOL_VEC2 = 0x8B57
GL_BOOL_VEC3 = 0x8B58
GL_BOOL_VEC4 = 0x8B59
GL_FLOAT_MAT2 = 0x8B5A
GL_FLOAT_MAT3 = 0x8B5B
GL_FLOAT_MAT4 = 0x8B5C
GL_SAMPLER_1D = 0x8B5D
GL_SAMPLER_2D = 0x8B5E
GL_SAMPLER_3D = 0x8B5F
GL_SAMPLER_CUBE = 0x8B60
GL_SAMPLER_1D_SHADOW = 0x8B61
GL_SAMPLER_2D_SHADOW = 0x8B62
GL_DELETE_STATUS = 0x8B80
GL_COMPILE_STATUS = 0x8B81
GL_LINK_STATUS = 0x8B82
GL_VALIDATE_STATUS = 0x8B83
GL_INFO_LOG_LENGTH = 0x8B84
GL_ATTACHED_SHADERS = 0x8B85
GL_ACTIVE_UNIFORMS = 0x8B86
GL_ACTIVE_UNIFORM_MAX_LENGTH = 0x8B87
GL_SHADER_SOURCE_LENGTH = 0x8B88
GL_ACTIVE_ATTRIBUTES = 0x8B89
GL_ACTIVE_ATTRIBUTE_MAX_LENGTH = 0x8B8A
GL_FRAGMENT_SHADER_DERIVATIVE_HINT = 0x8B8B
GL_SHADING_LANGUAGE_VERSION = 0x8B8C
GL_CURRENT_PROGRAM = 0x8B8D
GL_POINT_SPRITE_COORD_ORIGIN = 0x8CA0
GL_LOWER_LEFT = 0x8CA1
GL_UPPER_LEFT = 0x8CA2
GL_STENCIL_BACK_REF = 0x8CA3
GL_STENCIL_BACK_VALUE_MASK = 0x8CA4
GL_STENCIL_BACK_WRITEMASK = 0x8CA5
PFNGLBLENDEQUATIONSEPARATEPROC = C(None, UInt, UInt)
PFNGLDRAWBUFFERSPROC = C(None, Int, P(UInt))
PFNGLSTENCILOPSEPARATEPROC = C(None, UInt, UInt, UInt, UInt)
PFNGLSTENCILFUNCSEPARATEPROC = C(None, UInt, UInt, Int, UInt)
PFNGLSTENCILMASKSEPARATEPROC = C(None, UInt, UInt)
PFNGLATTACHSHADERPROC = C(None, UInt, UInt)
PFNGLBINDATTRIBLOCATIONPROC = C(None, UInt, UInt, CharP)
PFNGLCOMPILESHADERPROC = C(None, UInt)
PFNGLCREATEPROGRAMPROC = C(UInt)
PFNGLCREATESHADERPROC = C(UInt, UInt)
PFNGLDELETEPROGRAMPROC = C(None, UInt)
PFNGLDELETESHADERPROC = C(None, UInt)
PFNGLDETACHSHADERPROC = C(None, UInt, UInt)
PFNGLDISABLEVERTEXATTRIBARRAYPROC = C(None, UInt)
PFNGLENABLEVERTEXATTRIBARRAYPROC = C(None, UInt)
PFNGLGETACTIVEATTRIBPROC = C(
    None, UInt, UInt, Int, P(Int), P(Int), P(UInt), CharP)
PFNGLGETACTIVEUNIFORMPROC = C(
    None, UInt, UInt, Int, P(Int), P(Int), P(UInt), CharP)
PFNGLGETATTACHEDSHADERSPROC = C(None, UInt, Int, P(Int), P(UInt))
PFNGLGETATTRIBLOCATIONPROC = C(Int, UInt, CharP)
PFNGLGETPROGRAMIVPROC = C(None, UInt, UInt, P(Int))
PFNGLGETPROGRAMINFOLOGPROC = C(None, UInt, Int, P(Int), CharP)
PFNGLGETSHADERIVPROC = C(None, UInt, UInt, P(Int))
PFNGLGETSHADERINFOLOGPROC = C(None, UInt, Int, P(Int), CharP)
PFNGLGETSHADERSOURCEPROC = C(None, UInt, Int, P(Int), CharP)
PFNGLGETUNIFORMLOCATIONPROC = C(Int, UInt, CharP)
PFNGLGETUNIFORMFVPROC = C(None, UInt, Int, P(Float))
PFNGLGETUNIFORMIVPROC = C(None, UInt, Int, P(Int))
PFNGLGETVERTEXATTRIBDVPROC = C(None, UInt, UInt, P(Double))
PFNGLGETVERTEXATTRIBFVPROC = C(None, UInt, UInt, P(Float))
PFNGLGETVERTEXATTRIBIVPROC = C(None, UInt, UInt, P(Int))
PFNGLGETVERTEXATTRIBPOINTERVPROC = C(None, UInt, UInt, P(VoidP))
PFNGLISPROGRAMPROC = C(UByte, UInt)
PFNGLISSHADERPROC = C(UByte, UInt)
PFNGLLINKPROGRAMPROC = C(None, UInt)
PFNGLSHADERSOURCEPROC = C(None, UInt, Int, P(CharP), P(Int))
PFNGLUSEPROGRAMPROC = C(None, UInt)
PFNGLUNIFORM1FPROC = C(None, Int, Float)
PFNGLUNIFORM2FPROC = C(None, Int, Float, Float)
PFNGLUNIFORM3FPROC = C(None, Int, Float, Float, Float)
PFNGLUNIFORM4FPROC = C(None, Int, Float, Float, Float, Float)
PFNGLUNIFORM1IPROC = C(None, Int, Int)
PFNGLUNIFORM2IPROC = C(None, Int, Int, Int)
PFNGLUNIFORM3IPROC = C(None, Int, Int, Int, Int)
PFNGLUNIFORM4IPROC = C(None, Int, Int, Int, Int, Int)
PFNGLUNIFORM1FVPROC = C(None, Int, Int, P(Float))
PFNGLUNIFORM2FVPROC = C(None, Int, Int, P(Float))
PFNGLUNIFORM3FVPROC = C(None, Int, Int, P(Float))
PFNGLUNIFORM4FVPROC = C(None, Int, Int, P(Float))
PFNGLUNIFORM1IVPROC = C(None, Int, Int, P(Int))
PFNGLUNIFORM2IVPROC = C(None, Int, Int, P(Int))
PFNGLUNIFORM3IVPROC = C(None, Int, Int, P(Int))
PFNGLUNIFORM4IVPROC = C(None, Int, Int, P(Int))
PFNGLUNIFORMMATRIX2FVPROC = C(None, Int, Int, UByte, P(Float))
PFNGLUNIFORMMATRIX3FVPROC = C(None, Int, Int, UByte, P(Float))
PFNGLUNIFORMMATRIX4FVPROC = C(None, Int, Int, UByte, P(Float))
PFNGLVALIDATEPROGRAMPROC = C(None, UInt)
PFNGLVERTEXATTRIB1DPROC = C(None, UInt, Double)
PFNGLVERTEXATTRIB1DVPROC = C(None, UInt, P(Double))
PFNGLVERTEXATTRIB1FPROC = C(None, UInt, Float)
PFNGLVERTEXATTRIB1FVPROC = C(None, UInt, P(Float))
PFNGLVERTEXATTRIB1SPROC = C(None, UInt, Short)
PFNGLVERTEXATTRIB1SVPROC = C(None, UInt, P(Short))
PFNGLVERTEXATTRIB2DPROC = C(None, UInt, Double, Double)
PFNGLVERTEXATTRIB2DVPROC = C(None, UInt, P(Double))
PFNGLVERTEXATTRIB2FPROC = C(None, UInt, Float, Float)
PFNGLVERTEXATTRIB2FVPROC = C(None, UInt, P(Float))
PFNGLVERTEXATTRIB2SPROC = C(None, UInt, Short, Short)
PFNGLVERTEXATTRIB2SVPROC = C(None, UInt, P(Short))
PFNGLVERTEXATTRIB3DPROC = C(None, UInt, Double, Double, Double)
PFNGLVERTEXATTRIB3DVPROC = C(None, UInt, P(Double))
PFNGLVERTEXATTRIB3FPROC = C(None, UInt, Float, Float, Float)
PFNGLVERTEXATTRIB3FVPROC = C(None, UInt, P(Float))
PFNGLVERTEXATTRIB3SPROC = C(None, UInt, Short, Short, Short)
PFNGLVERTEXATTRIB3SVPROC = C(None, UInt, P(Short))
PFNGLVERTEXATTRIB4NBVPROC = C(None, UInt, P(Byte))
PFNGLVERTEXATTRIB4NIVPROC = C(None, UInt, P(Int))
PFNGLVERTEXATTRIB4NSVPROC = C(None, UInt, P(Short))
PFNGLVERTEXATTRIB4NUBPROC = C(None, UInt, UByte, UByte, UByte, UByte)
PFNGLVERTEXATTRIB4NUBVPROC = C(None, UInt, P(UByte))
PFNGLVERTEXATTRIB4NUIVPROC = C(None, UInt, P(UInt))
PFNGLVERTEXATTRIB4NUSVPROC = C(None, UInt, P(UShort))
PFNGLVERTEXATTRIB4BVPROC = C(None, UInt, P(Byte))
PFNGLVERTEXATTRIB4DPROC = C(None, UInt, Double, Double, Double, Double)
PFNGLVERTEXATTRIB4DVPROC = C(None, UInt, P(Double))
PFNGLVERTEXATTRIB4FPROC = C(None, UInt, Float, Float, Float, Float)
PFNGLVERTEXATTRIB4FVPROC = C(None, UInt, P(Float))
PFNGLVERTEXATTRIB4IVPROC = C(None, UInt, P(Int))
PFNGLVERTEXATTRIB4SPROC = C(None, UInt, Short, Short, Short, Short)
PFNGLVERTEXATTRIB4SVPROC = C(None, UInt, P(Short))
PFNGLVERTEXATTRIB4UBVPROC = C(None, UInt, P(UByte))
PFNGLVERTEXATTRIB4UIVPROC = C(None, UInt, P(UInt))
PFNGLVERTEXATTRIB4USVPROC = C(None, UInt, P(UShort))
PFNGLVERTEXATTRIBPOINTERPROC = C(None, UInt, Int, UInt, UByte, Int, VoidP)
glBlendEquationSeparate = E('glBlendEquationSeparate', None, UInt, UInt)
glDrawBuffers = E('glDrawBuffers', None, Int, P(UInt))
glStencilOpSeparate = E('glStencilOpSeparate', None, UInt, UInt, UInt, UInt)
glStencilFuncSeparate = E(
    'glStencilFuncSeparate', None, UInt, UInt, Int, UInt)
glStencilMaskSeparate = E('glStencilMaskSeparate', None, UInt, UInt)
glAttachShader = E('glAttachShader', None, UInt, UInt)
glBindAttribLocation = E('glBindAttribLocation', None, UInt, UInt, CharP)
glCompileShader = E('glCompileShader', None, UInt)
glCreateProgram = E('glCreateProgram', UInt)
glCreateShader = E('glCreateShader', UInt, UInt)
glDeleteProgram = E('glDeleteProgram', None, UInt)
glDeleteShader = E('glDeleteShader', None, UInt)
glDetachShader = E('glDetachShader', None, UInt, UInt)
glDisableVertexAttribArray = E('glDisableVertexAttribArray', None, UInt)
glEnableVertexAttribArray = E('glEnableVertexAttribArray', None, UInt)
glGetActiveAttrib = E('glGetActiveAttrib', None, UInt, UInt, Int, P(Int),
                      P(Int), P(UInt), CharP)
glGetActiveUniform = E('glGetActiveUniform', None, UInt, UInt, Int, P(Int),
                       P(Int), P(UInt), CharP)
glGetAttachedShaders = E(
    'glGetAttachedShaders', None, UInt, Int, P(Int), P(UInt))
glGetAttribLocation = E('glGetAttribLocation', Int, UInt, CharP)
glGetProgramiv = E('glGetProgramiv', None, UInt, UInt, P(Int))
glGetProgramInfoLog = E('glGetProgramInfoLog', None, UInt, Int, P(Int), CharP)
glGetShaderiv = E('glGetShaderiv', None, UInt, UInt, P(Int))
glGetShaderInfoLog = E('glGetShaderInfoLog', None, UInt, Int, P(Int), CharP)
glGetShaderSource = E('glGetShaderSource', None, UInt, Int, P(Int), CharP)
glGetUniformLocation = E('glGetUniformLocation', Int, UInt, CharP)
glGetUniformfv = E('glGetUniformfv', None, UInt, Int, P(Float))
glGetUniformiv = E('glGetUniformiv', None, UInt, Int, P(Int))
glGetVertexAttribdv = E('glGetVertexAttribdv', None, UInt, UInt, P(Double))
glGetVertexAttribfv = E('glGetVertexAttribfv', None, UInt, UInt, P(Float))
glGetVertexAttribiv = E('glGetVertexAttribiv', None, UInt, UInt, P(Int))
glGetVertexAttribPointerv = E(
    'glGetVertexAttribPointerv', None, UInt, UInt, P(VoidP))
glIsProgram = E('glIsProgram', UByte, UInt)
glIsShader = E('glIsShader', UByte, UInt)
glLinkProgram = E('glLinkProgram', None, UInt)
glShaderSource = E('glShaderSource', None, UInt, Int, P(CharP), P(Int))
glUseProgram = E('glUseProgram', None, UInt)
glUniform1f = E('glUniform1f', None, Int, Float)
glUniform2f = E('glUniform2f', None, Int, Float, Float)
glUniform3f = E('glUniform3f', None, Int, Float, Float, Float)
glUniform4f = E('glUniform4f', None, Int, Float, Float, Float, Float)
glUniform1i = E('glUniform1i', None, Int, Int)
glUniform2i = E('glUniform2i', None, Int, Int, Int)
glUniform3i = E('glUniform3i', None, Int, Int, Int, Int)
glUniform4i = E('glUniform4i', None, Int, Int, Int, Int, Int)
glUniform1fv = E('glUniform1fv', None, Int, Int, P(Float))
glUniform2fv = E('glUniform2fv', None, Int, Int, P(Float))
glUniform3fv = E('glUniform3fv', None, Int, Int, P(Float))
glUniform4fv = E('glUniform4fv', None, Int, Int, P(Float))
glUniform1iv = E('glUniform1iv', None, Int, Int, P(Int))
glUniform2iv = E('glUniform2iv', None, Int, Int, P(Int))
glUniform3iv = E('glUniform3iv', None, Int, Int, P(Int))
glUniform4iv = E('glUniform4iv', None, Int, Int, P(Int))
glUniformMatrix2fv = E('glUniformMatrix2fv', None, Int, Int, UByte, P(Float))
glUniformMatrix3fv = E('glUniformMatrix3fv', None, Int, Int, UByte, P(Float))
glUniformMatrix4fv = E('glUniformMatrix4fv', None, Int, Int, UByte, P(Float))
glValidateProgram = E('glValidateProgram', None, UInt)
glVertexAttrib1d = E('glVertexAttrib1d', None, UInt, Double)
glVertexAttrib1dv = E('glVertexAttrib1dv', None, UInt, P(Double))
glVertexAttrib1f = E('glVertexAttrib1f', None, UInt, Float)
glVertexAttrib1fv = E('glVertexAttrib1fv', None, UInt, P(Float))
glVertexAttrib1s = E('glVertexAttrib1s', None, UInt, Short)
glVertexAttrib1sv = E('glVertexAttrib1sv', None, UInt, P(Short))
glVertexAttrib2d = E('glVertexAttrib2d', None, UInt, Double, Double)
glVertexAttrib2dv = E('glVertexAttrib2dv', None, UInt, P(Double))
glVertexAttrib2f = E('glVertexAttrib2f', None, UInt, Float, Float)
glVertexAttrib2fv = E('glVertexAttrib2fv', None, UInt, P(Float))
glVertexAttrib2s = E('glVertexAttrib2s', None, UInt, Short, Short)
glVertexAttrib2sv = E('glVertexAttrib2sv', None, UInt, P(Short))
glVertexAttrib3d = E('glVertexAttrib3d', None, UInt, Double, Double, Double)
glVertexAttrib3dv = E('glVertexAttrib3dv', None, UInt, P(Double))
glVertexAttrib3f = E('glVertexAttrib3f', None, UInt, Float, Float, Float)
glVertexAttrib3fv = E('glVertexAttrib3fv', None, UInt, P(Float))
glVertexAttrib3s = E('glVertexAttrib3s', None, UInt, Short, Short, Short)
glVertexAttrib3sv = E('glVertexAttrib3sv', None, UInt, P(Short))
glVertexAttrib4Nbv = E('glVertexAttrib4Nbv', None, UInt, P(Byte))
glVertexAttrib4Niv = E('glVertexAttrib4Niv', None, UInt, P(Int))
glVertexAttrib4Nsv = E('glVertexAttrib4Nsv', None, UInt, P(Short))
glVertexAttrib4Nub = E(
    'glVertexAttrib4Nub', None, UInt, UByte, UByte, UByte, UByte)
glVertexAttrib4Nubv = E('glVertexAttrib4Nubv', None, UInt, P(UByte))
glVertexAttrib4Nuiv = E('glVertexAttrib4Nuiv', None, UInt, P(UInt))
glVertexAttrib4Nusv = E('glVertexAttrib4Nusv', None, UInt, P(UShort))
glVertexAttrib4bv = E('glVertexAttrib4bv', None, UInt, P(Byte))
glVertexAttrib4d = E(
    'glVertexAttrib4d', None, UInt, Double, Double, Double, Double)
glVertexAttrib4dv = E('glVertexAttrib4dv', None, UInt, P(Double))
glVertexAttrib4f = E(
    'glVertexAttrib4f', None, UInt, Float, Float, Float, Float)
glVertexAttrib4fv = E('glVertexAttrib4fv', None, UInt, P(Float))
glVertexAttrib4iv = E('glVertexAttrib4iv', None, UInt, P(Int))
glVertexAttrib4s = E(
    'glVertexAttrib4s', None, UInt, Short, Short, Short, Short)
glVertexAttrib4sv = E('glVertexAttrib4sv', None, UInt, P(Short))
glVertexAttrib4ubv = E('glVertexAttrib4ubv', None, UInt, P(UByte))
glVertexAttrib4uiv = E('glVertexAttrib4uiv', None, UInt, P(UInt))
glVertexAttrib4usv = E('glVertexAttrib4usv', None, UInt, P(UShort))
glVertexAttribPointer = E(
    'glVertexAttribPointer', None, UInt, Int, UInt, UByte, Int, VoidP)

__all__ = [
    'GL_VERSION_2_0', 'GL_BLEND_EQUATION_RGB',
    'GL_VERTEX_ATTRIB_ARRAY_ENABLED', 'GL_VERTEX_ATTRIB_ARRAY_SIZE',
    'GL_VERTEX_ATTRIB_ARRAY_STRIDE', 'GL_VERTEX_ATTRIB_ARRAY_TYPE',
    'GL_CURRENT_VERTEX_ATTRIB', 'GL_VERTEX_PROGRAM_POINT_SIZE',
    'GL_VERTEX_ATTRIB_ARRAY_POINTER', 'GL_STENCIL_BACK_FUNC',
    'GL_STENCIL_BACK_FAIL', 'GL_STENCIL_BACK_PASS_DEPTH_FAIL',
    'GL_STENCIL_BACK_PASS_DEPTH_PASS', 'GL_MAX_DRAW_BUFFERS',
    'GL_DRAW_BUFFER0', 'GL_DRAW_BUFFER1', 'GL_DRAW_BUFFER2',
    'GL_DRAW_BUFFER3', 'GL_DRAW_BUFFER4', 'GL_DRAW_BUFFER5',
    'GL_DRAW_BUFFER6', 'GL_DRAW_BUFFER7', 'GL_DRAW_BUFFER8',
    'GL_DRAW_BUFFER9', 'GL_DRAW_BUFFER10', 'GL_DRAW_BUFFER11',
    'GL_DRAW_BUFFER12', 'GL_DRAW_BUFFER13', 'GL_DRAW_BUFFER14',
    'GL_DRAW_BUFFER15', 'GL_BLEND_EQUATION_ALPHA', 'GL_MAX_VERTEX_ATTRIBS',
    'GL_VERTEX_ATTRIB_ARRAY_NORMALIZED', 'GL_MAX_TEXTURE_IMAGE_UNITS',
    'GL_FRAGMENT_SHADER', 'GL_VERTEX_SHADER',
    'GL_MAX_FRAGMENT_UNIFORM_COMPONENTS', 'GL_MAX_VERTEX_UNIFORM_COMPONENTS',
    'GL_MAX_VARYING_FLOATS', 'GL_MAX_VERTEX_TEXTURE_IMAGE_UNITS',
    'GL_MAX_COMBINED_TEXTURE_IMAGE_UNITS', 'GL_SHADER_TYPE', 'GL_FLOAT_VEC2',
    'GL_FLOAT_VEC3', 'GL_FLOAT_VEC4', 'GL_INT_VEC2', 'GL_INT_VEC3',
    'GL_INT_VEC4', 'GL_BOOL', 'GL_BOOL_VEC2', 'GL_BOOL_VEC3', 'GL_BOOL_VEC4',
    'GL_FLOAT_MAT2', 'GL_FLOAT_MAT3', 'GL_FLOAT_MAT4', 'GL_SAMPLER_1D',
    'GL_SAMPLER_2D', 'GL_SAMPLER_3D', 'GL_SAMPLER_CUBE',
    'GL_SAMPLER_1D_SHADOW', 'GL_SAMPLER_2D_SHADOW', 'GL_DELETE_STATUS',
    'GL_COMPILE_STATUS', 'GL_LINK_STATUS', 'GL_VALIDATE_STATUS',
    'GL_INFO_LOG_LENGTH', 'GL_ATTACHED_SHADERS', 'GL_ACTIVE_UNIFORMS',
    'GL_ACTIVE_UNIFORM_MAX_LENGTH', 'GL_SHADER_SOURCE_LENGTH',
    'GL_ACTIVE_ATTRIBUTES', 'GL_ACTIVE_ATTRIBUTE_MAX_LENGTH',
    'GL_FRAGMENT_SHADER_DERIVATIVE_HINT', 'GL_SHADING_LANGUAGE_VERSION',
    'GL_CURRENT_PROGRAM', 'GL_POINT_SPRITE_COORD_ORIGIN', 'GL_LOWER_LEFT',
    'GL_UPPER_LEFT', 'GL_STENCIL_BACK_REF', 'GL_STENCIL_BACK_VALUE_MASK',
    'GL_STENCIL_BACK_WRITEMASK', 'PFNGLBLENDEQUATIONSEPARATEPROC',
    'PFNGLDRAWBUFFERSPROC', 'PFNGLSTENCILOPSEPARATEPROC',
    'PFNGLSTENCILFUNCSEPARATEPROC', 'PFNGLSTENCILMASKSEPARATEPROC',
    'PFNGLATTACHSHADERPROC', 'PFNGLBINDATTRIBLOCATIONPROC',
    'PFNGLCOMPILESHADERPROC', 'PFNGLCREATEPROGRAMPROC',
    'PFNGLCREATESHADERPROC', 'PFNGLDELETEPROGRAMPROC',
    'PFNGLDELETESHADERPROC', 'PFNGLDETACHSHADERPROC',
    'PFNGLDISABLEVERTEXATTRIBARRAYPROC', 'PFNGLENABLEVERTEXATTRIBARRAYPROC',
    'PFNGLGETACTIVEATTRIBPROC', 'PFNGLGETACTIVEUNIFORMPROC',
    'PFNGLGETATTACHEDSHADERSPROC', 'PFNGLGETATTRIBLOCATIONPROC',
    'PFNGLGETPROGRAMIVPROC', 'PFNGLGETPROGRAMINFOLOGPROC',
    'PFNGLGETSHADERIVPROC', 'PFNGLGETSHADERINFOLOGPROC',
    'PFNGLGETSHADERSOURCEPROC', 'PFNGLGETUNIFORMLOCATIONPROC',
    'PFNGLGETUNIFORMFVPROC', 'PFNGLGETUNIFORMIVPROC',
    'PFNGLGETVERTEXATTRIBDVPROC', 'PFNGLGETVERTEXATTRIBFVPROC',
    'PFNGLGETVERTEXATTRIBIVPROC', 'PFNGLGETVERTEXATTRIBPOINTERVPROC',
    'PFNGLISPROGRAMPROC', 'PFNGLISSHADERPROC', 'PFNGLLINKPROGRAMPROC',
    'PFNGLSHADERSOURCEPROC', 'PFNGLUSEPROGRAMPROC', 'PFNGLUNIFORM1FPROC',
    'PFNGLUNIFORM2FPROC', 'PFNGLUNIFORM3FPROC', 'PFNGLUNIFORM4FPROC',
    'PFNGLUNIFORM1IPROC', 'PFNGLUNIFORM2IPROC', 'PFNGLUNIFORM3IPROC',
    'PFNGLUNIFORM4IPROC', 'PFNGLUNIFORM1FVPROC', 'PFNGLUNIFORM2FVPROC',
    'PFNGLUNIFORM3FVPROC', 'PFNGLUNIFORM4FVPROC', 'PFNGLUNIFORM1IVPROC',
    'PFNGLUNIFORM2IVPROC', 'PFNGLUNIFORM3IVPROC', 'PFNGLUNIFORM4IVPROC',
    'PFNGLUNIFORMMATRIX2FVPROC', 'PFNGLUNIFORMMATRIX3FVPROC',
    'PFNGLUNIFORMMATRIX4FVPROC', 'PFNGLVALIDATEPROGRAMPROC',
    'PFNGLVERTEXATTRIB1DPROC', 'PFNGLVERTEXATTRIB1DVPROC',
    'PFNGLVERTEXATTRIB1FPROC', 'PFNGLVERTEXATTRIB1FVPROC',
    'PFNGLVERTEXATTRIB1SPROC', 'PFNGLVERTEXATTRIB1SVPROC',
    'PFNGLVERTEXATTRIB2DPROC', 'PFNGLVERTEXATTRIB2DVPROC',
    'PFNGLVERTEXATTRIB2FPROC', 'PFNGLVERTEXATTRIB2FVPROC',
    'PFNGLVERTEXATTRIB2SPROC', 'PFNGLVERTEXATTRIB2SVPROC',
    'PFNGLVERTEXATTRIB3DPROC', 'PFNGLVERTEXATTRIB3DVPROC',
    'PFNGLVERTEXATTRIB3FPROC', 'PFNGLVERTEXATTRIB3FVPROC',
    'PFNGLVERTEXATTRIB3SPROC', 'PFNGLVERTEXATTRIB3SVPROC',
    'PFNGLVERTEXATTRIB4NBVPROC', 'PFNGLVERTEXATTRIB4NIVPROC',
    'PFNGLVERTEXATTRIB4NSVPROC', 'PFNGLVERTEXATTRIB4NUBPROC',
    'PFNGLVERTEXATTRIB4NUBVPROC', 'PFNGLVERTEXATTRIB4NUIVPROC',
    'PFNGLVERTEXATTRIB4NUSVPROC', 'PFNGLVERTEXATTRIB4BVPROC',
    'PFNGLVERTEXATTRIB4DPROC', 'PFNGLVERTEXATTRIB4DVPROC',
    'PFNGLVERTEXATTRIB4FPROC', 'PFNGLVERTEXATTRIB4FVPROC',
    'PFNGLVERTEXATTRIB4IVPROC', 'PFNGLVERTEXATTRIB4SPROC',
    'PFNGLVERTEXATTRIB4SVPROC', 'PFNGLVERTEXATTRIB4UBVPROC',
    'PFNGLVERTEXATTRIB4UIVPROC', 'PFNGLVERTEXATTRIB4USVPROC',
    'PFNGLVERTEXATTRIBPOINTERPROC', 'glBlendEquationSeparate',
    'glDrawBuffers', 'glStencilOpSeparate', 'glStencilFuncSeparate',
    'glStencilMaskSeparate', 'glAttachShader', 'glBindAttribLocation',
    'glCompileShader', 'glCreateProgram', 'glCreateShader', 'glDeleteProgram',
    'glDeleteShader', 'glDetachShader', 'glDisableVertexAttribArray',
    'glEnableVertexAttribArray', 'glGetActiveAttrib', 'glGetActiveUniform',
    'glGetAttachedShaders', 'glGetAttribLocation', 'glGetProgramiv',
    'glGetProgramInfoLog', 'glGetShaderiv', 'glGetShaderInfoLog',
    'glGetShaderSource', 'glGetUniformLocation', 'glGetUniformfv',
    'glGetUniformiv', 'glGetVertexAttribdv', 'glGetVertexAttribfv',
    'glGetVertexAttribiv', 'glGetVertexAttribPointerv', 'glIsProgram',
    'glIsShader', 'glLinkProgram', 'glShaderSource', 'glUseProgram',
    'glUniform1f', 'glUniform2f', 'glUniform3f', 'glUniform4f', 'glUniform1i',
    'glUniform2i', 'glUniform3i', 'glUniform4i', 'glUniform1fv',
    'glUniform2fv', 'glUniform3fv', 'glUniform4fv', 'glUniform1iv',
    'glUniform2iv', 'glUniform3iv', 'glUniform4iv', 'glUniformMatrix2fv',
    'glUniformMatrix3fv', 'glUniformMatrix4fv', 'glValidateProgram',
    'glVertexAttrib1d', 'glVertexAttrib1dv', 'glVertexAttrib1f',
    'glVertexAttrib1fv', 'glVertexAttrib1s', 'glVertexAttrib1sv',
    'glVertexAttrib2d', 'glVertexAttrib2dv', 'glVertexAttrib2f',
    'glVertexAttrib2fv', 'glVertexAttrib2s', 'glVertexAttrib2sv',
    'glVertexAttrib3d', 'glVertexAttrib3dv', 'glVertexAttrib3f',
    'glVertexAttrib3fv', 'glVertexAttrib3s', 'glVertexAttrib3sv',
    'glVertexAttrib4Nbv', 'glVertexAttrib4Niv', 'glVertexAttrib4Nsv',
    'glVertexAttrib4Nub', 'glVertexAttrib4Nubv', 'glVertexAttrib4Nuiv',
    'glVertexAttrib4Nusv', 'glVertexAttrib4bv', 'glVertexAttrib4d',
    'glVertexAttrib4dv', 'glVertexAttrib4f', 'glVertexAttrib4fv',
    'glVertexAttrib4iv', 'glVertexAttrib4s', 'glVertexAttrib4sv',
    'glVertexAttrib4ubv', 'glVertexAttrib4uiv', 'glVertexAttrib4usv',
    'glVertexAttribPointer'
]
