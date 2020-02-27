# include "_array.py" /*

import math

from ._array import non_zero, vector3_0, clamp, ctypes_wrap, \
    VOIDP, FLT, UNSIGNED


@ctypes_wrap(None, VOIDP, FLT, VOIDP)
def vector3_add_scalar(self, other, result):
    """ */

    void vector3_add_scalar(const float *self, float other, float *result) {
        for (int i = 0; i < 3; i++) result[i] = self[i] + other;
    }
    /* """
    result(*(_x + other for _x in self))


@ctypes_wrap(None, VOIDP, VOIDP, VOIDP)
def vector3_add_vector3(self, other, result):
    """ */

    void vector3_add_vector3(const float *self, const float *other,
                             float *result) {
        for (int i = 0; i < 3; i++) result[i] = self[i] + other[i];
    }
    /* """
    result(*(_x + _y for _x, _y in zip(self, other)))


@ctypes_wrap(None, VOIDP, FLT, VOIDP)
def vector3_sub_scalar(self, other, result):
    """ */

    void vector3_sub_scalar(const float *self, float other, float *result) {
        for (int i = 0; i < 3; i++) result[i] = self[i] - other;
    }
    /* """
    result(*(_x - other for _x in self))


@ctypes_wrap(None, VOIDP, VOIDP, VOIDP)
def vector3_sub_vector3(self, other, result):
    """ */

    void vector3_sub_vector3(const float *self, const float *other,
                             float *result) {
        for (int i = 0; i < 3; i++) result[i] = self[i] - other[i];
    }
    /* """
    result(*(_x - _y for _x, _y in zip(self, other)))


@ctypes_wrap(None, VOIDP, FLT, VOIDP)
def vector3_mul_scalar(self, other, result):
    """ */

    void vector3_mul_scalar(const float *self, float other, float *result) {
        for (int i = 0; i < 3; i++) result[i] = self[i] * other;
    }
    /* """
    result(*(_x * other for _x in self))


@ctypes_wrap(None, VOIDP, VOIDP, VOIDP)
def vector3_mul_vector3(self, other, result):
    """ */

    void vector3_mul_vector3(const float *self, const float *other,
                             float *result) {
        for (int i = 0; i < 3; i++) result[i] = self[i] * other[i];
    }
    /* """
    result(*(_x * _y for _x, _y in zip(self, other)))


@ctypes_wrap(None, VOIDP, VOIDP, VOIDP)
def vector3_mul_matrix3(self, other, result):
    """ */

    void vector3_mul_matrix3(const float *self, const float *other,
                             float *result) {
        float cache[3] = {
            other[0] * self[0] + other[3] * self[1] + other[6] * self[2],
            other[1] * self[0] + other[4] * self[1] + other[7] * self[2],
            other[2] * self[0] + other[5] * self[1] + other[8] * self[2]
        };
        memcpy(result, cache, 3 * sizeof(float));
    }
    /* """
    _sx, _sy, _sz = self
    _m11, _m21, _m31, _m12, _m22, _m32, _m13, _m23, _m33 = other

    result(
        _m11 * _sx + _m12 * _sy + _m13 * _sz,
        _m21 * _sx + _m22 * _sy + _m23 * _sz,
        _m31 * _sx + _m32 * _sy + _m33 * _sz
    )


@ctypes_wrap(None, VOIDP, VOIDP, VOIDP)
def vector3_mul_matrix4(self, other, result):
    """ */

    void vector3_mul_matrix4(const float *self, const float *other,
                             float *result) {
        float _sw = 1 / non_zero(
            other[3] * self[0] + other[7] * self[1] +
            other[11] * self[2] + other[15]);
        float cache[3] = {
            other[0] * self[0] + other[4] * self[1] +
            other[8] * self[2] + other[12] * _sw,
            other[1] * self[0] + other[5] * self[1] +
            other[9] * self[2] + other[13] * _sw,
            other[2] * self[0] + other[6] * self[1] +
            other[10] * self[2] + other[14] * _sw
        };
        memcpy(result, cache, 3 * sizeof(float));
    }
    /* """
    _sx, _sy, _sz = self
    (_m11, _m21, _m31, _m41, _m12, _m22, _m32, _m42,
     _m13, _m23, _m33, _m43, _m14, _m24, _m34, _m44) = other
    _sw = 1 / non_zero(_m41 * _sx + _m42 * _sy + _m43 * _sz + _m44)

    result(
        _m11 * _sx + _m12 * _sy + _m13 * _sz + _m14 * _sw,
        _m21 * _sx + _m22 * _sy + _m23 * _sz + _m24 * _sw,
        _m31 * _sx + _m32 * _sy + _m33 * _sz + _m34 * _sw
    )


