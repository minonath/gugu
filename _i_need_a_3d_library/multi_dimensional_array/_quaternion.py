# include "_array.py" /*

import math
from ._vector3 import vector3_dot_vector3, vector3_normalize
from ._array import xyz, yxz, zxy, zyx, yzx, xzy, clamp, \
    ctypes_wrap, VOIDP, FLT, UNSIGNED


@ctypes_wrap(None, VOIDP, UNSIGNED, VOIDP)
def quaternion_from_euler(euler, order, result):
    """ */

    void quaternion_from_euler(const float *euler, unsigned order,
                               float *result) {
        float c0 = cosf(euler[0] * 0.5f), c1 = cosf(euler[1] * 0.5f),
                c2 = cosf(euler[2] * 0.5f), s0 = sinf(euler[0] * 0.5f),
                s1 = sinf(euler[1] * 0.5f), s2 = sinf(euler[2] * 0.5f);
        switch (order) {
            case xyz:
                result[0] = s0 * c1 * c2 + c0 * s1 * s2;
                result[1] = c0 * s1 * c2 - s0 * c1 * s2;
                result[2] = c0 * c1 * s2 + s0 * s1 * c2;
                result[3] = c0 * c1 * c2 - s0 * s1 * s2;
                break;
            case yxz:
                result[0] = s0 * c1 * c2 + c0 * s1 * s2;
                result[1] = c0 * s1 * c2 - s0 * c1 * s2;
                result[2] = c0 * c1 * s2 - s0 * s1 * c2;
                result[3] = c0 * c1 * c2 + s0 * s1 * s2;
                break;
            case zxy:
                result[0] = s0 * c1 * c2 - c0 * s1 * s2;
                result[1] = c0 * s1 * c2 + s0 * c1 * s2;
                result[2] = c0 * c1 * s2 + s0 * s1 * c2;
                result[3] = c0 * c1 * c2 - s0 * s1 * s2;
                break;
            case zyx:
                result[0] = s0 * c1 * c2 - c0 * s1 * s2;
                result[1] = c0 * s1 * c2 + s0 * c1 * s2;
                result[2] = c0 * c1 * s2 - s0 * s1 * c2;
                result[3] = c0 * c1 * c2 + s0 * s1 * s2;
                break;
            case yzx:
                result[0] = s0 * c1 * c2 + c0 * s1 * s2;
                result[1] = c0 * s1 * c2 + s0 * c1 * s2;
                result[2] = c0 * c1 * s2 - s0 * s1 * c2;
                result[3] = c0 * c1 * c2 - s0 * s1 * s2;
                break;
            case xzy:
                result[0] = s0 * c1 * c2 - c0 * s1 * s2;
                result[1] = c0 * s1 * c2 - s0 * c1 * s2;
                result[2] = c0 * c1 * s2 + s0 * s1 * c2;
                result[3] = c0 * c1 * c2 + s0 * s1 * s2;
                break;
            default:
                return;
        }
    }
    /* """
    _x, _y, _z = euler

    c0 = math.cos(_x / 2)
    c1 = math.cos(_y / 2)
    c2 = math.cos(_z / 2)

    s0 = math.sin(_x / 2)
    s1 = math.sin(_y / 2)
    s2 = math.sin(_z / 2)

    if order == 'xyz':
        result(s0 * c1 * c2 + c0 * s1 * s2, c0 * s1 * c2 - s0 * c1 * s2,
               c0 * c1 * s2 + s0 * s1 * c2, c0 * c1 * c2 - s0 * s1 * s2)

    elif order == 'yxz':
        result(s0 * c1 * c2 + c0 * s1 * s2, c0 * s1 * c2 - s0 * c1 * s2,
               c0 * c1 * s2 - s0 * s1 * c2, c0 * c1 * c2 + s0 * s1 * s2)

    elif order == 'zxy':
        result(s0 * c1 * c2 - c0 * s1 * s2, c0 * s1 * c2 + s0 * c1 * s2,
               c0 * c1 * s2 + s0 * s1 * c2, c0 * c1 * c2 - s0 * s1 * s2)

    elif order == 'zyx':
        result(s0 * c1 * c2 - c0 * s1 * s2, c0 * s1 * c2 + s0 * c1 * s2,
               c0 * c1 * s2 - s0 * s1 * c2, c0 * c1 * c2 + s0 * s1 * s2)

    elif order == 'yzx':
        result(s0 * c1 * c2 + c0 * s1 * s2, c0 * s1 * c2 + s0 * c1 * s2,
               c0 * c1 * s2 - s0 * s1 * c2, c0 * c1 * c2 - s0 * s1 * s2)

    elif order == 'xzy':
        result(s0 * c1 * c2 - c0 * s1 * s2, c0 * s1 * c2 - s0 * c1 * s2,
               c0 * c1 * s2 + s0 * s1 * c2, c0 * c1 * c2 + s0 * s1 * s2)


