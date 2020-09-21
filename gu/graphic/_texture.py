import ctypes

from ._context import gl_context
from ._buffer import Buffer
from ..opengl import *
from ..system import OpenGLObject, Array, Type


class Compare:
    LessOrEqual = '<='
    Less = '<'
    GreaterOrEqual = '>='
    Greater = '>'
    Equal = '='
    Never = '0'
    Always = '1'

    COMPARE_MODES = {
        LessOrEqual: GL_LEQUAL,
        Less: GL_LESS,
        GreaterOrEqual: GL_GEQUAL,
        Greater: GL_GREATER,
        Equal: GL_EQUAL,
        Never: GL_NEVER,
        Always: GL_ALWAYS
    }


class Filter:
    Linear = 'linear'
    Nearest = 'nearest'
    LLinear = 'l_linear'
    LNearest = 'l_nearest'
    NLinear = 'n_linear'
    NNearest = 'n_nearest'

    FILTER_MODES = {
        Linear: GL_LINEAR,
        Nearest: GL_NEAREST,
        LLinear: GL_LINEAR_MIPMAP_LINEAR,
        LNearest: GL_LINEAR_MIPMAP_NEAREST,
        NLinear: GL_NEAREST_MIPMAP_LINEAR,
        NNearest: GL_NEAREST_MIPMAP_NEAREST
    }


class Swizzle:
    Red = 'red'
    Green = 'green'
    Blue = 'blue'
    Alpha = 'alpha'

    SWIZZLE_MODES = {
        Red: GL_RED,
        Green: GL_GREEN,
        Blue: GL_BLUE,
        Alpha: GL_ALPHA
    }
    GL_LIST = (
        GL_TEXTURE_SWIZZLE_R, GL_TEXTURE_SWIZZLE_G,
        GL_TEXTURE_SWIZZLE_B, GL_TEXTURE_SWIZZLE_A
    )


