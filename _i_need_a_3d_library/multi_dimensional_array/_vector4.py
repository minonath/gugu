# include "_array.py" /*

import math

from ._array import non_zero, clamp, ctypes_wrap, VOIDP, FLT


@ctypes_wrap(None, VOIDP, FLT, VOIDP)
def vector4_add_scalar(self, other, result):
    """ */

    void vector4_add_scalar(const float *self, float other, float *result) {
        for (int i = 0; i < 4; i++) result[i] = self[i] + other;
    }
    /* """
    result(*(_x + other for _x in self))


@ctypes_wrap(None, VOIDP, VOIDP, VOIDP)
def vector4_add_vector4(self, other, result):
    """ */

    void vector4_add_vector4(const float *self, const float *other,
                             float *result) {
        for (int i = 0; i < 4; i++) result[i] = self[i] + other[i];
    }
    /* """
    result(*(_x + _y for _x, _y in zip(self, other)))


@ctypes_wrap(None, VOIDP, FLT, VOIDP)
def vector4_sub_scalar(self, other, result):
    """ */

    void vector4_sub_scalar(const float *self, float other, float *result) {
        for (int i = 0; i < 4; i++) result[i] = self[i] - other;
    }
    /* """
    result(*(_x - other for _x in self))


@ctypes_wrap(None, VOIDP, VOIDP, VOIDP)
def vector4_sub_vector4(self, other, result):
    """ */

    void vector4_sub_vector4(const float *self, const float *other,
                             float *result) {
        for (int i = 0; i < 4; i++) result[i] = self[i] - other[i];
    }
    /* """
    result(*(_x - _y for _x, _y in zip(self, other)))


@ctypes_wrap(None, VOIDP, FLT, VOIDP)
def vector4_mul_scalar(self, other, result):
    """ */

    void vector4_mul_scalar(const float *self, float other, float *result) {
        for (int i = 0; i < 4; i++) result[i] = self[i] * other;
    }
    /* """
    result(*(_x * other for _x in self))


@ctypes_wrap(None, VOIDP, VOIDP, VOIDP)
def vector4_mul_matrix4(self, matrix4, result):
    """ */

    void vector4_mul_matrix4(const float *self, const float *matrix4,
                             float *result) {
        float cache[4] = {
            matrix4[0] * self[0] + matrix4[4] * self[1] +
            matrix4[8] * self[2] + matrix4[12] * self[3],
            matrix4[1] * self[0] + matrix4[5] * self[1] +
            matrix4[9] * self[2] + matrix4[13] * self[3],
            matrix4[2] * self[0] + matrix4[6] * self[1] +
            matrix4[10] * self[2] + matrix4[14] * self[3],
            matrix4[3] * self[0] + matrix4[7] * self[1] +
            matrix4[11] * self[2] + matrix4[15] * self[3]
        };
        memcpy(result, cache, 4 * sizeof(float));
    }
    /* """
    _x, _y, _z, _w = self
    (_m11, _m21, _m31, _m41, _m12, _m22, _m32, _m42,
     _m13, _m23, _m33, _m43, _m14, _m24, _m34, _m44) = matrix4

    result(
        _m11 * _x + _m12 * _y + _m13 * _z + _m14 * _w,
        _m21 * _x + _m22 * _y + _m23 * _z + _m24 * _w,
        _m31 * _x + _m32 * _y + _m33 * _z + _m34 * _w,
        _m41 * _x + _m42 * _y + _m43 * _z + _m44 * _w
    )


@ctypes_wrap(None, VOIDP, FLT, VOIDP)
def vector4_div_scalar(self, other, result):
    """ */

    void vector4_div_scalar(const float *self, float other, float *result) {
        for (int i = 0; i < 4; i++) result[i] = self[i] / non_zero(other);
    }
    /* """
    result(*(_x / non_zero(other) for _x in self))


