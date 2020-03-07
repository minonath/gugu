# ifndef GU_MATH_H
# define GU_MATH_H 1

# include <float.h>
# include <math.h>
# include <string.h>

# ifndef GU_PI
# define GU_PI 3.1415927410125732f
# endif

# ifndef GU_MIN
# define GU_MIN 1.1754943508222875e-38f
# endif

# define xyz 0x00
# define yxz 0x01
# define zxy 0x02
# define zyx 0x04
# define yzx 0x08
# define xzy 0x10 /*

import sys
import ctypes

_c_type = type(ctypes.c_ubyte)
_p_char = ctypes.POINTER(ctypes.c_char)
xyz = 0x00
yxz = 0x01
zxy = 0x02
zyx = 0x04
yzx = 0x08
xzy = 0x10

VOIDP = ctypes.c_void_p
FLT = ctypes.c_float
UNSIGNED = ctypes.c_uint

_types = {
    VOIDP: 'VOIDP',
    FLT: 'FLT',
    UNSIGNED: 'UNSIGNED',
    None: 'None',
}

_functions = {}


def ctypes_wrap(restype, *arg_types):
    def _wrap(_function):
        _functions[_function.__name__] = restype, arg_types
        return _function

    return _wrap


def _float_from_bytes(bytes_array):
    if sys.byteorder == 'big':  # 默认使用 little-endian
        bytes_array = reversed(bytes_array)
    _memory = (ctypes.c_ubyte * 4)(*bytes_array)
    return ctypes.cast(_memory, ctypes.POINTER(ctypes.c_float))[0]


# FLT_MIN * FLT_MAX = 4;  这条需要在 double 的情况下才能计算，否则一直是无限
# FLT_MIN = 0x00008000
# FLT_MAX = 0xffff7f7f
# inf = 0x0000807f 因为误差的缘故，计算 FLT_MAX 的相关总会得到 inf，它们两个只差 1
# nan = 0x0000c0ff 涉及 inf 的计算会得到 nan，表示无法计算的数字

float_nan = _float_from_bytes(b'\x00\x00\xc0\xff')
float_inf = _float_from_bytes(b'\x00\x00\x80\x7f')
float_max = _float_from_bytes(b'\xff\xff\x7f\x7f')
float_min = _float_from_bytes(b'\x00\x00\x80\x00')


class Array(object):
    __length__ = 1

    def __init__(self, *args, length=0, _type=None):
        if not length:
            length = self.__length__
        if not _type:
            _type = ctypes.c_float

        self.__values__ = (_type * length)(*args)
        self.__length__ = length
        self.__e_type__ = _type
        self.__e_size__ = ctypes.sizeof(_type)
        self.__b_size__ = length * self.__e_size__

    @property
    def _as_parameter_(self):  # 用来传递自身的指针
        return ctypes.cast(self.__values__, ctypes.POINTER(ctypes.c_float))

    def __getitem__(self, item):
        return self.__values__[item]

    def __setitem__(self, key, value):
        self.__values__[key] = value

    def __repr__(self):
        return self.__class__.__name__ + '(%s)' % ', '.join(
            '{:.3f}' for _ in range(self.__length__)).format(*self)

    def __call__(self, *args):
        self.__values__[:] = args
        return self

    def __bytes__(self):
        # 这里不能使用 ctypes.c_char_p 的 value 来获取字节，这样会导致在 0x00 终止
        return ctypes.cast(self.__values__, _p_char)[:self.__b_size__]

    @property
    def array_length(self) -> int:  # 对应 Attribute 读取数组长度
        return self.__length__

    @property
    def array_size(self) -> int:  # 对应 Attribute 读取数组字节长度
        return self.__b_size__

    @property
    def array_element_type(self) -> _c_type:
        return self.__e_type__

    @property
    def array_element_size(self) -> int:  # 对应 Attribute 读取数组元素长度
        return self.__e_size__


vector3_0 = Array(length=3)
vector3_1 = Array(length=3)
vector3_2 = Array(length=3)
quaternion_0 = Array(length=4)
matrix4_0 = Array(length=16)


def non_zero(number):
    """ */

    static inline float non_zero(float number) {
        if (number == 0.0f) return GU_MIN;
        else return number;
    }
    /* """
    if number == 0:
        return float_min
    return number


def clamp(number, number_min, number_max):
    """ */

    static inline float clamp(float number, float number_min,
                              float number_max) {
        if (number < number_min)
            return number_min;
        else if (number > number_max)
            return number_max;
        else return number;
    }
    /* """
    if number < number_min:
        return number_min
    elif number > number_max:
        return number_max
    else:
        return number


