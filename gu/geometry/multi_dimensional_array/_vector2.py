# include "_array.py" /*

import math

from ._array import non_zero, clamp, ctypes_wrap, VOIDP, FLT


@ctypes_wrap(None, VOIDP, FLT, VOIDP)
def vector2_add_scalar(self, other, result):
    """ */

    void vector2_add_scalar(const float *self, float other, float *result) {
        for (int i = 0; i < 2; i++) result[i] = self[i] + other;
    }
    /* """
    result(*(_x + other for _x in self))


@ctypes_wrap(None, VOIDP, VOIDP, VOIDP)
def vector2_add_vector2(self, other, result):
    """ */

    void vector2_add_vector2(const float *self, const float *other,
                             float *result) {
        for (int i = 0; i < 2; i++) result[i] = self[i] + other[i];
    }
    /* """
    result(*(_x + _y for _x, _y in zip(self, other)))


@ctypes_wrap(None, VOIDP, FLT, VOIDP)
def vector2_sub_scalar(self, other, result):
    """ */

    void vector2_sub_scalar(const float *self, float other, float *result) {
        for (int i = 0; i < 2; i++) result[i] = self[i] - other;
    }
    /* """
    result(*(_x - other for _x in self))


@ctypes_wrap(None, VOIDP, VOIDP, VOIDP)
def vector2_sub_vector2(self, other, result):
    """ */

    void vector2_sub_vector2(const float *self, const float *other,
                             float *result) {
        for (int i = 0; i < 2; i++) result[i] = self[i] - other[i];
    }
    /* """
    result(*(_x - _y for _x, _y in zip(self, other)))


@ctypes_wrap(None, VOIDP, FLT, VOIDP)
def vector2_mul_scalar(self, other, result):
    """ */

    void vector2_mul_scalar(const float *self, float other, float *result) {
        for (int i = 0; i < 2; i++) result[i] = self[i] * other;
    }
    /* """
    result(*(_x * other for _x in self))


@ctypes_wrap(None, VOIDP, VOIDP, VOIDP)
def vector2_mul_vector2(self, other, result):
    """ */

    void vector2_mul_vector2(const float *self, const float *other,
                             float *result) {
        for (int i = 0; i < 2; i++) result[i] = self[i] * other[i];
    }
    /* """
    result(*(_x * _y for _x, _y in zip(self, other)))


@ctypes_wrap(None, VOIDP, VOIDP, VOIDP)
def vector2_mul_matrix3(self, matrix3, result):
    """ */

    void vector2_mul_matrix3(const float *self, const float *matrix3,
                             float *result) {
        float a = matrix3[0] * self[0] + matrix3[3] * self[1] + matrix3[6];
        float b = matrix3[1] * self[0] + matrix3[4] * self[1] + matrix3[7];
        result[0] = a; result[1] = b;
    }
    /* """
    _x, _y = self
    _m11, _m21, _, _m12, _m22, _, _m13, _m23, _ = matrix3
    result(_m11 * _x + _m12 * _y + _m13, _m21 * _x + _m22 * _y + _m23)


@ctypes_wrap(None, VOIDP, FLT, VOIDP)
def vector2_div_scalar(self, other, result):
    """ */

    void vector2_div_scalar(const float *self, float other, float *result) {
        for (int i = 0; i < 2; i++) result[i] = self[i] / non_zero(other);
    }
    /* """
    result(*(_x / non_zero(other) for _x in self))


@ctypes_wrap(None, VOIDP, VOIDP, VOIDP)
def vector2_div_vector2(self, other, result):
    """ */

    void vector2_div_vector2(const float *self, const float *other,
                             float *result) {
        for (int i = 0; i < 2; i++) result[i] = self[i] / non_zero(other[i]);
    }
    /* """
    result(*(_x / non_zero(_y) for _x, _y in zip(self, other)))


@ctypes_wrap(None, VOIDP, VOIDP, VOIDP)
def vector2_min_vector2(self, other, result):
    """ */

    void vector2_min_vector2(const float *self, const float *other,
                             float *result) {
        for (int i = 0; i < 2; i++) result[i] = min(self[i], other[i]);
    }
    /* """
    result(*(min(_x, _y) for _x, _y in zip(self, other)))