@ctypes_wrap(None, VOIDP, VOIDP)
def quaternion_from_axis_angle(axis_angle, result):
    """ */

    void quaternion_from_axis_angle(const float *axis_angle, float *result) {
        float _half = axis_angle[3] / 2.0f;
        float _s = sinf(_half);
        result[0] = axis_angle[0] * _s;
        result[1] = axis_angle[1] * _s;
        result[2] = axis_angle[2] * _s;
        result[3] = cosf(_half);
    }
    /* """
    _x, _y, _z, angle = axis_angle
    half = angle / 2
    s = math.sin(half)
    result(_x * s, _y * s, _z * s, math.cos(half))


@ctypes_wrap(None, VOIDP, VOIDP)
def quaternion_from_matrix4_rotation(matrix4, result):
    """ */

    void quaternion_from_matrix4_rotation(const float *matrix4,
                                          float *result) {
        float trace = matrix4[0] + matrix4[5] + matrix4[10], s;
        if (trace > 0.0f) {  // matrix 和 result 绝对不会相同，因此不用缓存。
            s = 0.5f / sqrtf(trace + 1.0f);
            result[0] = (matrix4[6] - matrix4[9]) * s;
            result[1] = (matrix4[8] - matrix4[2]) * s;
            result[2] = (matrix4[1] - matrix4[4]) * s;
            result[3] = 0.25f / s;
        } else if (matrix4[0] > matrix4[5] && matrix4[0] > matrix4[10]) {
            s = 2.0f * sqrtf(1.0f + matrix4[0] - matrix4[5] - matrix4[10]);
            result[0] = 0.25f * s;
            result[1] = (matrix4[4] + matrix4[1]) / s;
            result[2] = (matrix4[8] + matrix4[2]) / s;
            result[3] = (matrix4[6] - matrix4[9]) / s;
        } else if (matrix4[5] > matrix4[10]) {
            s = 2.0f * sqrtf(1.0f + matrix4[5] - matrix4[0] - matrix4[10]);
            result[0] = (matrix4[4] + matrix4[1]) / s;
            result[1] = 0.25f * s;
            result[2] = (matrix4[9] + matrix4[6]) / s;
            result[3] = (matrix4[8] - matrix4[2]) / s;
        } else {
            s = 2.0f * sqrtf(1.0f + matrix4[10] - matrix4[0] - matrix4[5]);
            result[0] = (matrix4[8] + matrix4[2]) / s;
            result[1] = (matrix4[9] + matrix4[6]) / s;
            result[2] = 0.25f * s;
            result[3] = (matrix4[1] - matrix4[4]) / s;
        }
    }
    /* """
    (m11, m21, m31, _, m12, m22, m32, _,
     m13, m23, m33, _, _, _, _, _) = matrix4

    trace = m11 + m22 + m33
    if trace > 0:
        s = 0.5 / math.sqrt(trace + 1.0)
        result((m32 - m23) * s, (m13 - m31) * s, (m21 - m12) * s, 0.25 / s)

    elif m11 > m22 and m11 > m33:
        s = 2.0 * math.sqrt(1.0 + m11 - m22 - m33)
        result(0.25 * s, (m12 + m21) / s, (m13 + m31) / s, (m32 - m23) / s)

    elif m22 > m33:
        s = 2.0 * math.sqrt(1.0 + m22 - m11 - m33)
        result((m12 + m21) / s, 0.25 * s, (m23 + m32) / s, (m13 - m31) / s)

    else:
        s = 2.0 * math.sqrt(1.0 + m33 - m11 - m22)
        result((m13 + m31) / s, (m23 + m32) / s, 0.25 * s, (m21 - m12) / s)