@ctypes_wrap(None, VOIDP, VOIDP, VOIDP)
def vector3_mul_quaternion(self, other, result):
    """ */

    void vector3_mul_quaternion(const float *self, const float *other,
                                float *result) {
        float
            _x = other[3] * self[0] + other[1] * self[2] - other[2] * self[1],
            _y = other[3] * self[1] + other[2] * self[0] - other[0] * self[2],
            _z = other[3] * self[2] + other[0] * self[1] - other[1] * self[0],
            _w = other[0] * self[0] + other[1] * self[1] + other[2] * self[2];

        float cache[3] = {
            _x * other[3] + _w * other[0] - _y * other[2] + _z * other[1],
            _y * other[3] + _w * other[1] - _z * other[0] + _x * other[2],
            _z * other[3] + _w * other[2] - _x * other[1] + _y * other[0]
        };
        memcpy(result, cache, 3 * sizeof(float));
    }
    /* """
    _sx, _sy, _sz = self
    _ox, _oy, _oz, _ow = other

    _x = _ow * _sx + _oy * _sz - _oz * _sy
    _y = _ow * _sy + _oz * _sx - _ox * _sz
    _z = _ow * _sz + _ox * _sy - _oy * _sx
    _w = _ox * _sx + _oy * _sy + _oz * _sz

    result(
        _x * _ow + _w * _ox - _y * _oz + _z * _oy,
        _y * _ow + _w * _oy - _z * _ox + _x * _oz,
        _z * _ow + _w * _oz - _x * _oy + _y * _ox
    )


@ctypes_wrap(None, VOIDP, VOIDP, VOIDP)
def vector3_transform_direction(self, matrix4, result):
    """ */

    void vector3_transform_direction(const float *self, const float *matrix4,
                                     float *result) {
        float cache[3] = {
           matrix4[0] * self[0] + matrix4[4] * self[1] + matrix4[8] * self[2],
           matrix4[1] * self[0] + matrix4[5] * self[1] + matrix4[9] * self[2],
           matrix4[2] * self[0] + matrix4[6] * self[1] + matrix4[10] * self[2]
        };
        vector3_normalize(cache, result);
    }
    /* """
    _x, _y, _z = self
    (_m11, _m21, _m31, _, _m12, _m22, _m32, _,
     _m13, _m23, _m33, _, _, _, _, _) = matrix4

    result(
        _m11 * _x + _m12 * _y + _m13 * _z,
        _m21 * _x + _m22 * _y + _m23 * _z,
        _m31 * _x + _m32 * _y + _m33 * _z
    )

    vector3_normalize(result, result)


@ctypes_wrap(None, VOIDP, FLT, VOIDP)
def vector3_div_scalar(self, other, result):
    """ */

    void vector3_div_scalar(const float *self, float other, float *result) {
        for (int i = 0; i < 3; i++) result[i] = self[i] / non_zero(other);
    }
    /* """
    result(*(_x / non_zero(other) for _x in self))


@ctypes_wrap(None, VOIDP, VOIDP, VOIDP)
def vector3_div_vector3(self, other, result):
    """ */

    void vector3_div_vector3(const float *self, const float *other,
                             float *result) {
        for (int i = 0; i < 3; i++) result[i] = self[i] / non_zero(other[i]);
    }
    /* """
    result(*(_x / non_zero(_y) for _x, _y in zip(self, other)))