@ctypes_wrap(None, VOIDP, VOIDP, VOIDP)
def vector2_max_vector2(self, other, result):
    """ */

    void vector2_max_vector2(const float *self, const float *other,
                             float *result) {
        for (int i = 0; i < 2; i++) result[i] = max(self[i], other[i]);
    }
    /* """
    result(*(max(_x, _y) for _x, _y in zip(self, other)))


@ctypes_wrap(None, VOIDP, FLT, FLT, VOIDP)
def vector2_clamp_scalar(self, scalar_min, scalar_max, result):
    """ */

    void vector2_clamp_scalar(const float *self, float scalar_min,
                              float scalar_max, float *result) {
        for (int i = 0; i < 2; i++)
            result[i] = clamp(self[i], scalar_min, scalar_max);
    }
    /* """
    result(*(clamp(_x, scalar_min, scalar_max) for _x in self))


@ctypes_wrap(None, VOIDP, FLT, FLT, VOIDP)
def vector2_clamp_length(self, length_min, length_max, result):
    """ */

    void vector2_clamp_length(const float *self, float length_min,
                              float length_max, float *result) {
        float length = vector2_length(self);
        if (length != 0.0f) {
            length = clamp(length, length_min, length_max) / length;
            for (int i = 0; i < 2; i++) result[i] = self[i] * length;
        }
    }
    /* """
    _length = vector2_length(self)
    if _length:
        _ratio = clamp(_length, length_min, length_max) / _length
        vector2_mul_scalar(self, _ratio, result)


@ctypes_wrap(None, VOIDP, VOIDP, VOIDP, VOIDP)
def vector2_clamp_vector2(self, other_min, other_max, result):
    """ */

    void vector2_clamp_vector2(const float *self, const float *other_min,
                               const float *other_max, float *result) {
        for (int i = 0; i < 2; i++)
            result[i] = clamp(self[i], other_min[i], other_max[i]);
    }
    /* """
    result(*(clamp(_x, _y, _z) for _x, _y, _z in
             zip(self, other_min, other_max)))


@ctypes_wrap(None, VOIDP, VOIDP)
def vector2_floor(self, result):
    """ */

    void vector2_floor(const float *self, float *result) {
        for (int i = 0; i < 2; i++) result[i] = floorf(self[i]);
    }
    /* """
    result(*(math.floor(_x) for _x in self))


@ctypes_wrap(None, VOIDP, VOIDP)
def vector2_ceil(self, result):
    """ */

    void vector2_ceil(const float *self, float *result) {
        for (int i = 0; i < 2; i++) result[i] = ceilf(self[i]);
    }
    /* """
    result(*(math.ceil(_x) for _x in self))


@ctypes_wrap(None, VOIDP, VOIDP)
def vector2_round(self, result):
    """ */

    void vector2_round(const float *self, float *result) {
        for (int i = 0; i < 2; i++) result[i] = roundf(self[i]);
    }
    /* """
    result(*(round(_x) for _x in self))


@ctypes_wrap(None, VOIDP, VOIDP)
def vector2_trunc(self, result):
    """ */

    void vector2_trunc(const float *self, float *result) {
        for (int i = 0; i < 2; i++) result[i] = truncf(self[i]);
    }
    /* """
    result(*(math.trunc(_x) for _x in self))


@ctypes_wrap(None, VOIDP, VOIDP)
def vector2_negate(self, result):
    """ */

    void vector2_negate(const float *self, float *result) {
        for (int i = 0; i < 2; i++) result[i] = -self[i];
    }
    /* """
    result(*(-_x for _x in self))


@ctypes_wrap(FLT, VOIDP, VOIDP)
def vector2_dot_vector2(self, other):
    """ */

    float vector2_dot_vector2(const float *self, const float *other) {
        return self[0] * other[0] + self[1] * other[1];
    }
    /* """
    return sum(_x * _y for _x, _y in zip(self, other))


@ctypes_wrap(FLT, VOIDP, VOIDP)
def vector2_cross_vector2(self, other):
    """ */

    float vector2_cross_vector2(const float *self, const float *other) {
        return self[0] * other[1] - self[1] * other[0];
    }
    /* """
    return self[0] * other[1] - self[1] * other[0]