@ctypes_wrap(None, VOIDP, VOIDP, VOIDP)
def quaternion_from_unit_vector3(vector3_f, vector3_t, result):
    """ */

    void quaternion_from_unit_vector3(
            const float *vector3_f, const float *vector3_t, float *result) {
        result[0] = vector3_f[1] * vector3_t[2] - vector3_f[2] * vector3_t[1];
        result[1] = vector3_f[2] * vector3_t[0] - vector3_f[0] * vector3_t[2];
        result[2] = vector3_f[0] * vector3_t[1] - vector3_f[1] * vector3_t[0];
        result[3] = vector3_dot_vector3(vector3_f, vector3_t) + 1.0f;
        vector3_normalize(result, result);
    }
    /* """
    x, y, z = vector3_f
    a, b, c = vector3_t

    result(y * c - z * b, z * a - x * c, x * b - y * a,
           vector3_dot_vector3(vector3_f, vector3_t) + 1)
    vector3_normalize(result, result)


@ctypes_wrap(FLT, VOIDP, VOIDP)
def quaternion_angle_to_quaternion(self, other):
    """ */

    float quaternion_angle_to_quaternion(const float *self,
                                         const float *other) {
        return 2 * acosf(fabsf(clamp(
            quaternion_dot_quaternion(self, other), -1.0f, 1.0f)));
    }
    /* """
    return 2 * math.acos(abs(clamp(
        quaternion_dot_quaternion(self, other), -1, 1)))


@ctypes_wrap(None, VOIDP, VOIDP, FLT, VOIDP)
def quaternion_rotate_towards(self, other, step, result):
    """ */

    void quaternion_rotate_towards(const float *self, const float *other,
                                   float step, float *result) {
        float angle = quaternion_angle_to_quaternion(self, other);
        if (angle == 0.0f) memcpy(result, self, 4 * sizeof(float));
        else quaternion_spherical_linear_interpolation(
            self, other, min(1.0f, step / angle), result);
    }
    /* """
    angle = quaternion_angle_to_quaternion(self, other)
    if angle == 0:
        result(*self)
    else:
        angle = min(1, step / angle)
        quaternion_spherical_linear_interpolation(self, other, angle, result)


@ctypes_wrap(None, VOIDP, VOIDP)
def quaternion_conjugate(self, result):
    """ */

    void quaternion_conjugate(const float *self, float *result) {
        for (int i = 0; i < 3; i++) result[i] = -self[i];  // 注意这里是 3
    }
    /* """
    x, y, z, w = self
    result(-x, -y, -z, w)


@ctypes_wrap(FLT, VOIDP, VOIDP)
def quaternion_dot_quaternion(self, other):
    """ */

    float quaternion_dot_quaternion(const float *self, const float *other) {
        return self[0] * other[0] + self[1] * other[1] + self[2] * other[2] +
               self[3] * other[3];
    }
    /* """
    return sum(_x * _y for _x, _y in zip(self, other))


@ctypes_wrap(FLT, VOIDP)
def quaternion_length_squared(self):
    """ */

    float quaternion_length_squared(const float *self) {
        return self[0] * self[0] + self[1] * self[1] + self[2] * self[2] +
               self[3] * self[3];
    }
    /* """
    return sum(_x ** 2 for _x in self)


@ctypes_wrap(FLT, VOIDP)
def quaternion_length(self):
    """ */

    float quaternion_length(const float *self) {
        return sqrtf(quaternion_length_squared(self));
    }
    /* """
    return math.sqrt(quaternion_length_squared(self))


@ctypes_wrap(None, VOIDP, VOIDP)
def quaternion_normalize(self, result):
    """ */

    void quaternion_normalize(const float *self, float *result) {
        float length = quaternion_length(self);
        if (length != 0.0f)
            for (int i = 0; i < 4; i++) result[i] = self[i] / length;
    }
    /* """
    _length = quaternion_length(self)
    if _length:
        result(*(_x / _length for _x in self))