""" */

static inline float min(const float self, const float other) {
    if (self > other) return other;
    else return self;
}

static inline float max(const float self, const float other) {
    if (self < other) return other;
    else return self;
}

static float vector3_0[3], vector3_1[3], vector3_2[3], vector2_0[2],
        matrix4_0[16];

void vector3_add_scalar(const float *self, float other, float *result);

void vector3_add_vector3(const float *self, const float *other,
                         float *result);

void vector3_sub_scalar(const float *self, float other, float *result);

void vector3_sub_vector3(const float *self, const float *other,
                         float *result);

void vector3_mul_scalar(const float *self, float other, float *result);

void vector3_mul_vector3(const float *self, const float *other,
                         float *result);

void vector3_mul_matrix3(const float *self, const float *other,
                         float *result);

void vector3_mul_matrix4(const float *self, const float *other,
                         float *result);

void vector3_mul_quaternion(const float *self, const float *other,
                            float *result);

void vector3_transform_direction(const float *self, const float *other,
                                 float *result);

void vector3_div_scalar(const float *self, float other, float *result);

void vector3_div_vector3(const float *self, const float *other,
                         float *result);

void vector3_min_vector3(const float *self, const float *other,
                         float *result);

void vector3_max_vector3(const float *self, const float *other,
                         float *result);

void vector3_clamp_scalar(const float *self, float scalar_min,
                          float scalar_max, float *result);

void vector3_clamp_length(const float *self, float length_min,
                          float length_max, float *result);

void vector3_clamp_vector3(const float *self, const float *other_min,
                           const float *other_max, float *result);

void vector3_floor(const float *self, float *result);

void vector3_ceil(const float *self, float *result);

void vector3_round(const float *self, float *result);

void vector3_trunc(const float *self, float *result);

void vector3_negate(const float *self, float *result);

float vector3_dot_vector3(const float *self, const float *other);

float vector3_length_squared(const float *self);

float vector3_length(const float *self);

float vector3_length_manhattan(const float *self);

void vector3_normalize(const float *self, float *result);

void vector3_interpolation(const float *self, const float *other,
                           float alpha, float *result);

void vector3_cross_vector3(const float *self, const float *other,
                           float *result);

void vector3_project_vector3(const float *self, const float *other,
                             float *result);

void vector3_reflect(const float *self, const float *normal, float *result);

float vector3_angle_to_vector3(const float *self, const float *other);

float vector3_distance_squared_to_vector3(const float *self,
                                          const float *other);

float vector3_distance_to_vector3(const float *self, const float *other);

float vector3_distance_manhattan_to_vector3(const float *self,
                                            const float *other);

void vector3_from_spherical(float radius, float phi,
                            float theta, float *result);

void vector3_from_cylindrical(float radius, float theta,
                              float y, float *result);

void vector3_from_matrix4_offset(const float *matrix4, unsigned offset,
                                 float *result);

void vector3_from_matrix4_scale(const float *matrix4, float *result);

void vector2_add_scalar(const float *self, float other, float *result);

void vector2_add_vector2(const float *self, const float *other,
                         float *result);

void vector2_sub_scalar(const float *self, float other, float *result);

void vector2_sub_vector2(const float *self, const float *other,
                         float *result);

void vector2_mul_scalar(const float *self, float other, float *result);

void vector2_mul_vector2(const float *self, const float *other,
                         float *result);

void vector2_mul_matrix3(const float *self, const float *matrix3,
                         float *result);

void vector2_div_scalar(const float *self, float other, float *result);

void vector2_div_vector2(const float *self, const float *other,
                         float *result);

void vector2_min_vector2(const float *self, const float *other,
                         float *result);

void vector2_max_vector2(const float *self, const float *other,
                         float *result);

void vector2_clamp_scalar(const float *self, float scalar_min,
                          float scalar_max, float *result);

void vector2_clamp_length(const float *self, float length_min,
                          float length_max, float *result);

void vector2_clamp_vector2(const float *self, const float *other_min,
                           const float *other_max, float *result);

void vector2_floor(const float *self, float *result);

void vector2_ceil(const float *self, float *result);

void vector2_round(const float *self, float *result);

void vector2_trunc(const float *self, float *result);

void vector2_negate(const float *self, float *result);

float vector2_dot_vector2(const float *self, const float *other);

float vector2_cross_vector2(const float *self, const float *other);

float vector2_length_squared(const float *self);

float vector2_length(const float *self);

float vector2_length_manhattan(const float *self);

void vector2_normalize(const float *self, float *result);

float vector2_angle(const float *self);

float vector2_distance_squared_to_vector2(const float *self,
                                          const float *other);

float vector2_distance_to_vector2(const float *self, const float *other);

float vector2_distance_manhattan_to_vector2(const float *self,
                                            const float *other);

void vector2_interpolation(const float *self, const float *other,
                           float alpha, float *result);

void vector2_rotate_around(const float *self, const float *other,
                           float angle, float *result);

void vector4_add_scalar(const float *self, float other, float *result);

void vector4_add_vector4(const float *self, const float *other,
                         float *result);

void vector4_sub_scalar(const float *self, float other, float *result);

void vector4_sub_vector4(const float *self, const float *other,
                         float *result);

void vector4_mul_scalar(const float *self, float other, float *result);

void vector4_mul_matrix4(const float *self, const float *matrix4,
                         float *result);

void vector4_div_scalar(const float *self, float other, float *result);

void vector4_from_quaternion(const float *quaternion, float *result);

void vector4_from_matrix4(const float *matrix4, float *result);

void vector4_min_vector4(const float *self, const float *other,
                         float *result);

void vector4_max_vector4(const float *self, const float *other,
                         float *result);

void vector4_clamp_scalar(const float *self, float scalar_min,
                          float scalar_max, float *result);

void vector4_clamp_length(const float *self, float length_min,
                          float length_max, float *result);

void vector4_clamp_vector4(const float *self, float *other_min,
                           float *other_max, float *result);

void vector4_floor(const float *self, float *result);

void vector4_ceil(const float *self, float *result);

void vector4_round(const float *self, float *result);

void vector4_trunc(const float *self, float *result);

void vector4_negate(const float *self, float *result);

float vector4_dot_vector4(const float *self, const float *other);

float vector4_length_squared(const float *self);

float vector4_length(const float *self);

float vector4_length_manhattan(const float *self);

void vector4_normalize(const float *self, float *result);

void vector4_interpolation(const float *self, const float *other,
                           float alpha, float *result);

void quaternion_from_euler(const float *euler, unsigned order,
                           float *result);

void quaternion_from_axis_angle(const float *axis_angle, float *result);

void quaternion_from_matrix4_rotation(const float *matrix4, float *result);

void quaternion_from_unit_vector3(const float *vector3_f,
                                  const float *vector3_t, float *result);

float quaternion_angle_to_quaternion(const float *self, const float *other);

void quaternion_rotate_towards(const float *self, const float *other,
                               float step, float *result);

void quaternion_conjugate(const float *self, float *result);

float quaternion_dot_quaternion(const float *self, const float *other);

float quaternion_length_squared(const float *self);

float quaternion_length(const float *self);

void quaternion_normalize(const float *self, float *result);

void quaternion_mul_quaternion(const float *self, const float *other,
                               float *result);

void quaternion_spherical_linear_interpolation(
        const float *self, const float *other, float alpha, float *result);

void euler_from_matrix4(const float *matrix4, unsigned order, float *result);

void matrix3_from_identity(float *result);

void matrix3_from_matrix4(const float *matrix4, float *result);

void matrix3_mul_matrix3(const float *self, const float *other,
                         float *result);

void matrix3_mul_scalar(const float *self, float other, float *result);

float matrix3_determinant(const float *self);

void matrix3_inverse(const float *self, float *result);

void matrix3_transpose(const float *self, float *result);

void matrix3_from_uv_transform(float tx, float ty, float sx, float sy,
                               float rotation, float cx, float cy,
                               float *result);

void matrix3_scale(const float *self, float sx, float sy, float *result);

void matrix3_rotate(const float *self, float theta, float *result);

void matrix3_translate(const float *self, float tx, float ty,
                       float *result);

void matrix4_from_identity(float *result);

void matrix4_from_basis(const float *axis_a, const float *axis_b,
                        const float *axis_c, float *result);

void matrix4_from_matrix3_as_rotation(const float *matrix3, float *result);

void matrix4_from_euler(const float *euler, unsigned order, float *result);

void matrix4_from_quaternion(const float *quaternion, float *result);

void matrix4_from_look_at(const float *eye, const float *target,
                          const float *up, float *result);

void matrix4_mul_matrix4(const float *self, const float *other,
                         float *result);

void matrix4_mul_scalar(const float *self, float other, float *result);

float matrix4_determinant(const float *self);

void matrix4_transpose(const float *self, float *result);

void matrix4_inverse(const float *self, float *result);

void matrix4_scale_vector3(const float *self, const float *vector3,
                           float *result);

float matrix4_max_scale(const float *self);

void matrix4_from_translation(float x, float y, float z, float *result);

void matrix4_from_rotation_x(float theta, float *result);

void matrix4_from_rotation_y(float theta, float *result);

void matrix4_from_rotation_z(float theta, float *result);

void matrix4_from_rotation(const float *axis, float angle, float *result);

void matrix4_from_scale(float x, float y, float z, float *result);

void matrix4_from_shear(float x, float y, float z, float *result);

void matrix4_from_compose(const float *position, const float *rotation,
                          const float *scale, float *result);

void matrix4_to_decompose(const float *self, float *position,
                          float *rotation, float *scale);

void matrix4_from_perspective_bounds(
        float left, float right, float bottom, float top, float near,
        float far, float *result);

void matrix4_from_orthogonal(
        float left, float right, float bottom, float top, float near,
        float far, float *result);

/* """

# */

# endif //GU_MATH_H