@ctypes_wrap(FLT, VOIDP)
def vector2_length_squared(self):
    """ */

    float vector2_length_squared(const float *self) {
        return self[0] * self[0] + self[1] * self[1];
    }
    /* """
    return sum(_x ** 2 for _x in self)


@ctypes_wrap(FLT, VOIDP)
def vector2_length(self):
    """ */

    float vector2_length(const float *self) {
        return sqrtf(vector2_length_squared(self));
    }
    /* """
    return sum(_x ** 2 for _x in self) ** 0.5


@ctypes_wrap(FLT, VOIDP)
def vector2_length_manhattan(self):
    """ */

    float vector2_length_manhattan(const float *self) {
        return fabsf(self[0]) + fabsf(self[1]);
    }
    /* """
    return sum(abs(_x) for _x in self)


@ctypes_wrap(None, VOIDP, VOIDP)
def vector2_normalize(self, result):
    """ */

    void vector2_normalize(const float *self, float *result) {
        float _length = vector2_length(self);
        if (_length != 0.0f)
            for (int i = 0; i < 2; i++) result[i] = self[i] / _length;
    }
    /* """
    _length = vector2_length(self)
    if _length:
        result(*(_x / _length for _x in self))


@ctypes_wrap(FLT, VOIDP)
def vector2_angle(self):
    """ */

    float vector2_angle(const float *self) {
        float _angle = atan2f(self[1], self[0]);
        if (_angle < 0.0f)
            _angle += 2.0f * GU_PI;

        return _angle;
    }
    /* """
    _angle = math.atan2(self[1], self[0])
    if _angle < 0:
        _angle += 2 * math.pi

    return _angle


@ctypes_wrap(FLT, VOIDP, VOIDP)
def vector2_distance_squared_to_vector2(self, other):
    """ */

    float vector2_distance_squared_to_vector2(const float *self,
                                              const float *other) {
        vector2_sub_vector2(self, other, vector2_0);
        return vector2_length_squared(vector2_0);
    }
    /* """
    return sum((_x - _y) ** 2 for _x, _y in zip(self, other))


@ctypes_wrap(FLT, VOIDP, VOIDP)
def vector2_distance_to_vector2(self, other):
    """ */

    float vector2_distance_to_vector2(const float *self, const float *other) {
        return sqrtf(vector2_distance_squared_to_vector2(self, other));
    }
    /* """
    return math.sqrt(vector2_distance_squared_to_vector2(self, other))


@ctypes_wrap(FLT, VOIDP, VOIDP)
def vector2_distance_manhattan_to_vector2(self, other):
    """ */

    float vector2_distance_manhattan_to_vector2(const float *self,
                                                const float *other) {
        vector2_sub_vector2(self, other, vector2_0);
        return vector2_length_manhattan(vector2_0);
    }
    /* """
    return sum(abs(_x - _y) for _x, _y in zip(self, other))


@ctypes_wrap(None, VOIDP, VOIDP, FLT, VOIDP)
def vector2_interpolation(self, other, alpha, result):
    """ */

    void vector2_interpolation(const float *self, const float *other,
                               float alpha, float *result) {
        float beta = 1.0f - alpha;
        for (int i = 0; i < 2; i++)
            result[i] = other[i] * alpha + self[i] * beta;
    }
    /* """
    result(*(_x + (_y - _x) * alpha for _x, _y in zip(self, other)))


@ctypes_wrap(None, VOIDP, VOIDP, FLT, VOIDP)
def vector2_rotate_around(self, other, angle, result):
    """ */

    void vector2_rotate_around(const float *self, const float *other,
                               float angle, float *result) {
        float _x = self[0] - other[0], _y = self[1] - other[1],
                _c = cosf(angle), _s = sinf(angle);
        result[0] = _x * _c - _y * _s + other[0];
        result[1] = _x * _s + _y * _c + other[1];
    }
    /* """
    _m, _n = other
    _x = self[0] - _m
    _y = self[1] - _n
    _c = math.cos(angle)
    _s = math.sin(angle)

    result(_x * _c - _y * _s + _m, _x * _s + _y * _c + _n)

# */