@ctypes_wrap(None, VOIDP, VOIDP, VOIDP)
def quaternion_mul_quaternion(self, other, result):
    """ */

    void quaternion_mul_quaternion(const float *self, const float *other,
                                   float *result) {
        float cache[4] = {  // 计算结果会影响后一个计算结果，所以需要一个缓存。
            self[0] * other[3] + self[3] * other[0] + self[1] * other[2] -
            self[2] * other[1],
            self[1] * other[3] + self[3] * other[1] + self[2] * other[0] -
            self[0] * other[2],
            self[2] * other[3] + self[3] * other[2] + self[0] * other[1] -
            self[1] * other[0],
            self[3] * other[3] - self[0] * other[0] - self[1] * other[1] -
            self[2] * other[2]
        };
        memcpy(result, cache, 4 * sizeof(float));
    }
    /* """
    _ax, _ay, _az, _aw = self
    _bx, _by, _bz, _bw = other

    result(
        _ax * _bw + _aw * _bx + _ay * _bz - _az * _by,
        _ay * _bw + _aw * _by + _az * _bx - _ax * _bz,
        _az * _bw + _aw * _bz + _ax * _by - _ay * _bx,
        _aw * _bw - _ax * _bx - _ay * _by - _az * _bz
    )


@ctypes_wrap(None, VOIDP, VOIDP, FLT, VOIDP)
def quaternion_spherical_linear_interpolation(self, other, alpha, result):
    """ */

    void quaternion_spherical_linear_interpolation(
        const float *self, const float *other, float alpha, float *result) {
        if (alpha == 0.0f) memcpy(result, self, 4 * sizeof(float));
        else if (alpha == 1.0f) memcpy(result, other, 4 * sizeof(float));
        else {
            float cos_half_theta = quaternion_dot_quaternion(self, other),
                    sin_half_theta, half_theta, ratio_a, ratio_b;
            if (cos_half_theta < 1.0f && cos_half_theta > -1.0f) {
                sin_half_theta = sqrtf(1.0f - cos_half_theta * cos_half_theta);
                half_theta = atan2f(sin_half_theta, cos_half_theta);
                ratio_a = sinf((1 - alpha) * half_theta) / sin_half_theta;
                ratio_b = sinf(alpha * half_theta) / sin_half_theta;

                for (int i = 0; i < 4; i++)
                    result[i] = self[i] * ratio_a + other[i] * ratio_b;
            } else
                memcpy(result, self, 4 * sizeof(float));
        }
    }
    /* """
    if alpha == 0:
        result(*self)
    elif alpha == 1:
        result(*other)
    else:
        x, y, z, w = self
        _x, _y, _z, _w = other

        cos_half_theta = w * _w + x * _x + y * _y + z * _z

        if -1.0 < cos_half_theta < 1.0:
            sin_half_theta = math.sqrt(
                1.0 - cos_half_theta * cos_half_theta)
            half_theta = math.atan2(sin_half_theta, cos_half_theta)
            ratio_a = math.sin((1 - alpha) * half_theta) / sin_half_theta
            ratio_b = math.sin(alpha * half_theta) / sin_half_theta

            result(
                x * ratio_a + _x * ratio_b, y * ratio_a + _y * ratio_b,
                z * ratio_a + _z * ratio_b, w * ratio_a + _w * ratio_b)

        else:
            result(x, y, z, w)