@ctypes_wrap(None, VOIDP, VOIDP, VOIDP)
def vector3_min_vector3(self, other, result):
    """ */

    void vector3_min_vector3(const float *self, const float *other,
                             float *result) {
        for (int i = 0; i < 3; i++) result[i] = min(self[i], other[i]);
    }
    /* """
    result(*(min(_x, _y) for _x, _y in zip(self, other)))


@ctypes_wrap(None, VOIDP, VOIDP, VOIDP)
def vector3_max_vector3(self, other, result):
    """ */

    void vector3_max_vector3(const float *self, const float *other,
                             float *result) {
        for (int i = 0; i < 3; i++) result[i] = max(self[i], other[i]);
    }
    /* """
    result(*(max(_x, _y) for _x, _y in zip(self, other)))


@ctypes_wrap(None, VOIDP, FLT, FLT, VOIDP)
def vector3_clamp_scalar(self, scalar_min, scalar_max, result):
    """ */

    void vector3_clamp_scalar(const float *self, float scalar_min,
                              float scalar_max, float *result) {
        for (int i = 0; i < 3; i++)
            result[i] = clamp(self[i], scalar_min, scalar_max);
    }
    /* """
    result(*(clamp(_x, scalar_min, scalar_max) for _x in self))


@ctypes_wrap(None, VOIDP, FLT, FLT, VOIDP)
def vector3_clamp_length(self, length_min, length_max, result):
    """ */

    void vector3_clamp_length(const float *self, float length_min,
                              float length_max, float *result) {
        float _length = vector3_length(self);

        if (_length > 0.0f) {
            float _ratio = clamp(_length, length_min, length_max) / _length;
            for (int i = 0; i < 3; i++) result[i] = self[i] * _ratio;
        }
    }
    /* """
    _length = vector3_length(self)
    if _length:
        _ratio = clamp(_length, length_min, length_max) / _length
        vector3_mul_scalar(self, _ratio, result)


@ctypes_wrap(None, VOIDP, VOIDP, VOIDP, VOIDP)
def vector3_clamp_vector3(self, other_min, other_max, result):
    """ */

    void vector3_clamp_vector3(const float *self, const float *other_min,
                               const float *other_max, float *result) {
        for (int i = 0; i < 3; i++)
            result[i] = clamp(self[i], other_min[i], other_max[i]);
    }
    /* """
    result(*(clamp(_x, _y, _z) for _x, _y, _z in
             zip(self, other_min, other_max)))


@ctypes_wrap(None, VOIDP, VOIDP)
def vector3_floor(self, result):
    """ */

    void vector3_floor(const float *self, float *result) {
        for (int i = 0; i < 3; i++) result[i] = floorf(self[i]);
    }
    /* """
    result(*(math.floor(_x) for _x in self))


@ctypes_wrap(None, VOIDP, VOIDP)
def vector3_ceil(self, result):
    """ */

    void vector3_ceil(const float *self, float *result) {
        for (int i = 0; i < 3; i++) result[i] = ceilf(self[i]);
    }
    /* """
    result(*(math.ceil(_x) for _x in self))


@ctypes_wrap(None, VOIDP, VOIDP)
def vector3_round(self, result):
    """ */

    void vector3_round(const float *self, float *result) {
        for (int i = 0; i < 3; i++) result[i] = roundf(self[i]);
    }
    /* """
    result(*(round(_x) for _x in self))


@ctypes_wrap(None, VOIDP, VOIDP)
def vector3_trunc(self, result):
    """ */

    void vector3_trunc(const float *self, float *result) {
        for (int i = 0; i < 3; i++) result[i] = truncf(self[i]);
    }
    /* """
    result(*(math.trunc(_x) for _x in self))


@ctypes_wrap(None, VOIDP, VOIDP)
def vector3_negate(self, result):
    """ */

    void vector3_negate(const float *self, float *result) {
        for (int i = 0; i < 3; i++) result[i] = -self[i];
    }
    /* """
    result(*(-_x for _x in self))