class Texture(OpenGLObject):
    # 基本类型对应 4 种通道模式
    # 一个通道是红色，二个是红绿，三个是红绿蓝，四个是红绿蓝加透明
    _BASE_FLOAT = GL_RED, GL_RG, GL_RGB, GL_RGBA
    # 基本类型对应的整数形式，储存的整数的量，正常 PNG 图片是用整数形式
    _BASE_INT = GL_RED_INTEGER, GL_RG_INTEGER, GL_RGB_INTEGER, GL_RGBA_INTEGER

    # 显卡内部储存格式，需要对应
    _INTERNAL_FLOAT_8 = GL_R8, GL_RG8, GL_RGB8, GL_RGBA8
    _INTERNAL_FLOAT_16 = GL_R16F, GL_RG16F, GL_RGB16F, GL_RGBA16F
    _INTERNAL_FLOAT_32 = GL_R32F, GL_RG32F, GL_RGB32F, GL_RGBA32F
    _INTERNAL_UNSIGNED_8 = GL_R8UI, GL_RG8UI, GL_RGB8UI, GL_RGBA8UI
    _INTERNAL_UNSIGNED_16 = GL_R16UI, GL_RG16UI, GL_RGB16UI, GL_RGBA16UI
    _INTERNAL_UNSIGNED_32 = GL_R32UI, GL_RG32UI, GL_RGB32UI, GL_RGBA32UI
    _INTERNAL_INT_8 = GL_R8I, GL_RG8I, GL_RGB8I, GL_RGBA8I
    _INTERNAL_INT_16 = GL_R16I, GL_RG16I, GL_RGB16I, GL_RGBA16I
    _INTERNAL_INT_32 = GL_R32I, GL_RG32I, GL_RGB32I, GL_RGBA32I

    # TEXTURE STORAGE FORMAT 显卡内部缓存储存文件的格式和尺寸
    Float8 = 'Float8'
    Float16 = 'Float16'
    Float32 = 'Float32'
    UInt8 = 'UInt8'
    UInt16 = 'UInt16'
    UInt32 = 'UInt32'
    Int8 = 'Int8'
    Int16 = 'Int16'
    Int32 = 'Int32'

    _STORAGE_GL_INFO = {
        Float8: (_BASE_FLOAT, _INTERNAL_FLOAT_8, GL_UNSIGNED_BYTE, 1),
        Float16: (_BASE_FLOAT, _INTERNAL_FLOAT_16, GL_HALF_FLOAT, 2),
        Float32: (_BASE_FLOAT, _INTERNAL_FLOAT_32, GL_FLOAT, 4),
        UInt8: (_BASE_INT, _INTERNAL_UNSIGNED_8, GL_UNSIGNED_BYTE, 1),
        UInt16: (_BASE_INT, _INTERNAL_UNSIGNED_16, GL_UNSIGNED_SHORT, 2),
        UInt32: (_BASE_INT, _INTERNAL_UNSIGNED_32, GL_UNSIGNED_INT, 4),
        Int8: (_BASE_INT, _INTERNAL_INT_8, GL_BYTE, 1),
        Int16: (_BASE_INT, _INTERNAL_INT_16, GL_SHORT, 2),
        Int32: (_BASE_INT, _INTERNAL_INT_32, GL_INT, 4)
    }

    @classmethod
    def _texture_info(cls, mask, components):
        _meow = components - 1
        _bases, _internals, _gl_type, _p_bytes = cls._STORAGE_GL_INFO[mask]
        return mask, _bases[_meow], _internals[_meow], _gl_type, _p_bytes

    def __init__(self, data, width, height, type_mask,
                 channels=1, alignment=1, samples=0, depth=False):
        self._texture_max_level = 0
        self._texture_repeat_x = True
        self._texture_repeat_y = True
        self._texture_min_filter = Filter.Linear
        self._texture_mag_filter = Filter.Linear
        self._texture_compare = None
        self._texture_anisotropy = 1.0
        self._texture_swizzle = (
            Swizzle.Red, Swizzle.Green, Swizzle.Blue, Swizzle.Alpha
        )

        OpenGLObject.__init__(self, data, width, height, type_mask,
                              channels, alignment, samples, depth)

    def _initial(self, data, width, height, data_type,
                 channels, alignment, samples, depth):

        assert alignment in (1, 2, 4, 8)
        assert not samples & (samples - 1)  # 意味着必须是 2 的 n 次方
        assert samples <= gl_context.max_samples
        assert not (data and samples)  # 不能同时有 data 和 samples 

        self._texture_width = width
        self._texture_height = height

        self._texture_depth = depth
        if depth:
            self._texture_gl_base = GL_DEPTH_COMPONENT
            self._texture_gl_internal = GL_DEPTH_COMPONENT24
            (self._texture_type, _, _, self._texture_gl_type,
             self._texture_pixel_bytes) = self._texture_info(self.Float32, 1)

            self._texture_channels = 1
            self._texture_compare = Compare.LessOrEqual
            self._texture_repeat_x = False
            self._texture_repeat_y = False

        else:
            (self._texture_type,
             self._texture_gl_base, self._texture_gl_internal,
             self._texture_gl_type, self._texture_pixel_bytes
             ) = self._texture_info(data_type, channels)

            self._texture_channels = channels

        if data:
            _excepted = (width * channels * self._texture_pixel_bytes +
                         alignment - 1) // alignment * alignment * height
            assert len(data) == _excepted

        self._texture_samples = samples
        if samples:
            self._texture_gl_target = GL_TEXTURE_2D_MULTISAMPLE
        else:
            self._texture_gl_target = GL_TEXTURE_2D

        self._texture_id = ctypes.c_uint()
        glActiveTexture(gl_context.default_texture_unit)
        glGenTextures(1, self._texture_id)
        if not self._texture_id:
            raise OpenGLError('无法创建(Texture)对象')

        glBindTexture(self._texture_gl_target, self._texture_id)
        glTexParameteri(
            self._texture_gl_target, GL_TEXTURE_MIN_FILTER, GL_LINEAR
        )
        glTexParameteri(
            self._texture_gl_target, GL_TEXTURE_MAG_FILTER, GL_LINEAR
        )

        if self._texture_samples:
            glTexImage2DMultisample(
                self._texture_gl_target, self._texture_samples,
                self._texture_gl_internal, self._texture_width,
                self._texture_height, True
            )
        else:
            glPixelStorei(GL_PACK_ALIGNMENT, alignment)
            glPixelStorei(GL_UNPACK_ALIGNMENT, alignment)
            glTexImage2D(
                self._texture_gl_target, 0, self._texture_gl_internal,
                self._texture_width, self._texture_height, 0,
                self._texture_gl_base, self._texture_gl_type, data
            )

        if self._texture_depth:
            glTexParameteri(
                self._texture_gl_target, GL_TEXTURE_COMPARE_MODE,
                GL_COMPARE_REF_TO_TEXTURE
            )
            glTexParameteri(
                self._texture_gl_target, GL_TEXTURE_COMPARE_FUNC, GL_LEQUAL
            )

        self._string = (
            '<texture_{} size=({}, {}) type={} samples={} depth={}>'
        ).format(
            self._texture_id.value, self._texture_width, self._texture_height,
            self._texture_type, self._texture_samples, self._texture_depth
        )

    @property
    def _as_parameter_(self):
        return self._texture_id

    def _release(self):
        glDeleteTextures(1, self._texture_id)

    def texture_read(self, data=None, offset=0, level=0, alignment=1):
        """ 把 Texture 写入 Array Buffer 里面 """

        if self._texture_samples:
            return

        assert alignment in (1, 2, 4, 8)
        assert level <= self._texture_max_level

        _width = max(self._texture_width // (1 << level), 1)
        _height = max(self._texture_height // (1 << level), 1)

        _expected = (_width * self._texture_channels *
                     self._texture_pixel_bytes + alignment - 1
                     ) // alignment * alignment * _height
        offset *= self._texture_pixel_bytes
        _expected += offset

        if not data:
            data = self.texture_cache
            if _expected > data.array_bytes:
                data.array_new_size(_expected, new_bytes=True)

        if isinstance(data, Array):
            # 作为 Array 超出了范围，还是可以进行写入，但是会引发内存崩溃
            # 因为范围外的内存不会进行回收，泄露从而导致报错
            assert _expected <= data.array_bytes, _expected
            # raise OverflowError(
            #     'array 长度不足时会泄露内存，需要拥有 %d 的长度，当前为 %d' % (
            #         _expected + offset, data.array_bytes)
            # )

            if offset:
                data = data.array_offset(offset)

            glActiveTexture(gl_context.default_texture_unit)
            glBindTexture(GL_TEXTURE_2D, self._texture_id)
            glPixelStorei(GL_PACK_ALIGNMENT, alignment)
            glPixelStorei(GL_UNPACK_ALIGNMENT, alignment)
            glGetTexImage(
                GL_TEXTURE_2D, level, self._texture_gl_base,
                self._texture_gl_type, data
            )

        elif isinstance(data, Buffer):
            assert _expected <= data.buffer_bytes, _expected
            # raise OverflowError(
            #     'buffer 长度不足时读取会失败，需要拥有 %d 的长度，当前为 %d' % (
            #         _expected + offset, data.buffer_bytes)
            # )
            glBindBuffer(GL_PIXEL_PACK_BUFFER, data)
            glActiveTexture(gl_context.default_texture_unit)
            glBindTexture(GL_TEXTURE_2D, self._texture_id)
            glPixelStorei(GL_PACK_ALIGNMENT, alignment)
            glPixelStorei(GL_UNPACK_ALIGNMENT, alignment)
            glGetTexImage(
                GL_TEXTURE_2D, level, self._texture_gl_base,
                self._texture_gl_type, offset)
            glBindBuffer(GL_PIXEL_PACK_BUFFER, 0)

        else:
            raise NotImplemented

    def texture_write(self, data, viewport=None, level=0, alignment=1):

        assert alignment in (1, 2, 4, 8)
        assert level <= self._texture_max_level
        assert not self._texture_samples

        if viewport:
            _x, _y, _width, _height = viewport
        else:
            _x = _y = 0
            _width = max(self._texture_width // (1 << level), 1)
            _height = max(self._texture_height // (1 << level), 1)

        _expected = (_width * self._texture_channels *
                     self._texture_pixel_bytes + alignment - 1
                     ) // alignment * alignment * _height

        if isinstance(data, Array):
            assert _expected <= data.array_bytes

            glActiveTexture(gl_context.default_texture_unit)
            glBindTexture(self._texture_gl_target, self._texture_id)
            glPixelStorei(GL_PACK_ALIGNMENT, alignment)
            glPixelStorei(GL_UNPACK_ALIGNMENT, alignment)
            glTexSubImage2D(
                self._texture_gl_target, level, _x, _y, _width, _height,
                self._texture_gl_base, self._texture_gl_type, data
            )

        elif isinstance(data, Buffer):
            assert _expected < data.buffer_bytes

            glBindBuffer(GL_PIXEL_UNPACK_BUFFER, data)
            glActiveTexture(gl_context.default_texture_unit)
            glBindTexture(self._texture_gl_target, self._texture_id)
            glPixelStorei(GL_PACK_ALIGNMENT, alignment)
            glPixelStorei(GL_UNPACK_ALIGNMENT, alignment)
            glTexSubImage2D(
                self._texture_gl_target, level, _x, _y, _width, _height,
                self._texture_gl_base, self._texture_gl_type, 0)
            glBindBuffer(GL_PIXEL_UNPACK_BUFFER, 0)

        else:
            raise NotImplemented

    def texture_bind(self, index):
        glActiveTexture(GL_TEXTURE0 + index)
        glBindTexture(self._texture_gl_target, self._texture_id)

    @property
    def texture_cache(self):
        if hasattr(self, '_texture_cache'):
            return self._texture_cache
        else:
            _expected = (self._texture_width * self._texture_channels *
                         self._texture_pixel_bytes * self._texture_height)
            _array = Array(size=_expected, data_type=Type.Char)
            setattr(self, '_texture_cache', _array)
            return _array

    @property
    def texture_viewport(self):
        return 0, 0, self._texture_width, self._texture_height

    @property
    def texture_max_level(self):
        return self._texture_max_level

    @property
    def texture_repeat_x(self):
        return self._texture_repeat_x

    @property
    def texture_repeat_y(self):
        return self._texture_repeat_y

    @property
    def texture_min_filter(self):
        return self._texture_min_filter

    @property
    def texture_mag_filter(self):
        return self._texture_mag_filter

    @property
    def texture_compare_function(self):
        assert not self._texture_depth

        return self._texture_compare

    @property
    def texture_anisotropy(self):
        return self._texture_anisotropy

    @property
    def texture_swizzle(self):
        assert not self._texture_depth

        return self._texture_swizzle

    def texture_build_mip_maps(self, base_level=0, max_level=16):
        assert not self._texture_max_level

        glActiveTexture(gl_context.default_texture_unit)
        glBindTexture(self._texture_gl_target, self._texture_id)

        glTexParameteri(
            self._texture_gl_target, GL_TEXTURE_BASE_LEVEL, base_level
        )
        glTexParameteri(
            self._texture_gl_target, GL_TEXTURE_MAX_LEVEL, max_level
        )

        glGenerateMipmap(self._texture_gl_target)

        glTexParameteri(
            self._texture_gl_target, GL_TEXTURE_MIN_FILTER,
            GL_LINEAR_MIPMAP_LINEAR
        )
        glTexParameteri(
            self._texture_gl_target, GL_TEXTURE_MAG_FILTER, GL_LINEAR
        )

        self._texture_max_level = max_level

    def texture_set_repeat_x(self, value):
        glActiveTexture(gl_context.default_texture_unit)
        glBindTexture(self._texture_gl_target, self._texture_id)
        if value:
            glTexParameteri(
                self._texture_gl_target, GL_TEXTURE_WRAP_S, GL_REPEAT
            )
            self._texture_repeat_x = True

        else:
            glTexParameteri(
                self._texture_gl_target, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE
            )
            self._texture_repeat_x = False

    def texture_set_repeat_y(self, value):
        glActiveTexture(gl_context.default_texture_unit)
        glBindTexture(self._texture_gl_target, self._texture_id)
        if value:
            glTexParameteri(
                self._texture_gl_target, GL_TEXTURE_WRAP_T, GL_REPEAT
            )
            self._texture_repeat_y = True
        else:
            glTexParameteri(
                self._texture_gl_target, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE
            )
            self._texture_repeat_y = False

    def texture_set_min_filter(self, value):
        glActiveTexture(gl_context.default_texture_unit)
        glBindTexture(self._texture_gl_target, self._texture_id)
        glTexParameteri(
            self._texture_gl_target, GL_TEXTURE_MIN_FILTER,
            Filter.FILTER_MODES[value]
        )
        self._texture_min_filter = value

    def texture_set_mag_filter(self, value):
        glActiveTexture(gl_context.default_texture_unit)
        glBindTexture(self._texture_gl_target, self._texture_id)
        glTexParameteri(
            self._texture_gl_target, GL_TEXTURE_MAG_FILTER,
            Filter.FILTER_MODES[value]
        )
        self._texture_mag_filter = value

    def texture_set_compare_function(self, value):
        assert not self._texture_depth

        glActiveTexture(gl_context.default_texture_unit)
        glBindTexture(self._texture_gl_target, self._texture_id)
        if value is None:
            glTexParameteri(
                self._texture_gl_target, GL_TEXTURE_COMPARE_MODE, GL_NONE
            )
            self._texture_compare = None
        else:
            glTexParameteri(
                self._texture_gl_target, GL_TEXTURE_COMPARE_MODE,
                GL_COMPARE_REF_TO_TEXTURE
            )
            glTexParameteri(
                self._texture_gl_target, GL_TEXTURE_COMPARE_FUNC,
                Compare.COMPARE_MODES[value]
            )
            self._texture_compare = value

    def texture_set_anisotropy(self, value):
        assert 1.0 <= value <= gl_context.max_anisotropy

        _value = float(value)
        glActiveTexture(gl_context.default_texture_unit)
        glBindTexture(self._texture_gl_target, self._texture_id)
        glTexParameterf(
            self._texture_gl_target, GL_TEXTURE_MAX_ANISOTROPY, _value
        )
        self._texture_anisotropy = _value

    def texture_set_swizzle(self, *value):
        assert not self._texture_depth

        for _m, _v in zip(Swizzle.GL_LIST, value):
            glTexParameteri(
                self._texture_gl_target, _m, Swizzle.SWIZZLE_MODES[_v]
            )

        self._texture_swizzle = *value, *self.texture_swizzle[len(value):]


__all__ = ['Filter', 'Compare', 'Swizzle', 'Texture']