@ctypes_wrap(None, VOIDP, UNSIGNED, VOIDP)
def euler_from_matrix4(matrix4, order, result):
    """ */

    void euler_from_matrix4(const float *matrix4, unsigned order,
                            float *result) {
        switch (order) {
            case xyz:
                result[1] = asinf(clamp(matrix4[8], -1.0f, 1.0f));
                if (fabsf(matrix4[8]) < 1.0f) {
                    result[0] = atan2f(-matrix4[9], matrix4[10]);
                    result[2] = atan2f(-matrix4[4], matrix4[0]);
                } else {
                    result[0] = atan2f(matrix4[6], matrix4[5]);
                    result[2] = 0.0f;
                }
                break;
            case yxz:
                result[0] = asinf(-clamp(matrix4[9], -1.0f, 1.0f));
                if (fabsf(matrix4[9]) < 1.0f) {
                    result[1] = atan2f(matrix4[8], matrix4[10]);
                    result[2] = atan2f(matrix4[1], matrix4[5]);
                } else {
                    result[1] = atan2f(matrix4[6], matrix4[5]);
                    result[2] = 0.0f;
                }
                break;
            case zxy:
                result[0] = asinf(clamp(matrix4[6], -1.0f, 1.0f));
                if (fabsf(matrix4[6]) < 1.0f) {
                    result[1] = atan2f(-matrix4[2], matrix4[10]);
                    result[2] = atan2f(-matrix4[4], matrix4[5]);
                } else {
                    result[1] = 0.0f;
                    result[2] = atan2f(matrix4[1], matrix4[0]);
                }
                break;
            case zyx:
                result[1] = asinf(-clamp(matrix4[2], -1.0f, 1.0f));
                if (fabsf(matrix4[2]) < 1.0f) {
                    result[0] = atan2f(matrix4[6], matrix4[10]);
                    result[2] = atan2f(matrix4[1], matrix4[0]);
                } else {
                    result[0] = 0.0f;
                    result[2] = atan2f(-matrix4[4], matrix4[5]);
                }
                break;
            case yzx:
                result[2] = asinf(clamp(matrix4[1], -1.0f, 1.0f));
                if (fabsf(matrix4[1]) < 1.0f) {
                    result[0] = atan2f(-matrix4[9], matrix4[5]);
                    result[1] = atan2f(-matrix4[2], matrix4[0]);
                } else {
                    result[0] = 0.0f;
                    result[1] = atan2f(matrix4[8], matrix4[10]);
                }
                break;
            case xzy:
                result[2] = asinf(-clamp(matrix4[4], -1.0f, 1.0f));
                if (fabsf(matrix4[4]) < 1.0f) {
                    result[0] = atan2f(matrix4[6], matrix4[5]);
                    result[1] = atan2f(matrix4[8], matrix4[0]);
                } else {
                    result[0] = atan2f(-matrix4[9], matrix4[10]);
                    result[1] = 0.0f;
                }
                break;
            default:
                result[0] = result[1] = result[2] = 0.0f;
        }
    }
    /* """
    (_m11, _m21, _m31, _, _m12, _m22, _m32, _,
     _m13, _m23, _m33, _, _, _, _, _) = matrix4

    if order == xyz:
        _y = math.asin(clamp(_m13, -1, 1))
        if abs(_m13) < 1:
            result(math.atan2(-_m23, _m33), _y, math.atan2(-_m12, _m11))
        else:
            result(math.atan2(_m32, _m22), _y, 0)

    elif order == yxz:
        _x = math.asin(-clamp(_m23, -1, 1))
        if abs(_m23) < 1:
            result(_x, math.atan2(_m13, _m33), math.atan2(_m21, _m22))
        else:
            result(_x, math.atan2(- _m31, _m11), 0)

    elif order == zxy:
        _x = math.asin(clamp(_m32, -1, 1))
        if abs(_m32) < 1:
            result(_x, math.atan2(-_m31, _m33), math.atan2(-_m12, _m22))
        else:
            result(_x, 0, math.atan2(_m21, _m11))

    elif order == zyx:
        _y = math.asin(-clamp(_m31, -1, 1))
        if abs(_m31) < 1:
            result(math.atan2(_m32, _m33), _y, math.atan2(_m21, _m11))
        else:
            result(0, _y, math.atan2(-_m12, _m22))

    elif order == yzx:
        _z = math.asin(clamp(_m21, -1, 1))
        if abs(_m21) < 1:
            result(math.atan2(-_m23, _m22), math.atan2(-_m31, _m11), _z)
        else:
            result(0, math.atan2(_m13, _m33), _z)

    elif order == xzy:
        _z = math.asin(-clamp(_m12, -1, 1))
        if abs(_m12) < 1:
            result(math.atan2(_m32, _m22), math.atan2(_m13, _m11), _z)
        else:
            result(math.atan2(-_m23, _m33), 0, _z)

# */