@ctypes_wrap(None, VOIDP, VOIDP)
def vector4_from_quaternion(quaternion, result):
    """ */

    void vector4_from_quaternion(const float *quaternion, float *result) {
        float _t = non_zero(sqrtf(1.0f - quaternion[3] * quaternion[3]));

        result[0] = quaternion[0] / _t;
        result[1] = quaternion[1] / _t;
        result[2] = quaternion[2] / _t;
        result[3] = 2.0f * acosf(quaternion[3]);
    }
    /* """
    _x, _y, _z, _w = quaternion
    _t = non_zero((1 - _w ** 2) ** 0.5)
    result(_x / _t, _y / _t, _z / _t, 2 * math.acos(_w))


@ctypes_wrap(None, VOIDP, VOIDP)
def vector4_from_matrix4(matrix4, result):
    """ */

    void vector4_from_matrix4(const float *matrix4, float *result) {
        float _a = matrix4[6] - matrix4[9], _b = matrix4[8] - matrix4[2],
                _c = matrix4[1] - matrix4[4];
        float _s = non_zero(sqrtf(_a * _a + _b * _b + _c * _c));
        result[0] = _a / _s;
        result[1] = _b / _s;
        result[2] = _c / _s;
        result[3] = acosf(matrix4[0] + matrix4[5] + matrix4[10] - 1.0f) * 0.5f;
    }
    /* """
    (_m11, _m21, _m31, _, _m12, _m22, _m32, _,
     _m13, _m23, _m33, _, _, _, _, _) = matrix4

    _s = non_zero(((_m32 - _m23) * (_m32 - _m23) +
                   (_m13 - _m31) * (_m13 - _m31) +
                   (_m21 - _m12) * (_m21 - _m12)) ** 0.5)

    result((_m32 - _m23) / _s, (_m13 - _m31) / _s, (_m21 - _m12) / _s,
           math.acos((_m11 + _m22 + _m33 - 1) / 2))


@ctypes_wrap(None, VOIDP, VOIDP, VOIDP)
def vector4_min_vector4(self, other, result):
    """ */

    void vector4_min_vector4(const float *self, const float *other,
                             float *result) {
        for (int i = 0; i < 4; i++) result[i] = min(self[i], other[i]);
    }
    /* """
    result(*(min(_x, _y) for _x, _y in zip(self, other)))


@ctypes_wrap(None, VOIDP, VOIDP, VOIDP)
def vector4_max_vector4(self, other, result):
    """ */

    void vector4_max_vector4(const float *self, const float *other,
                             float *result) {
        for (int i = 0; i < 4; i++) result[i] = max(self[i], other[i]);
    }
    /* """
    result(*(max(_x, _y) for _x, _y in zip(self, other)))


@ctypes_wrap(None, VOIDP, FLT, FLT, VOIDP)
def vector4_clamp_scalar(self, scalar_min, scalar_max, result):
    """ */

    void vector4_clamp_scalar(const float *self, float scalar_min,
                              float scalar_max, float *result) {
        for (int i = 0; i < 4; i++)
            result[i] = clamp(self[i], scalar_min, scalar_max);
    }
    /* """
    result(*(clamp(_x, scalar_min, scalar_max) for _x in self))


@ctypes_wrap(None, VOIDP, FLT, FLT, VOIDP)
def vector4_clamp_length(self, length_min, length_max, result):
    """ */

    void vector4_clamp_length(const float *self, float length_min,
                              float length_max, float *result) {
        float length = vector4_length(self);
        if (length != 0.0f) {
            length = clamp(length, length_min, length_max) / length;
            for (int i = 0; i < 4; i++) result[i] = self[i] * length;
        }
    }
    /* """
    _length = vector4_length(self)
    if _length:
        _ratio = clamp(_length, length_min, length_max) / _length
        vector4_mul_scalar(self, _ratio, result)


@ctypes_wrap(None, VOIDP, VOIDP, VOIDP, VOIDP)
def vector4_clamp_vector4(self, other_min, other_max, result):
    """ */

    void vector4_clamp_vector4(const float *self, float *other_min,
                               float *other_max, float *result) {
        for (int i = 0; i < 4; i++)
            result[i] = clamp(self[i], other_min[i], other_max[i]);
    }
    /* """
    result(*(clamp(_x, _y, _z) for _x, _y, _z in
             zip(self, other_min, other_max)))