@ctypes_wrap(FLT, VOIDP, VOIDP)
def vector3_dot_vector3(self, other):
    """ */

    float vector3_dot_vector3(const float *self, const float *other) {
        return self[0] * other[0] + self[1] * other[1] + self[2] * other[2];
    }
    /* """
    return sum(_x * _y for _x, _y in zip(self, other))


@ctypes_wrap(FLT, VOIDP)
def vector3_length_squared(self):
    """ */

    float vector3_length_squared(const float *self) {
        return self[0] * self[0] + self[1] * self[1] + self[2] * self[2];
    }
    /* """
    return sum(_x ** 2 for _x in self)


@ctypes_wrap(FLT, VOIDP)
def vector3_length(self):
    """ */

    float vector3_length(const float *self) {
        return sqrtf(vector3_length_squared(self));
    }
    /* """
    return sum(_x ** 2 for _x in self) ** 0.5


@ctypes_wrap(FLT, VOIDP)
def vector3_length_manhattan(self):
    """ */

    float vector3_length_manhattan(const float *self) {
        return fabsf(self[0]) + fabsf(self[1]) + fabsf(self[2]);
    }
    /* """
    return sum(abs(_x) for _x in self)


@ctypes_wrap(None, VOIDP, VOIDP)
def vector3_normalize(self, result):
    """ */

    void vector3_normalize(const float *self, float *result) {
        float _length = vector3_length(self);
        if (_length > 0.0f)
            for (int i = 0; i < 3; i++) result[i] = self[i] / _length;
    }
    /* """
    _length = vector3_length(self)
    if _length:
        result(*(_x / _length for _x in self))


@ctypes_wrap(None, VOIDP, VOIDP, FLT, VOIDP)
def vector3_interpolation(self, other, alpha, result):
    """ */

    void vector3_interpolation(const float *self, const float *other,
                               float alpha, float *result) {
        float beta = 1.0f - alpha;
        for (int i = 0; i < 3; i++)
            result[i] = other[i] * alpha + self[i] * beta;
    }
    /* """
    result(*(_x + (_y - _x) * alpha for _x, _y in zip(self, other)))


@ctypes_wrap(None, VOIDP, VOIDP, VOIDP)
def vector3_cross_vector3(self, other, result):
    """ */

    void vector3_cross_vector3(const float *self, const float *other,
                               float *result) {
        float cache[3] = { // 计算的步骤不能影响结果，所以需要一个临时缓存。
            self[1] * other[2] - self[2] * other[1],
            self[2] * other[0] - self[0] * other[2],
            self[0] * other[1] - self[1] * other[0]
        };
        memcpy(result, cache, 3 * sizeof(float));
    }
    /* """
    _sx, _sy, _sz = self
    _ox, _oy, _oz = other

    result(
        _sy * _oz - _sz * _oy, _sz * _ox - _sx * _oz, _sx * _oy - _sy * _ox)


@ctypes_wrap(None, VOIDP, VOIDP, VOIDP)
def vector3_project_vector3(self, other, result):
    """ */

    void vector3_project_vector3(const float *self, const float *other,
                                 float *result) {
        float _scalar = vector3_dot_vector3(self, other) /
                        vector3_length_squared(other);
        vector3_mul_scalar(other, _scalar, result);
    }
    /* """
    _scalar = vector3_dot_vector3(self, other) / vector3_length_squared(other)
    vector3_mul_scalar(other, _scalar, result)


@ctypes_wrap(None, VOIDP, VOIDP, VOIDP)
def vector3_reflect(self, normal, result):
    """ */

    void vector3_reflect(const float *self, const float *normal,
                         float *result) {
        vector3_mul_scalar(
            normal, vector3_dot_vector3(self, normal) * 2.0f, result);
        vector3_sub_vector3(self, result, result);
    }
    /* """
    vector3_mul_scalar(normal, 2 * self.dot_vector3(normal), result)
    return vector3_sub_vector3(self, result, result)


