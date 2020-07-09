import ctypes

from .object import OpenGLObject

from ..window import gl_context
from ..opengl import *

COMPARE_FUNCTION_MASKS = (
    'GL_NONE', 'GL_L''EQUAL', 'GL_LESS', 'GL_G''EQUAL', 'GL_GREATER',
    'GL_EQUAL', 'GL_NOTEQUAL', 'GL_NEVER', 'GL_ALWAYS'
)

# 基本类型对应 4 种通道模式。
# 一个通道是红色，二个是红绿，三个是红绿蓝，四个是红绿蓝加透明。
BASE_FLOAT = 'GL_RED, GL_RG', 'GL_RGB', 'GL_RGB''A'

# 基本类型对应的整数形式，储存的整数的量，正常 PNG 图片是用整数形式。
BASE_INT = (
    'GL_RED_INTEGER', 'GL_RG_INTEGER', 'GL_RGB_INTEGER', 'GL_RGB''A_INTEGER'
)

# 显卡内部储存格式，需要对应。
INTERNAL_FLOAT_8 = 'GL_R8', 'GL_RG8', 'GL_RGB8', 'GL_RGB''A8'
INTERNAL_FLOAT_16 = 'GL_R16F', 'GL_RG16F', 'GL_RGB16F', 'GL_RGB''A16F'
INTERNAL_FLOAT_32 = 'GL_R32F', 'GL_RG32F', 'GL_RGB32F', 'GL_RGB''A32F'
INTERNAL_UNSIGNED_8 = 'GL_R8UI', 'GL_RG8UI', 'GL_RGB8UI', 'GL_RGB''A8UI'
INTERNAL_UNSIGNED_16 = 'GL_R16UI', 'GL_RG16UI', 'GL_RGB16UI', 'GL_RGB''A16UI'
INTERNAL_UNSIGNED_32 = 'GL_R32UI', 'GL_RG32UI', 'GL_RGB32UI', 'GL_RGB''A32UI'
INTERNAL_INT_8 = 'GL_R8I', 'GL_RG8I', 'GL_RGB8I', 'GL_RGB''A8I'
INTERNAL_INT_16 = 'GL_R16I', 'GL_RG16I', 'GL_RGB16I', 'GL_RGB''A16I'
INTERNAL_INT_32 = 'GL_R32I', 'GL_RG32I', 'GL_RGB32I', 'GL_RGB''A32I'

# 纹理储存格式。
TEXTURE_STORAGE_FORMAT = {
    'float 8': (BASE_FLOAT, INTERNAL_FLOAT_8, 'GL_UNSIGNED_BYTE', 1),
    'float 16': (BASE_FLOAT, INTERNAL_FLOAT_16, 'GL_HALF_FLOAT', 2),
    'float 32': (BASE_FLOAT, INTERNAL_FLOAT_32, 'GL_FLOAT', 4),
    'unsigned 8': (BASE_INT, INTERNAL_UNSIGNED_8, 'GL_UNSIGNED_BYTE', 1),
    'unsigned 16': (BASE_INT, INTERNAL_UNSIGNED_16, 'GL_UNSIGNED_SHORT', 2),
    'unsigned 32': (BASE_INT, INTERNAL_UNSIGNED_32, 'GL_UNSIGNED_INT', 4),
    'int 8': (BASE_INT, INTERNAL_INT_8, 'GL_BYTE', 1),
    'int 16': (BASE_INT, INTERNAL_INT_16, 'GL_SHORT', 2),
    'int 32': (BASE_INT, INTERNAL_INT_32, 'GL_INT', 4),
}