@ctypes_wrap(None, VOIDP, VOIDP)
def vector4_floor(self, result):
    """ */

    void vector4_floor(const float *self, float *result) {
        for (int i = 0; i < 4; i++) result[i] = floorf(self[i]);
    }
    /* """
    result(*(math.floor(_x) for _x in self))


@ctypes_wrap(None, VOIDP, VOIDP)
def vector4_ceil(self, result):
    """ */

    void vector4_ceil(const float *self, float *result) {
        for (int i = 0; i < 4; i++) result[i] = ceilf(self[i]);
    }
    /* """
    result(*(math.ceil(_x) for _x in self))


@ctypes_wrap(None, VOIDP, VOIDP)
def vector4_round(self, result):
    """ */

    void vector4_round(const float *self, float *result) {
        for (int i = 0; i < 4; i++) result[i] = roundf(self[i]);
    }
    /* """
    result(*(round(_x) for _x in self))


@ctypes_wrap(None, VOIDP, VOIDP)
def vector4_trunc(self, result):
    """ */

    void vector4_trunc(const float *self, float *result) {
        for (int i = 0; i < 4; i++) result[i] = truncf(self[i]);
    }
    /* """
    result(*(math.trunc(_x) for _x in self))


@ctypes_wrap(None, VOIDP, VOIDP)
def vector4_negate(self, result):
    """ */

    void vector4_negate(const float *self, float *result) {
        for (int i = 0; i < 4; i++) result[i] = -self[i];
    }
    /* """
    result(*(-_x for _x in self))


@ctypes_wrap(FLT, VOIDP, VOIDP)
def vector4_dot_vector4(self, other):
    """ */

    float vector4_dot_vector4(const float *self, const float *other) {
        return self[0] * other[0] + self[1] * other[1] + self[2] * other[2] +
               self[3] * other[3];
    }
    /* """
    return sum(_x * _y for _x, _y in zip(self, other))


@ctypes_wrap(FLT, VOIDP)
def vector4_length_squared(self):
    """ */

    float vector4_length_squared(const float *self) {
        return self[0] * self[0] + self[1] * self[1] + self[2] * self[2] +
               self[3] * self[3];
    }
    /* """
    return sum(_x ** 2 for _x in self)


@ctypes_wrap(FLT, VOIDP)
def vector4_length(self):
    """ */

    float vector4_length(const float *self) {
        return sqrtf(vector4_length_squared(self));
    }
    /* """
    return sum(_x ** 2 for _x in self) ** 0.5


@ctypes_wrap(FLT, VOIDP)
def vector4_length_manhattan(self):
    """ */

    float vector4_length_manhattan(const float *self) {
        return fabsf(self[0]) + fabsf(self[1]) + fabsf(self[2]) +
               fabsf(self[3]);
    }
    /* """
    return sum(abs(_x) for _x in self)


@ctypes_wrap(None, VOIDP, VOIDP)
def vector4_normalize(self, result):
    """ */

    void vector4_normalize(const float *self, float *result) {
        float length = vector4_length(self);
        if (length != 0.0f)
            for (int i = 0; i < 4; i++) result[i] = self[i] / length;
    }
    /* """
    _length = vector4_length(self)
    if _length:
        result(*(_x / _length for _x in self))


@ctypes_wrap(None, VOIDP, VOIDP, FLT, VOIDP)
def vector4_interpolation(self, other, alpha, result):
    """ */

    void vector4_interpolation(const float *self, const float *other,
                               float alpha, float *result) {
        float beta = 1.0f - alpha;
        for (int i = 0; i < 4; i++)
            result[i] = other[i] * alpha + self[i] * beta;
    }
    /* """
    result(*(_x + (_y - _x) * alpha for _x, _y in zip(self, other)))

# */