@ctypes_wrap(FLT, VOIDP, VOIDP)
def vector3_angle_to_vector3(self, other):
    """ */

    float vector3_angle_to_vector3(const float *self, const float *other) {
        float _theta = vector3_dot_vector3(self, other) / sqrtf(
                vector3_length_squared(self) * vector3_length_squared(other));
        return acosf(clamp(_theta, -1.0f, 1.0f));
    }
    /* """
    _theta = self.dot_vector3(other) / (
            (self.length_squared() * other.length_squared()) ** 0.5)
    _theta = -1 if _theta < -1 else 1 if _theta > 1 else _theta
    return math.acos(_theta)


@ctypes_wrap(FLT, VOIDP, VOIDP)
def vector3_distance_squared_to_vector3(self, other):
    """ */

    float vector3_distance_squared_to_vector3(const float *self,
                                              const float *other) {
        vector3_sub_vector3(self, other, vector3_0);
        return vector3_length_squared(vector3_0);
    }
    /* """
    return sum((_x - _y) ** 2 for _x, _y in zip(self, other))


@ctypes_wrap(FLT, VOIDP, VOIDP)
def vector3_distance_to_vector3(self, other):
    """ */

    float vector3_distance_to_vector3(const float *self, const float *other) {
        return sqrtf(vector3_distance_squared_to_vector3(self, other));
    }
    /* """
    return math.sqrt(vector3_distance_squared_to_vector3(self, other))


@ctypes_wrap(FLT, VOIDP, VOIDP)
def vector3_distance_manhattan_to_vector3(self, other):
    """ */

    float vector3_distance_manhattan_to_vector3(const float *self,
                                                const float *other) {
        vector3_sub_vector3(self, other, vector3_0);
        return vector3_length_manhattan(vector3_0);
    }
    /* """
    return sum(abs(_x - _y) for _x, _y in zip(self, other))


@ctypes_wrap(None, FLT, FLT, FLT, VOIDP)
def vector3_from_spherical(radius, phi, theta, result):
    """ */

    void vector3_from_spherical(float radius, float phi,
                                float theta, float *result) {
        float _s = sinf(phi) * radius;
        result[0] = _s * sinf(theta);
        result[1] = cosf(phi) * radius;
        result[2] = _s * cosf(theta);
    }
    /* """
    _s = math.sin(phi) * radius
    result(_s * math.sin(theta), math.cos(phi) * radius, _s * math.cos(theta))


@ctypes_wrap(None, FLT, FLT, FLT, VOIDP)
def vector3_from_cylindrical(radius, theta, y, result):
    """ */

    void vector3_from_cylindrical(float radius, float theta,
                                  float y, float *result) {
        result[0] = radius * sinf(theta);
        result[1] = y;
        result[2] = radius * cosf(theta);
    }
    /* """
    result(radius * math.sin(theta), y, radius * math.cos(theta))


@ctypes_wrap(None, VOIDP, UNSIGNED, VOIDP)
def vector3_from_matrix4_offset(matrix4, offset, result):
    """ */

    void vector3_from_matrix4_offset(const float *matrix4, unsigned offset,
                                     float *result) {
        memcpy(result, matrix4 + offset, 3 * sizeof(float));
    }
    /* """
    result(matrix4[offset], matrix4[offset + 1], matrix4[offset + 2])


@ctypes_wrap(None, VOIDP, VOIDP)
def vector3_from_matrix4_scale(matrix4, result):
    """ */

    void vector3_from_matrix4_scale(const float *matrix4, float *result) {
        for (int i = 0; i < 3; i++) {
            vector3_from_matrix4_offset(matrix4, i * 4, vector3_0);
            result[i] = vector3_length(vector3_0);
        }
    }
    /* """
    vector3_from_matrix4_offset(matrix4, 0, vector3_0)
    result[0] = vector3_length(vector3_0)
    vector3_from_matrix4_offset(matrix4, 4, vector3_0)
    result[1] = vector3_length(vector3_0)
    vector3_from_matrix4_offset(matrix4, 8, vector3_0)
    result[2] = vector3_length(vector3_0)

# */
