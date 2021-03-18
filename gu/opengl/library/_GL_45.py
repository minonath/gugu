from .._types import *

GL_VERSION_4_5 = 1
GL_CONTEXT_LOST = 0x0507
GL_NEGATIVE_ONE_TO_ONE = 0x935E
GL_ZERO_TO_ONE = 0x935F
GL_CLIP_ORIGIN = 0x935C
GL_CLIP_DEPTH_MODE = 0x935D
GL_QUERY_WAIT_INVERTED = 0x8E17
GL_QUERY_NO_WAIT_INVERTED = 0x8E18
GL_QUERY_BY_REGION_WAIT_INVERTED = 0x8E19
GL_QUERY_BY_REGION_NO_WAIT_INVERTED = 0x8E1A
GL_MAX_CULL_DISTANCES = 0x82F9
GL_MAX_COMBINED_CLIP_AND_CULL_DISTANCES = 0x82FA
GL_TEXTURE_TARGET = 0x1006
GL_QUERY_TARGET = 0x82EA
GL_GUILTY_CONTEXT_RESET = 0x8253
GL_INNOCENT_CONTEXT_RESET = 0x8254
GL_UNKNOWN_CONTEXT_RESET = 0x8255
GL_RESET_NOTIFICATION_STRATEGY = 0x8256
GL_LOSE_CONTEXT_ON_RESET = 0x8252
GL_NO_RESET_NOTIFICATION = 0x8261
GL_CONTEXT_FLAG_ROBUST_ACCESS_BIT = 0x00000004
GL_CONTEXT_RELEASE_BEHAVIOR = 0x82FB
GL_CONTEXT_RELEASE_BEHAVIOR_FLUSH = 0x82FC
PFNGLCLIPCONTROLPROC = C(None, UInt, UInt)
PFNGLCREATETRANSFORMFEEDBACKSPROC = C(None, Int, P(UInt))
PFNGLTRANSFORMFEEDBACKBUFFERBASEPROC = C(None, UInt, UInt, UInt)
PFNGLTRANSFORMFEEDBACKBUFFERRANGEPROC = C(None, UInt, UInt, UInt, Size, Size)
PFNGLGETTRANSFORMFEEDBACKIVPROC = C(None, UInt, UInt, P(Int))
PFNGLGETTRANSFORMFEEDBACKI_VPROC = C(None, UInt, UInt, UInt, P(Int))
PFNGLGETTRANSFORMFEEDBACKI64_VPROC = C(None, UInt, UInt, UInt, P(Int64))
PFNGLCREATEBUFFERSPROC = C(None, Int, P(UInt))
PFNGLNAMEDBUFFERSTORAGEPROC = C(None, UInt, Size, VoidP, UInt)
PFNGLNAMEDBUFFERDATAPROC = C(None, UInt, Size, VoidP, UInt)
PFNGLNAMEDBUFFERSUBDATAPROC = C(None, UInt, Size, Size, VoidP)
PFNGLCOPYNAMEDBUFFERSUBDATAPROC = C(None, UInt, UInt, Size, Size, Size)
PFNGLCLEARNAMEDBUFFERDATAPROC = C(None, UInt, UInt, UInt, UInt, VoidP)
PFNGLCLEARNAMEDBUFFERSUBDATAPROC = C(
    None, UInt, UInt, Size, Size, UInt, UInt, VoidP
)
PFNGLMAPNAMEDBUFFERPROC = C(VoidP, UInt, UInt)
PFNGLMAPNAMEDBUFFERRANGEPROC = C(VoidP, UInt, Size, Size, UInt)
PFNGLUNMAPNAMEDBUFFERPROC = C(UByte, UInt)
PFNGLFLUSHMAPPEDNAMEDBUFFERRANGEPROC = C(None, UInt, Size, Size)
PFNGLGETNAMEDBUFFERPARAMETERIVPROC = C(None, UInt, UInt, P(Int))
PFNGLGETNAMEDBUFFERPARAMETERI64VPROC = C(None, UInt, UInt, P(Int64))
PFNGLGETNAMEDBUFFERPOINTERVPROC = C(None, UInt, UInt, P(VoidP))
PFNGLGETNAMEDBUFFERSUBDATAPROC = C(None, UInt, Size, Size, VoidP)
PFNGLCREATEFRAMEBUFFERSPROC = C(None, Int, P(UInt))
PFNGLNAMEDFRAMEBUFFERRENDERBUFFERPROC = C(None, UInt, UInt, UInt, UInt)
PFNGLNAMEDFRAMEBUFFERPARAMETERIPROC = C(None, UInt, UInt, Int)
PFNGLNAMEDFRAMEBUFFERTEXTUREPROC = C(None, UInt, UInt, UInt, Int)
PFNGLNAMEDFRAMEBUFFERTEXTURELAYERPROC = C(None, UInt, UInt, UInt, Int, Int)
PFNGLNAMEDFRAMEBUFFERDRAWBUFFERPROC = C(None, UInt, UInt)
PFNGLNAMEDFRAMEBUFFERDRAWBUFFERSPROC = C(None, UInt, Int, P(UInt))
PFNGLNAMEDFRAMEBUFFERREADBUFFERPROC = C(None, UInt, UInt)
PFNGLINVALIDATENAMEDFRAMEBUFFERDATAPROC = C(None, UInt, Int, P(UInt))
PFNGLINVALIDATENAMEDFRAMEBUFFERSUBDATAPROC = C(
    None, UInt, Int, P(UInt), Int, Int, Int, Int
)
PFNGLCLEARNAMEDFRAMEBUFFERIVPROC = C(None, UInt, UInt, Int, P(Int))
PFNGLCLEARNAMEDFRAMEBUFFERUIVPROC = C(None, UInt, UInt, Int, P(UInt))
PFNGLCLEARNAMEDFRAMEBUFFERFVPROC = C(None, UInt, UInt, Int, P(Float))
PFNGLCLEARNAMEDFRAMEBUFFERFIPROC = C(None, UInt, UInt, Int, Float, Int)
PFNGLBLITNAMEDFRAMEBUFFERPROC = C(
    None, UInt, UInt, Int, Int, Int, Int, Int, Int, Int, Int, UInt, UInt
)
PFNGLCHECKNAMEDFRAMEBUFFERSTATUSPROC = C(UInt, UInt, UInt)
PFNGLGETNAMEDFRAMEBUFFERPARAMETERIVPROC = C(None, UInt, UInt, P(Int))
PFNGLGETNAMEDFRAMEBUFFERATTACHMENTPARAMETERIVPROC = C(
    None, UInt, UInt, UInt, P(Int)
)
PFNGLCREATERENDERBUFFERSPROC = C(None, Int, P(UInt))
PFNGLNAMEDRENDERBUFFERSTORAGEPROC = C(None, UInt, UInt, Int, Int)
PFNGLNAMEDRENDERBUFFERSTORAGEMULTISAMPLEPROC = C(
    None, UInt, Int, UInt, Int, Int
)
PFNGLGETNAMEDRENDERBUFFERPARAMETERIVPROC = C(None, UInt, UInt, P(Int))
PFNGLCREATETEXTURESPROC = C(None, UInt, Int, P(UInt))
PFNGLTEXTUREBUFFERPROC = C(None, UInt, UInt, UInt)
PFNGLTEXTUREBUFFERRANGEPROC = C(None, UInt, UInt, UInt, Size, Size)
PFNGLTEXTURESTORAGE1DPROC = C(None, UInt, Int, UInt, Int)
PFNGLTEXTURESTORAGE2DPROC = C(None, UInt, Int, UInt, Int, Int)
PFNGLTEXTURESTORAGE3DPROC = C(None, UInt, Int, UInt, Int, Int, Int)
PFNGLTEXTURESTORAGE2DMULTISAMPLEPROC = C(
    None, UInt, Int, UInt, Int, Int, UByte
)
PFNGLTEXTURESTORAGE3DMULTISAMPLEPROC = C(
    None, UInt, Int, UInt, Int, Int, Int, UByte
)
PFNGLTEXTURESUBIMAGE1DPROC = C(None, UInt, Int, Int, Int, UInt, UInt, VoidP)
PFNGLTEXTURESUBIMAGE2DPROC = C(
    None, UInt, Int, Int, Int, Int, Int, UInt, UInt, VoidP
)
PFNGLTEXTURESUBIMAGE3DPROC = C(
    None, UInt, Int, Int, Int, Int, Int, Int, Int, UInt, UInt, VoidP
)
PFNGLCOMPRESSEDTEXTURESUBIMAGE1DPROC = C(
    None, UInt, Int, Int, Int, UInt, Int, VoidP
)
PFNGLCOMPRESSEDTEXTURESUBIMAGE2DPROC = C(
    None, UInt, Int, Int, Int, Int, Int, UInt, Int, VoidP
)
PFNGLCOMPRESSEDTEXTURESUBIMAGE3DPROC = C(
    None, UInt, Int, Int, Int, Int, Int, Int, Int, UInt, Int, VoidP
)
PFNGLCOPYTEXTURESUBIMAGE1DPROC = C(None, UInt, Int, Int, Int, Int, Int)
PFNGLCOPYTEXTURESUBIMAGE2DPROC = C(
    None, UInt, Int, Int, Int, Int, Int, Int, Int
)
PFNGLCOPYTEXTURESUBIMAGE3DPROC = C(
    None, UInt, Int, Int, Int, Int, Int, Int, Int, Int
)
PFNGLTEXTUREPARAMETERFPROC = C(None, UInt, UInt, Float)
PFNGLTEXTUREPARAMETERFVPROC = C(None, UInt, UInt, P(Float))
PFNGLTEXTUREPARAMETERIPROC = C(None, UInt, UInt, Int)
PFNGLTEXTUREPARAMETERIIVPROC = C(None, UInt, UInt, P(Int))
PFNGLTEXTUREPARAMETERIUIVPROC = C(None, UInt, UInt, P(UInt))
PFNGLTEXTUREPARAMETERIVPROC = C(None, UInt, UInt, P(Int))
PFNGLGENERATETEXTUREMIPMAPPROC = C(None, UInt)
PFNGLBINDTEXTUREUNITPROC = C(None, UInt, UInt)
PFNGLGETTEXTUREIMAGEPROC = C(None, UInt, Int, UInt, UInt, Int, VoidP)
PFNGLGETCOMPRESSEDTEXTUREIMAGEPROC = C(None, UInt, Int, Int, VoidP)
PFNGLGETTEXTURELEVELPARAMETERFVPROC = C(None, UInt, Int, UInt, P(Float))
PFNGLGETTEXTURELEVELPARAMETERIVPROC = C(None, UInt, Int, UInt, P(Int))
PFNGLGETTEXTUREPARAMETERFVPROC = C(None, UInt, UInt, P(Float))
PFNGLGETTEXTUREPARAMETERIIVPROC = C(None, UInt, UInt, P(Int))
PFNGLGETTEXTUREPARAMETERIUIVPROC = C(None, UInt, UInt, P(UInt))
PFNGLGETTEXTUREPARAMETERIVPROC = C(None, UInt, UInt, P(Int))
PFNGLCREATEVERTEXARRAYSPROC = C(None, Int, P(UInt))
PFNGLDISABLEVERTEXARRAYATTRIBPROC = C(None, UInt, UInt)
PFNGLENABLEVERTEXARRAYATTRIBPROC = C(None, UInt, UInt)
PFNGLVERTEXARRAYELEMENTBUFFERPROC = C(None, UInt, UInt)
PFNGLVERTEXARRAYVERTEXBUFFERPROC = C(None, UInt, UInt, UInt, Size, Int)
PFNGLVERTEXARRAYVERTEXBUFFERSPROC = C(
    None, UInt, UInt, Int, P(UInt), P(Size), P(Int)
)
PFNGLVERTEXARRAYATTRIBBINDINGPROC = C(None, UInt, UInt, UInt)
PFNGLVERTEXARRAYATTRIBFORMATPROC = C(None, UInt, UInt, Int, UInt, UByte, UInt)
PFNGLVERTEXARRAYATTRIBIFORMATPROC = C(None, UInt, UInt, Int, UInt, UInt)
PFNGLVERTEXARRAYATTRIBLFORMATPROC = C(None, UInt, UInt, Int, UInt, UInt)
PFNGLVERTEXARRAYBINDINGDIVISORPROC = C(None, UInt, UInt, UInt)
PFNGLGETVERTEXARRAYIVPROC = C(None, UInt, UInt, P(Int))
PFNGLGETVERTEXARRAYINDEXEDIVPROC = C(None, UInt, UInt, UInt, P(Int))
PFNGLGETVERTEXARRAYINDEXED64IVPROC = C(None, UInt, UInt, UInt, P(Int64))
PFNGLCREATESAMPLERSPROC = C(None, Int, P(UInt))
PFNGLCREATEPROGRAMPIPELINESPROC = C(None, Int, P(UInt))
PFNGLCREATEQUERIESPROC = C(None, UInt, Int, P(UInt))
PFNGLGETQUERYBUFFEROBJECTI64VPROC = C(None, UInt, UInt, UInt, Size)
PFNGLGETQUERYBUFFEROBJECTIVPROC = C(None, UInt, UInt, UInt, Size)
PFNGLGETQUERYBUFFEROBJECTUI64VPROC = C(None, UInt, UInt, UInt, Size)
PFNGLGETQUERYBUFFEROBJECTUIVPROC = C(None, UInt, UInt, UInt, Size)
PFNGLMEMORYBARRIERBYREGIONPROC = C(None, UInt)
PFNGLGETTEXTURESUBIMAGEPROC = C(
    None, UInt, Int, Int, Int, Int, Int, Int, Int, UInt, UInt, Int, VoidP
)
PFNGLGETCOMPRESSEDTEXTURESUBIMAGEPROC = C(
    None, UInt, Int, Int, Int, Int, Int, Int, Int, Int, VoidP
)
PFNGLGETGRAPHICSRESETSTATUSPROC = C(UInt)
PFNGLGETNCOMPRESSEDTEXIMAGEPROC = C(None, UInt, Int, Int, VoidP)
PFNGLGETNTEXIMAGEPROC = C(None, UInt, Int, UInt, UInt, Int, VoidP)
PFNGLGETNUNIFORMDVPROC = C(None, UInt, Int, Int, P(Double))
PFNGLGETNUNIFORMFVPROC = C(None, UInt, Int, Int, P(Float))
PFNGLGETNUNIFORMIVPROC = C(None, UInt, Int, Int, P(Int))
PFNGLGETNUNIFORMUIVPROC = C(None, UInt, Int, Int, P(UInt))
PFNGLREADNPIXELSPROC = C(None, Int, Int, Int, Int, UInt, UInt, Int, VoidP)
PFNGLTEXTUREBARRIERPROC = C(None)
glClipControl = E('glClipControl', None, UInt, UInt)
glCreateTransformFeedbacks = E(
    'glCreateTransformFeedbacks', None, Int, P(UInt)
)
glTransformFeedbackBufferBase = E(
    'glTransformFeedbackBufferBase', None, UInt, UInt, UInt
)
glTransformFeedbackBufferRange = E(
    'glTransformFeedbackBufferRange', None, UInt, UInt, UInt, Size, Size
)
glGetTransformFeedbackiv = E(
    'glGetTransformFeedbackiv', None, UInt, UInt, P(Int)
)
glGetTransformFeedbacki_v = E(
    'glGetTransformFeedbacki_v', None, UInt, UInt, UInt, P(Int)
)
glGetTransformFeedbacki64_v = E(
    'glGetTransformFeedbacki64_v', None, UInt, UInt, UInt, P(Int64)
)
glCreateBuffers = E('glCreateBuffers', None, Int, P(UInt))
glNamedBufferStorage = E(
    'glNamedBufferStorage', None, UInt, Size, VoidP, UInt
)
glNamedBufferData = E('glNamedBufferData', None, UInt, Size, VoidP, UInt)
glNamedBufferSubData = E(
    'glNamedBufferSubData', None, UInt, Size, Size, VoidP
)
glCopyNamedBufferSubData = E(
    'glCopyNamedBufferSubData', None, UInt, UInt, Size, Size, Size
)
glClearNamedBufferData = E(
    'glClearNamedBufferData', None, UInt, UInt, UInt, UInt, VoidP
)
glClearNamedBufferSubData = E(
    'glClearNamedBufferSubData', None, UInt, UInt, Size, Size, UInt, UInt,
    VoidP
)
glMapNamedBuffer = E('glMapNamedBuffer', VoidP, UInt, UInt)
glMapNamedBufferRange = E(
    'glMapNamedBufferRange', VoidP, UInt, Size, Size, UInt
)
glUnmapNamedBuffer = E('glUnmapNamedBuffer', UByte, UInt)
glFlushMappedNamedBufferRange = E(
    'glFlushMappedNamedBufferRange', None, UInt, Size, Size
)
glGetNamedBufferParameteriv = E(
    'glGetNamedBufferParameteriv', None, UInt, UInt, P(Int)
)
glGetNamedBufferParameteri64v = E(
    'glGetNamedBufferParameteri64v', None, UInt, UInt, P(Int64)
)
glGetNamedBufferPointerv = E(
    'glGetNamedBufferPointerv', None, UInt, UInt, P(VoidP)
)
glGetNamedBufferSubData = E(
    'glGetNamedBufferSubData', None, UInt, Size, Size, VoidP
)
glCreateFramebuffers = E('glCreateFramebuffers', None, Int, P(UInt))
glNamedFramebufferRenderbuffer = E(
    'glNamedFramebufferRenderbuffer', None, UInt, UInt, UInt, UInt
)
glNamedFramebufferParameteri = E(
    'glNamedFramebufferParameteri', None, UInt, UInt, Int
)
glNamedFramebufferTexture = E(
    'glNamedFramebufferTexture', None, UInt, UInt, UInt, Int
)
glNamedFramebufferTextureLayer = E(
    'glNamedFramebufferTextureLayer', None, UInt, UInt, UInt, Int, Int
)
glNamedFramebufferDrawBuffer = E(
    'glNamedFramebufferDrawBuffer', None, UInt, UInt
)
glNamedFramebufferDrawBuffers = E(
    'glNamedFramebufferDrawBuffers', None, UInt, Int, P(UInt)
)
glNamedFramebufferReadBuffer = E(
    'glNamedFramebufferReadBuffer', None, UInt, UInt
)
glInvalidateNamedFramebufferData = E(
    'glInvalidateNamedFramebufferData', None, UInt, Int, P(UInt)
)
glInvalidateNamedFramebufferSubData = E(
    'glInvalidateNamedFramebufferSubData', None, UInt, Int, P(UInt), Int, Int,
    Int, Int
)
glClearNamedFramebufferiv = E(
    'glClearNamedFramebufferiv', None, UInt, UInt, Int, P(Int)
)
glClearNamedFramebufferuiv = E(
    'glClearNamedFramebufferuiv', None, UInt, UInt, Int, P(UInt)
)
glClearNamedFramebufferfv = E(
    'glClearNamedFramebufferfv', None, UInt, UInt, Int, P(Float)
)
glClearNamedFramebufferfi = E(
    'glClearNamedFramebufferfi', None, UInt, UInt, Int, Float, Int
)
glBlitNamedFramebuffer = E(
    'glBlitNamedFramebuffer', None, UInt, UInt, Int, Int, Int, Int, Int, Int,
    Int, Int, UInt, UInt
)
glCheckNamedFramebufferStatus = E(
    'glCheckNamedFramebufferStatus', UInt, UInt, UInt
)
glGetNamedFramebufferParameteriv = E(
    'glGetNamedFramebufferParameteriv', None, UInt, UInt, P(Int)
)
glGetNamedFramebufferAttachmentParameteriv = E(
    'glGetNamedFramebufferAttachmentParameteriv', None, UInt, UInt, UInt,
    P(Int)
)
glCreateRenderbuffers = E('glCreateRenderbuffers', None, Int, P(UInt))
glNamedRenderbufferStorage = E(
    'glNamedRenderbufferStorage', None, UInt, UInt, Int, Int
)
glNamedRenderbufferStorageMultisample = E(
    'glNamedRenderbufferStorageMultisample', None, UInt, Int, UInt, Int, Int
)
glGetNamedRenderbufferParameteriv = E(
    'glGetNamedRenderbufferParameteriv', None, UInt, UInt, P(Int)
)
glCreateTextures = E('glCreateTextures', None, UInt, Int, P(UInt))
glTextureBuffer = E('glTextureBuffer', None, UInt, UInt, UInt)
glTextureBufferRange = E(
    'glTextureBufferRange', None, UInt, UInt, UInt, Size, Size
)
glTextureStorage1D = E('glTextureStorage1D', None, UInt, Int, UInt, Int)
glTextureStorage2D = E('glTextureStorage2D', None, UInt, Int, UInt, Int, Int)
glTextureStorage3D = E(
    'glTextureStorage3D', None, UInt, Int, UInt, Int, Int, Int
)
glTextureStorage2DMultisample = E(
    'glTextureStorage2DMultisample', None, UInt, Int, UInt, Int, Int, UByte
)
glTextureStorage3DMultisample = E(
    'glTextureStorage3DMultisample', None, UInt, Int, UInt, Int, Int, Int,
    UByte
)
glTextureSubImage1D = E(
    'glTextureSubImage1D', None, UInt, Int, Int, Int, UInt, UInt, VoidP
)
glTextureSubImage2D = E(
    'glTextureSubImage2D', None, UInt, Int, Int, Int, Int, Int, UInt, UInt,
    VoidP
)
glTextureSubImage3D = E(
    'glTextureSubImage3D', None, UInt, Int, Int, Int, Int, Int, Int, Int,
    UInt, UInt, VoidP
)
glCompressedTextureSubImage1D = E(
    'glCompressedTextureSubImage1D', None, UInt, Int, Int, Int, UInt, Int,
    VoidP
)
glCompressedTextureSubImage2D = E(
    'glCompressedTextureSubImage2D', None, UInt, Int, Int, Int, Int, Int,
    UInt, Int, VoidP
)
glCompressedTextureSubImage3D = E(
    'glCompressedTextureSubImage3D', None, UInt, Int, Int, Int, Int, Int, Int,
    Int, UInt, Int, VoidP
)
glCopyTextureSubImage1D = E(
    'glCopyTextureSubImage1D', None, UInt, Int, Int, Int, Int, Int
)
glCopyTextureSubImage2D = E(
    'glCopyTextureSubImage2D', None, UInt, Int, Int, Int, Int, Int, Int, Int
)
glCopyTextureSubImage3D = E(
    'glCopyTextureSubImage3D', None, UInt, Int, Int, Int, Int, Int, Int, Int,
    Int
)
glTextureParameterf = E('glTextureParameterf', None, UInt, UInt, Float)
glTextureParameterfv = E('glTextureParameterfv', None, UInt, UInt, P(Float))
glTextureParameteri = E('glTextureParameteri', None, UInt, UInt, Int)
glTextureParameterIiv = E('glTextureParameterIiv', None, UInt, UInt, P(Int))
glTextureParameterIuiv = E(
    'glTextureParameterIuiv', None, UInt, UInt, P(UInt)
)
glTextureParameteriv = E('glTextureParameteriv', None, UInt, UInt, P(Int))
glGenerateTextureMipmap = E('glGenerateTextureMipmap', None, UInt)
glBindTextureUnit = E('glBindTextureUnit', None, UInt, UInt)
glGetTextureImage = E(
    'glGetTextureImage', None, UInt, Int, UInt, UInt, Int, VoidP
)
glGetCompressedTextureImage = E(
    'glGetCompressedTextureImage', None, UInt, Int, Int, VoidP
)
glGetTextureLevelParameterfv = E(
    'glGetTextureLevelParameterfv', None, UInt, Int, UInt, P(Float)
)
glGetTextureLevelParameteriv = E(
    'glGetTextureLevelParameteriv', None, UInt, Int, UInt, P(Int)
)
glGetTextureParameterfv = E(
    'glGetTextureParameterfv', None, UInt, UInt, P(Float)
)
glGetTextureParameterIiv = E(
    'glGetTextureParameterIiv', None, UInt, UInt, P(Int)
)
glGetTextureParameterIuiv = E(
    'glGetTextureParameterIuiv', None, UInt, UInt, P(UInt)
)
glGetTextureParameteriv = E(
    'glGetTextureParameteriv', None, UInt, UInt, P(Int)
)
glCreateVertexArrays = E('glCreateVertexArrays', None, Int, P(UInt))
glDisableVertexArrayAttrib = E('glDisableVertexArrayAttrib', None, UInt, UInt)
glEnableVertexArrayAttrib = E('glEnableVertexArrayAttrib', None, UInt, UInt)
glVertexArrayElementBuffer = E('glVertexArrayElementBuffer', None, UInt, UInt)
glVertexArrayVertexBuffer = E(
    'glVertexArrayVertexBuffer', None, UInt, UInt, UInt, Size, Int
)
glVertexArrayVertexBuffers = E(
    'glVertexArrayVertexBuffers', None, UInt, UInt, Int, P(UInt), P(Size),
    P(Int)
)
glVertexArrayAttribBinding = E(
    'glVertexArrayAttribBinding', None, UInt, UInt, UInt
)
glVertexArrayAttribFormat = E(
    'glVertexArrayAttribFormat', None, UInt, UInt, Int, UInt, UByte, UInt
)
glVertexArrayAttribIFormat = E(
    'glVertexArrayAttribIFormat', None, UInt, UInt, Int, UInt, UInt
)
glVertexArrayAttribLFormat = E(
    'glVertexArrayAttribLFormat', None, UInt, UInt, Int, UInt, UInt
)
glVertexArrayBindingDivisor = E(
    'glVertexArrayBindingDivisor', None, UInt, UInt, UInt
)
glGetVertexArrayiv = E('glGetVertexArrayiv', None, UInt, UInt, P(Int))
glGetVertexArrayIndexediv = E(
    'glGetVertexArrayIndexediv', None, UInt, UInt, UInt, P(Int)
)
glGetVertexArrayIndexed64iv = E(
    'glGetVertexArrayIndexed64iv', None, UInt, UInt, UInt, P(Int64)
)
glCreateSamplers = E('glCreateSamplers', None, Int, P(UInt))
glCreateProgramPipelines = E('glCreateProgramPipelines', None, Int, P(UInt))
glCreateQueries = E('glCreateQueries', None, UInt, Int, P(UInt))
glGetQueryBufferObjecti64v = E(
    'glGetQueryBufferObjecti64v', None, UInt, UInt, UInt, Size
)
glGetQueryBufferObjectiv = E(
    'glGetQueryBufferObjectiv', None, UInt, UInt, UInt, Size
)
glGetQueryBufferObjectui64v = E(
    'glGetQueryBufferObjectui64v', None, UInt, UInt, UInt, Size
)
glGetQueryBufferObjectuiv = E(
    'glGetQueryBufferObjectuiv', None, UInt, UInt, UInt, Size
)
glMemoryBarrierByRegion = E('glMemoryBarrierByRegion', None, UInt)
glGetTextureSubImage = E(
    'glGetTextureSubImage', None, UInt, Int, Int, Int, Int, Int, Int, Int,
    UInt, UInt, Int, VoidP
)
glGetCompressedTextureSubImage = E(
    'glGetCompressedTextureSubImage', None, UInt, Int, Int, Int, Int, Int,
    Int, Int, Int, VoidP
)
glGetGraphicsResetStatus = E('glGetGraphicsResetStatus', UInt)
glGetnCompressedTexImage = E(
    'glGetnCompressedTexImage', None, UInt, Int, Int, VoidP
)
glGetnTexImage = E('glGetnTexImage', None, UInt, Int, UInt, UInt, Int, VoidP)
glGetnUniformdv = E('glGetnUniformdv', None, UInt, Int, Int, P(Double))
glGetnUniformfv = E('glGetnUniformfv', None, UInt, Int, Int, P(Float))
glGetnUniformiv = E('glGetnUniformiv', None, UInt, Int, Int, P(Int))
glGetnUniformuiv = E('glGetnUniformuiv', None, UInt, Int, Int, P(UInt))
glReadnPixels = E(
    'glReadnPixels', None, Int, Int, Int, Int, UInt, UInt, Int, VoidP
)
glTextureBarrier = E('glTextureBarrier', None)