def storage_info(type_mask, components):
    assert type_mask in TEXTURE_STORAGE_FORMAT
    assert components in (1, 2, 3, 4)

    components -= 1
    (base_set, internal_set, pixel_enum, pixel_bytes
     ) = TEXTURE_STORAGE_FORMAT[type_mask]

    base_enum = base_set[components]
    internal_enum = internal_set[components]
    base = gl_getattr(base_enum)
    internal = gl_getattr(internal_enum)
    pixel_type = gl_getattr(pixel_enum)

    return (base_enum, base, internal_enum, internal,
            pixel_enum, pixel_type, pixel_bytes)


class Texture(OpenGLObject):
    """
    包含的变量及用途：

    _texture_alignment          显卡内存对齐字节数。
    _texture_type_mask          显卡储存格式概括。
    _texture_base_enum          纹理储存基本格式（文本）。
    _texture_base               纹理储存基本格式。
    _texture_internal_enum      显卡内储存格式（文本）。
    _texture_internal           显卡内储存格式。

    _texture_depth              纹理是否为深度模式。
    _texture_sample_nums        纹理是否为多重采样。

    _texture_id                 纹理显卡编号。
    _texture_data               纹理数据。
    _texture_width              纹理宽度。
    _texture_height             纹理高度。
    _texture_target_enum        纹理目标（文本）。
    _texture_target             纹理目标。

    _texture_pixel_channel_nums 像素纹理通道数。
    _texture_pixel_enum         像素内存类型（文本）。
    _texture_pixel_type         像素内存类型。
    _texture_pixel_bytes        像素内存类型占用的字节数。

    texture_anisotropy          纹理各向异性比例（公开）。
    _texture_anisotropy         纹理各向异性比例。
    texture_mag_filter          纹理放大滤波器（公开）。
    _texture_mag_filter         纹理放大滤波器。
    texture_min_filter          纹理缩小滤波器（公开）。
    _texture_min_filter         纹理缩小滤波器。
    _texture_max_level          纹理map层次数。
    texture_repeat_x            纹理横向重复比例（公开）。
    _texture_repeat_x           纹理横向重复比例。
    texture_repeat_y            纹理纵向重复比例（公开）。
    _texture_repeat_y           纹理纵向重复比例。
    texture_compare_enum        纹理深度对比函数（文本）。
    _texture_compare_function   纹理深度对比函数。
    texture_swizzle             纹理通道设定。
    """

    def __init__(self, data, width, height, type_mask, pixel_channel_nums,
                 sample_nums=0, alignment=1, depth=False):
        assert not sample_nums & (sample_nums - 1)  # 意味着必须是 2 的 n 次方。
        assert sample_nums <= gl_context.max_samples
        assert alignment in (1, 2, 4, 8)
        assert not (data and sample_nums)  # 不能同时有 data 和 samples 。

        self._texture_data = data
        self._texture_width = width
        self._texture_height = height

        self._texture_depth = depth
        if depth:
            self._texture_base_enum = 'GL_DEPTH_COMPONENT'
            self._texture_base = GL_DEPTH_COMPONENT
            self._texture_internal_enum = 'GL_DEPTH_COMPONENT24'
            self._texture_internal = GL_DEPTH_COMPONENT24
            (_, _, _, _,
             self._texture_pixel_enum, self._texture_pixel_type,
             self._texture_pixel_bytes) = storage_info('float 32', 1)

            self._texture_type_mask = 'float 32'
            self._texture_pixel_channel_nums = 1
            self._texture_compare_function = 'GL_LEQ''UAL'
            self._texture_repeat_x = False
            self._texture_repeat_y = False
        else:
            (self._texture_base_enum, self._texture_base,
             self._texture_internal_enum, self._texture_internal,
             self._texture_pixel_enum, self._texture_pixel_type,
             self._texture_pixel_bytes
             ) = storage_info(type_mask, pixel_channel_nums)

            self._texture_type_mask = type_mask
            self._texture_pixel_channel_nums = pixel_channel_nums
            self._texture_compare_function = 'GL_NONE'
            self._texture_repeat_x = True
            self._texture_repeat_y = True

        self._texture_alignment = alignment
        if data:
            size = (width * pixel_channel_nums * self._texture_pixel_bytes +
                    alignment - 1) // alignment * alignment * height
            assert len(data) == size

        self._texture_sample_nums = sample_nums
        if sample_nums:
            self._texture_target_enum = 'GL_TEXTURE_2D_MULTI''SAMPLE'
            self._texture_target = GL_TEXTURE_2D_MULTISAMPLE
        else:
            self._texture_target_enum = 'GL_TEXTURE_2D'
            self._texture_target = GL_TEXTURE_2D

        self._texture_id = ctypes.c_uint()
        self._texture_max_level = 0
        self._texture_anisotropy = 1.0
        self._texture_min_filter = 'GL_LINEAR'
        self._texture_mag_filter = 'GL_LINEAR'

        OpenGLObject.__init__(self)

    def __repr__(self):
        return self.__string__

    def __str__(self):
        if self._texture_id:
            return ('<{} width={} height={} base={} internal={} type={} '
                    'target={} compare={} anisotropy={} depth={} min_filter='
                    '{} mag_filter={} repeat={}, {}>').format(
                self.__string__, self._texture_width, self._texture_height,
                self._texture_base_enum, self._texture_internal_enum,
                self._texture_pixel_enum, self._texture_target_enum,
                self._texture_compare_function, self._texture_anisotropy,
                self._texture_depth, self._texture_min_filter,
                self._texture_mag_filter, self._texture_repeat_x,
                self._texture_repeat_y
            )
        else:
            return 'wait...'

    def gl_initialize(self) -> str:
        glActiveTexture(gl_context.default_texture_unit)
        glGenTextures(1, self._texture_id)

        if not self._texture_id:
            raise OpenGLError('无法创建 Texture ID')

        glBindTexture(self._texture_target, self._texture_id)
        glTexParameteri(
            self._texture_target, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(
            self._texture_target, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        if self._texture_sample_nums:
            glTexImage2DMultisample(
                self._texture_target, self._texture_sample_nums,
                self._texture_internal, self._texture_width,
                self._texture_height, True)
        else:
            glPixelStorei(GL_PACK_ALIGNMENT, self._texture_alignment)
            glPixelStorei(GL_UNPACK_ALIGNMENT, self._texture_alignment)
            glTexImage2D(
                self._texture_target, 0, self._texture_internal,
                self._texture_width, self._texture_height, 0,
                self._texture_base, self._texture_pixel_type,
                self._texture_data
            )

        if self._texture_depth:
            glTexParameteri(self._texture_target, GL_TEXTURE_COMPARE_MODE,
                            GL_COMPARE_REF_TO_TEXTURE)
            glTexParameteri(
                self._texture_target, GL_TEXTURE_COMPARE_FUNC, GL_LEQUAL)

        return 'texture_%d' % self._texture_id.value

    def gl_release(self):
        glDeleteTextures(1, self._texture_id)

    @property
    def texture_swizzle(self):  # swizzle 有单独的读取方法，所以不需要缓存
        assert not self._texture_depth
        glActiveTexture(gl_context.default_texture_unit)
        glBindTexture(self._texture_target, self)
        swizzle = ctypes.c_int()
        glGetTexParameteriv(
            self._texture_target, GL_TEXTURE_SWIZZLE_R, swizzle)
        r = gl_tostring(swizzle.value)
        glGetTexParameteriv(
            self._texture_target, GL_TEXTURE_SWIZZLE_G, swizzle)
        g = gl_tostring(swizzle.value)
        glGetTexParameteriv(
            self._texture_target, GL_TEXTURE_SWIZZLE_B, swizzle)
        b = gl_tostring(swizzle.value)
        glGetTexParameteriv(
            self._texture_target, GL_TEXTURE_SWIZZLE_A, swizzle)
        a = gl_tostring(swizzle.value)
        return r, g, b, a

    @texture_swizzle.setter
    def texture_swizzle(self, value):
        assert not self._texture_depth
        value = (gl_getattr(i) for i in value)
        try:
            glTexParameteri(
                self._texture_target, GL_TEXTURE_SWIZZLE_R, next(value))
            glTexParameteri(
                self._texture_target, GL_TEXTURE_SWIZZLE_G, next(value))
            glTexParameteri(
                self._texture_target, GL_TEXTURE_SWIZZLE_B, next(value))
            glTexParameteri(
                self._texture_target, GL_TEXTURE_SWIZZLE_A, next(value))
        except StopIteration:
            pass

    @property
    def texture_repeat_x(self):
        return self._texture_repeat_x

    @texture_repeat_x.setter
    def texture_repeat_x(self, value):
        glActiveTexture(gl_context.default_texture_unit)
        glBindTexture(self._texture_target, self)
        if value:
            glTexParameteri(
                self._texture_target, GL_TEXTURE_WRAP_S, GL_REPEAT)
            self._texture_repeat_x = True
        else:
            glTexParameteri(
                self._texture_target, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
            self._texture_repeat_x = False

    @property
    def texture_repeat_y(self):
        return self._texture_repeat_y

    @texture_repeat_y.setter
    def texture_repeat_y(self, value):
        glActiveTexture(gl_context.default_texture_unit)
        glBindTexture(self._texture_target, self)
        if value:
            glTexParameteri(
                self._texture_target, GL_TEXTURE_WRAP_T, GL_REPEAT)
            self._texture_repeat_y = True
        else:
            glTexParameteri(
                self._texture_target, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
            self._texture_repeat_y = False

    @property
    def texture_min_filter(self):
        return self._texture_min_filter

    @texture_min_filter.setter
    def texture_min_filter(self, value):
        glActiveTexture(gl_context.default_texture_unit)
        glBindTexture(self._texture_target, self)
        glTexParameteri(
            self._texture_target, GL_TEXTURE_MIN_FILTER, gl_getattr(value))
        self._texture_min_filter = value

    @property
    def texture_mag_filter(self):
        return self._texture_mag_filter

    @texture_mag_filter.setter
    def texture_mag_filter(self, value):
        glActiveTexture(gl_context.default_texture_unit)
        glBindTexture(self._texture_target, self)
        glTexParameteri(
            self._texture_target, GL_TEXTURE_MAG_FILTER, gl_getattr(value))
        self._texture_mag_filter = value

    @property
    def texture_compare_enum(self):
        assert not self._texture_depth
        return self._texture_compare_function

    @texture_compare_enum.setter
    def texture_compare_enum(self, value):
        assert not self._texture_depth
        assert value in COMPARE_FUNCTION_MASKS
        glActiveTexture(gl_context.default_texture_unit)
        glBindTexture(self._texture_target, self)
        if value == 'GL_NONE':
            glTexParameteri(
                self._texture_target, GL_TEXTURE_COMPARE_MODE, GL_NONE)
        else:
            glTexParameteri(self._texture_target, GL_TEXTURE_COMPARE_MODE,
                            GL_COMPARE_REF_TO_TEXTURE)
            glTexParameteri(self._texture_target, GL_TEXTURE_COMPARE_FUNC,
                            gl_getattr(value))
        self._texture_compare_function = value

    @property
    def texture_anisotropy(self):
        return self._texture_anisotropy

    @texture_anisotropy.setter
    def texture_anisotropy(self, value):
        assert 1.0 <= value <= gl_context.max_anisotropy
        glActiveTexture(gl_context.default_texture_unit)
        glBindTexture(self._texture_target, self)
        glTexParameterf(self._texture_target, GL_TEXTURE_MAX_ANISOTROPY,
                        self._texture_anisotropy)
        self._texture_anisotropy = value

    def __call__(self, target):
        glBindTexture(target, self._texture_id)