__all__ = [
    'GL_VERSION_4_5', 'GL_CONTEXT_LOST', 'GL_NEGATIVE_ONE_TO_ONE',
    'GL_ZERO_TO_ONE', 'GL_CLIP_ORIGIN', 'GL_CLIP_DEPTH_MODE',
    'GL_QUERY_WAIT_INVERTED', 'GL_QUERY_NO_WAIT_INVERTED',
    'GL_QUERY_BY_REGION_WAIT_INVERTED', 'GL_QUERY_BY_REGION_NO_WAIT_INVERTED',
    'GL_MAX_CULL_DISTANCES', 'GL_MAX_COMBINED_CLIP_AND_CULL_DISTANCES',
    'GL_TEXTURE_TARGET', 'GL_QUERY_TARGET', 'GL_GUILTY_CONTEXT_RESET',
    'GL_INNOCENT_CONTEXT_RESET', 'GL_UNKNOWN_CONTEXT_RESET',
    'GL_RESET_NOTIFICATION_STRATEGY', 'GL_LOSE_CONTEXT_ON_RESET',
    'GL_NO_RESET_NOTIFICATION', 'GL_CONTEXT_FLAG_ROBUST_ACCESS_BIT',
    'GL_CONTEXT_RELEASE_BEHAVIOR', 'GL_CONTEXT_RELEASE_BEHAVIOR_FLUSH',
    'PFNGLCLIPCONTROLPROC', 'PFNGLCREATETRANSFORMFEEDBACKSPROC',
    'PFNGLTRANSFORMFEEDBACKBUFFERBASEPROC',
    'PFNGLTRANSFORMFEEDBACKBUFFERRANGEPROC',
    'PFNGLGETTRANSFORMFEEDBACKIVPROC', 'PFNGLGETTRANSFORMFEEDBACKI_VPROC',
    'PFNGLGETTRANSFORMFEEDBACKI64_VPROC', 'PFNGLCREATEBUFFERSPROC',
    'PFNGLNAMEDBUFFERSTORAGEPROC', 'PFNGLNAMEDBUFFERDATAPROC',
    'PFNGLNAMEDBUFFERSUBDATAPROC', 'PFNGLCOPYNAMEDBUFFERSUBDATAPROC',
    'PFNGLCLEARNAMEDBUFFERDATAPROC', 'PFNGLCLEARNAMEDBUFFERSUBDATAPROC',
    'PFNGLMAPNAMEDBUFFERPROC', 'PFNGLMAPNAMEDBUFFERRANGEPROC',
    'PFNGLUNMAPNAMEDBUFFERPROC', 'PFNGLFLUSHMAPPEDNAMEDBUFFERRANGEPROC',
    'PFNGLGETNAMEDBUFFERPARAMETERIVPROC',
    'PFNGLGETNAMEDBUFFERPARAMETERI64VPROC', 'PFNGLGETNAMEDBUFFERPOINTERVPROC',
    'PFNGLGETNAMEDBUFFERSUBDATAPROC', 'PFNGLCREATEFRAMEBUFFERSPROC',
    'PFNGLNAMEDFRAMEBUFFERRENDERBUFFERPROC',
    'PFNGLNAMEDFRAMEBUFFERPARAMETERIPROC', 'PFNGLNAMEDFRAMEBUFFERTEXTUREPROC',
    'PFNGLNAMEDFRAMEBUFFERTEXTURELAYERPROC',
    'PFNGLNAMEDFRAMEBUFFERDRAWBUFFERPROC',
    'PFNGLNAMEDFRAMEBUFFERDRAWBUFFERSPROC',
    'PFNGLNAMEDFRAMEBUFFERREADBUFFERPROC',
    'PFNGLINVALIDATENAMEDFRAMEBUFFERDATAPROC',
    'PFNGLINVALIDATENAMEDFRAMEBUFFERSUBDATAPROC',
    'PFNGLCLEARNAMEDFRAMEBUFFERIVPROC', 'PFNGLCLEARNAMEDFRAMEBUFFERUIVPROC',
    'PFNGLCLEARNAMEDFRAMEBUFFERFVPROC', 'PFNGLCLEARNAMEDFRAMEBUFFERFIPROC',
    'PFNGLBLITNAMEDFRAMEBUFFERPROC', 'PFNGLCHECKNAMEDFRAMEBUFFERSTATUSPROC',
    'PFNGLGETNAMEDFRAMEBUFFERPARAMETERIVPROC',
    'PFNGLGETNAMEDFRAMEBUFFERATTACHMENTPARAMETERIVPROC',
    'PFNGLCREATERENDERBUFFERSPROC', 'PFNGLNAMEDRENDERBUFFERSTORAGEPROC',
    'PFNGLNAMEDRENDERBUFFERSTORAGEMULTISAMPLEPROC',
    'PFNGLGETNAMEDRENDERBUFFERPARAMETERIVPROC', 'PFNGLCREATETEXTURESPROC',
    'PFNGLTEXTUREBUFFERPROC', 'PFNGLTEXTUREBUFFERRANGEPROC',
    'PFNGLTEXTURESTORAGE1DPROC', 'PFNGLTEXTURESTORAGE2DPROC',
    'PFNGLTEXTURESTORAGE3DPROC', 'PFNGLTEXTURESTORAGE2DMULTISAMPLEPROC',
    'PFNGLTEXTURESTORAGE3DMULTISAMPLEPROC', 'PFNGLTEXTURESUBIMAGE1DPROC',
    'PFNGLTEXTURESUBIMAGE2DPROC', 'PFNGLTEXTURESUBIMAGE3DPROC',
    'PFNGLCOMPRESSEDTEXTURESUBIMAGE1DPROC',
    'PFNGLCOMPRESSEDTEXTURESUBIMAGE2DPROC',
    'PFNGLCOMPRESSEDTEXTURESUBIMAGE3DPROC', 'PFNGLCOPYTEXTURESUBIMAGE1DPROC',
    'PFNGLCOPYTEXTURESUBIMAGE2DPROC', 'PFNGLCOPYTEXTURESUBIMAGE3DPROC',
    'PFNGLTEXTUREPARAMETERFPROC', 'PFNGLTEXTUREPARAMETERFVPROC',
    'PFNGLTEXTUREPARAMETERIPROC', 'PFNGLTEXTUREPARAMETERIIVPROC',
    'PFNGLTEXTUREPARAMETERIUIVPROC', 'PFNGLTEXTUREPARAMETERIVPROC',
    'PFNGLGENERATETEXTUREMIPMAPPROC', 'PFNGLBINDTEXTUREUNITPROC',
    'PFNGLGETTEXTUREIMAGEPROC', 'PFNGLGETCOMPRESSEDTEXTUREIMAGEPROC',
    'PFNGLGETTEXTURELEVELPARAMETERFVPROC',
    'PFNGLGETTEXTURELEVELPARAMETERIVPROC', 'PFNGLGETTEXTUREPARAMETERFVPROC',
    'PFNGLGETTEXTUREPARAMETERIIVPROC', 'PFNGLGETTEXTUREPARAMETERIUIVPROC',
    'PFNGLGETTEXTUREPARAMETERIVPROC', 'PFNGLCREATEVERTEXARRAYSPROC',
    'PFNGLDISABLEVERTEXARRAYATTRIBPROC', 'PFNGLENABLEVERTEXARRAYATTRIBPROC',
    'PFNGLVERTEXARRAYELEMENTBUFFERPROC', 'PFNGLVERTEXARRAYVERTEXBUFFERPROC',
    'PFNGLVERTEXARRAYVERTEXBUFFERSPROC', 'PFNGLVERTEXARRAYATTRIBBINDINGPROC',
    'PFNGLVERTEXARRAYATTRIBFORMATPROC', 'PFNGLVERTEXARRAYATTRIBIFORMATPROC',
    'PFNGLVERTEXARRAYATTRIBLFORMATPROC', 'PFNGLVERTEXARRAYBINDINGDIVISORPROC',
    'PFNGLGETVERTEXARRAYIVPROC', 'PFNGLGETVERTEXARRAYINDEXEDIVPROC',
    'PFNGLGETVERTEXARRAYINDEXED64IVPROC', 'PFNGLCREATESAMPLERSPROC',
    'PFNGLCREATEPROGRAMPIPELINESPROC', 'PFNGLCREATEQUERIESPROC',
    'PFNGLGETQUERYBUFFEROBJECTI64VPROC', 'PFNGLGETQUERYBUFFEROBJECTIVPROC',
    'PFNGLGETQUERYBUFFEROBJECTUI64VPROC', 'PFNGLGETQUERYBUFFEROBJECTUIVPROC',
    'PFNGLMEMORYBARRIERBYREGIONPROC', 'PFNGLGETTEXTURESUBIMAGEPROC',
    'PFNGLGETCOMPRESSEDTEXTURESUBIMAGEPROC',
    'PFNGLGETGRAPHICSRESETSTATUSPROC', 'PFNGLGETNCOMPRESSEDTEXIMAGEPROC',
    'PFNGLGETNTEXIMAGEPROC', 'PFNGLGETNUNIFORMDVPROC',
    'PFNGLGETNUNIFORMFVPROC', 'PFNGLGETNUNIFORMIVPROC',
    'PFNGLGETNUNIFORMUIVPROC', 'PFNGLREADNPIXELSPROC',
    'PFNGLTEXTUREBARRIERPROC', 'glClipControl', 'glCreateTransformFeedbacks',
    'glTransformFeedbackBufferBase', 'glTransformFeedbackBufferRange',
    'glGetTransformFeedbackiv', 'glGetTransformFeedbacki_v',
    'glGetTransformFeedbacki64_v', 'glCreateBuffers', 'glNamedBufferStorage',
    'glNamedBufferData', 'glNamedBufferSubData', 'glCopyNamedBufferSubData',
    'glClearNamedBufferData', 'glClearNamedBufferSubData', 'glMapNamedBuffer',
    'glMapNamedBufferRange', 'glUnmapNamedBuffer',
    'glFlushMappedNamedBufferRange', 'glGetNamedBufferParameteriv',
    'glGetNamedBufferParameteri64v', 'glGetNamedBufferPointerv',
    'glGetNamedBufferSubData', 'glCreateFramebuffers',
    'glNamedFramebufferRenderbuffer', 'glNamedFramebufferParameteri',
    'glNamedFramebufferTexture', 'glNamedFramebufferTextureLayer',
    'glNamedFramebufferDrawBuffer', 'glNamedFramebufferDrawBuffers',
    'glNamedFramebufferReadBuffer', 'glInvalidateNamedFramebufferData',
    'glInvalidateNamedFramebufferSubData', 'glClearNamedFramebufferiv',
    'glClearNamedFramebufferuiv', 'glClearNamedFramebufferfv',
    'glClearNamedFramebufferfi', 'glBlitNamedFramebuffer',
    'glCheckNamedFramebufferStatus', 'glGetNamedFramebufferParameteriv',
    'glGetNamedFramebufferAttachmentParameteriv', 'glCreateRenderbuffers',
    'glNamedRenderbufferStorage', 'glNamedRenderbufferStorageMultisample',
    'glGetNamedRenderbufferParameteriv', 'glCreateTextures',
    'glTextureBuffer', 'glTextureBufferRange', 'glTextureStorage1D',
    'glTextureStorage2D', 'glTextureStorage3D',
    'glTextureStorage2DMultisample', 'glTextureStorage3DMultisample',
    'glTextureSubImage1D', 'glTextureSubImage2D', 'glTextureSubImage3D',
    'glCompressedTextureSubImage1D', 'glCompressedTextureSubImage2D',
    'glCompressedTextureSubImage3D', 'glCopyTextureSubImage1D',
    'glCopyTextureSubImage2D', 'glCopyTextureSubImage3D',
    'glTextureParameterf', 'glTextureParameterfv', 'glTextureParameteri',
    'glTextureParameterIiv', 'glTextureParameterIuiv', 'glTextureParameteriv',
    'glGenerateTextureMipmap', 'glBindTextureUnit', 'glGetTextureImage',
    'glGetCompressedTextureImage', 'glGetTextureLevelParameterfv',
    'glGetTextureLevelParameteriv', 'glGetTextureParameterfv',
    'glGetTextureParameterIiv', 'glGetTextureParameterIuiv',
    'glGetTextureParameteriv', 'glCreateVertexArrays',
    'glDisableVertexArrayAttrib', 'glEnableVertexArrayAttrib',
    'glVertexArrayElementBuffer', 'glVertexArrayVertexBuffer',
    'glVertexArrayVertexBuffers', 'glVertexArrayAttribBinding',
    'glVertexArrayAttribFormat', 'glVertexArrayAttribIFormat',
    'glVertexArrayAttribLFormat', 'glVertexArrayBindingDivisor',
    'glGetVertexArrayiv', 'glGetVertexArrayIndexediv',
    'glGetVertexArrayIndexed64iv', 'glCreateSamplers',
    'glCreateProgramPipelines', 'glCreateQueries',
    'glGetQueryBufferObjecti64v', 'glGetQueryBufferObjectiv',
    'glGetQueryBufferObjectui64v', 'glGetQueryBufferObjectuiv',
    'glMemoryBarrierByRegion', 'glGetTextureSubImage',
    'glGetCompressedTextureSubImage', 'glGetGraphicsResetStatus',
    'glGetnCompressedTexImage', 'glGetnTexImage', 'glGetnUniformdv',
    'glGetnUniformfv', 'glGetnUniformiv', 'glGetnUniformuiv', 'glReadnPixels',
    'glTextureBarrier'
]
