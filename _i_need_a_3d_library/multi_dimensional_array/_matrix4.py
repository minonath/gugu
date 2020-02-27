# include "_array.py" /*

import math
from ._vector3 import vector3_sub_vector3, vector3_normalize, \
    vector3_cross_vector3, vector3_dot_vector3, vector3_from_matrix4_scale
from ._quaternion import quaternion_from_matrix4_rotation
from ._array import xyz, yxz, zxy, zyx, yzx, xzy, \
    vector3_0, vector3_1, vector3_2, matrix4_0, \
    ctypes_wrap, VOIDP, FLT, UNSIGNED


@ctypes_wrap(None, VOIDP)
def matrix4_from_identity(result):
    """ */

    static float matrix4_identity[16] = {
        1.0f, 0.0f, 0.0f, 0.0f,
        0.0f, 1.0f, 0.0f, 0.0f,
        0.0f, 0.0f, 1.0f, 0.0f,
        0.0f, 0.0f, 0.0f, 1.0f
    };

    void matrix4_from_identity(float *result) {
        memcpy(result, matrix4_identity, 16 * sizeof(float));
    }
    /* """
    result(1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1)


@ctypes_wrap(None, VOIDP, VOIDP, VOIDP, VOIDP)
def matrix4_from_basis(axis_a, axis_b, axis_c, result):
    """ */

    void matrix4_from_basis(const float *axis_a, const float *axis_b,
                            const float *axis_c, float *result) {
        memcpy(result, axis_a, 3 * sizeof(float));
        memcpy(result + 4, axis_b, 3 * sizeof(float));
        memcpy(result + 8, axis_c, 3 * sizeof(float));
    }
    /* """
    result(axis_a[0], axis_a[1], axis_a[2], result[3],
           axis_b[0], axis_b[1], axis_b[2], result[7],
           axis_c[0], axis_c[1], axis_c[2], result[11],
           result[12], result[13], result[14], result[15])


@ctypes_wrap(None, VOIDP, VOIDP)
def matrix4_from_matrix3_as_rotation(matrix3, result):
    """ */

    void matrix4_from_matrix3_as_rotation(const float *matrix3,
                                          float *result) {
        float scale_x = vector3_length(matrix3),
              scale_y = vector3_length(matrix3 + 4),
              scale_z = vector3_length(matrix3 + 8);
        vector3_mul_scalar(matrix3, scale_x, result);
        vector3_mul_scalar(matrix3 + 3, scale_y, result + 4);
        vector3_mul_scalar(matrix3 + 6, scale_z, result + 8);
    }
    /* """
    _m11, _m21, _m31, _m12, _m22, _m32, _m13, _m23, _m33 = matrix3
    _scale_x = (_m11 * _m11 + _m21 * _m21 + _m31 * _m31) ** 0.5
    _scale_y = (_m12 * _m12 + _m22 * _m22 + _m32 * _m32) ** 0.5
    _scale_z = (_m13 * _m13 + _m23 * _m23 + _m33 * _m33) ** 0.5

    result(_m11 * _scale_x, _m21 * _scale_x, _m31 * _scale_x, 0,
           _m12 * _scale_y, _m22 * _scale_y, _m32 * _scale_y, 0,
           _m13 * _scale_z, _m23 * _scale_z, _m33 * _scale_z, 0, 0, 0, 0, 1)


@ctypes_wrap(None, VOIDP, UNSIGNED, VOIDP)
def matrix4_from_euler(euler, order, result):
    """ */

    void matrix4_from_euler(const float *euler, unsigned order,
                            float *result) {
        float a = cosf(euler[0]), b = sinf(euler[0]), c = cosf(euler[1]),
              d = sinf(euler[1]), e = cosf(euler[2]), f = sinf(euler[2]);
        switch (order) {
            case xyz:
                result[0] = c * e;              result[1] = a * f + b * e * d;
                result[2] = b * f - a * e * d;  result[3] = 0.0f;
                result[4] = -c * f;             result[5] = a * e - b * f * d;
                result[6] = b * e + a * f * d;  result[7] = 0.0f;
                result[8] = d;                  result[9] = -b * c;
                result[10] = a * c;             result[11] = 0.0f;
                result[12] =    result[13] =    result[14] = 0.0f;
                result[15] = 1.0f;              break;
            case yxz:
                result[0] = c * e + d * f * b;  result[1] = a * f;
                result[2] = c * f * b - d * e;  result[3] = 0.0f;
                result[4] = d * e * b - c * f;  result[5] = a * e;
                result[6] = d * f + c * e * b;  result[7] = 0.0f;
                result[8] = a * d;              result[9] = -b;
                result[10] = a * c;             result[11] = 0.0f;
                result[12] =    result[13] =    result[14] = 0.0f;
                result[15] = 1.0f;              break;
            case zxy:
                result[0] = c * e - d * f * b;  result[1] = c * f + d * e * b;
                result[2] = -a * d;             result[3] = 0.0f;
                result[4] = -a * f;             result[5] = a * e;
                result[6] = b;                  result[7] = 0.0f;
                result[8] = d * e + c * f * b;  result[9] = d * f - c * e * b;
                result[10] = a * c;             result[11] = 0.0f;
                result[12] =    result[13] =    result[14] = 0.0f;
                result[15] = 1.0f;              break;
            case zyx:
                result[0] = c * e;              result[1] = c * f;
                result[2] = -d;                 result[3] = 0.0f;
                result[4] = b * e * d - a * f;  result[5] = b * f * d + a * e;
                result[6] = b * c;              result[7] = 0.0f;
                result[8] = a * e * d + b * f;  result[9] = a * f * d - b * e;
                result[10] = a * c;             result[11] = 0.0f;
                result[12] =    result[13] =    result[14] = 0.0f;
                result[15] = 1.0f;              break;
            case yzx:
                result[0] = c * e;              result[1] = f;
                result[2] = -d * e;             result[3] = 0.0f;
                result[4] = b * d - a * c * f;  result[5] = a * e;
                result[6] = a * d * f + b * c;  result[7] = 0.0f;
                result[8] = b * c * f + a * d;  result[9] = -b * e;
                result[10] = a * c - b * d * f; result[11] = 0.0f;
                result[12] =    result[13] =    result[14] = 0.0f;
                result[15] = 1.0f;              break;
            case xzy:
                result[0] = c * e;              result[1] = a * c * f + b * d;
                result[2] = b * c * f - a * d;  result[3] = 0.0f;
                result[4] = -f;                 result[5] = a * e;
                result[6] = b * e;              result[7] = 0.0f;
                result[8] = d * e;              result[9] = a * d * f - b * c;
                result[10] = b * d * f + a * c; result[11] = 0.0f;
                result[12] =    result[13] =    result[14] = 0.0f;
                result[15] = 1.0f;              break;
            default:
                memcpy(result, matrix4_identity, 16 * sizeof(float));
        }
    }
    /* """
    x, y, z = euler
    a = math.cos(x)
    b = math.sin(x)
    c = math.cos(y)
    d = math.sin(y)
    e = math.cos(z)
    f = math.sin(z)

    if order == xyz:
        result(c * e, a * f + b * e * d, b * f - a * e * d, 0,
               - c * f, a * e - b * f * d, b * e + a * f * d, 0,
               d, - b * c, a * c, 0, 0, 0, 0, 1)
    elif order == yxz:
        result(c * e + d * f * b, a * f, c * f * b - d * e, 0,
               d * e * b - c * f, a * e, d * f + c * e * b, 0,
               a * d, - b, a * c, 0, 0, 0, 0, 1)
    elif order == zxy:
        result(
            c * e - d * f * b, c * f + d * e * b, - a * d, 0, - a * f, a * e,
            b, 0, d * e + c * f * b, d * f - c * e * b, a * c, 0, 0, 0, 0, 1)
    elif order == zyx:
        result(
            c * e, c * f, - d, 0, b * e * d - a * f, b * f * d + a * e, b * c,
            0, a * e * d + b * f, a * f * d - b * e, a * c, 0, 0, 0, 0, 1)
    elif order == yzx:
        result(
            c * e, f, - d * e, 0, b * d - a * c * f, a * e, a * d * f + b * c,
            0, b * c * f + a * d, - b * e, a * c - b * d * f, 0, 0, 0, 0, 1)
    elif order == xzy:
        result(
            c * e, a * c * f + b * d, b * c * f - a * d, 0, - f, a * e, b * e,
            0, d * e, a * d * f - b * c, b * d * f + a * c, 0, 0, 0, 0, 1)
    return result


@ctypes_wrap(None, VOIDP, VOIDP)
def matrix4_from_quaternion(quaternion, result):
    """ */

    void matrix4_from_quaternion(const float *quaternion, float *result) {
        result[0] = 1.0f - (quaternion[1] * quaternion[1] +
                            quaternion[2] * quaternion[2]) * 2.0f;
        result[1] = (quaternion[0] * quaternion[1] +
                     quaternion[3] * quaternion[2]) * 2.0f;
        result[2] = (quaternion[0] * quaternion[2] -
                     quaternion[3] * quaternion[1]) * 2.0f;
        result[3] = 0.0f;
        result[4] = (quaternion[0] * quaternion[1] -
                     quaternion[3] * quaternion[2]) * 2.0f;
        result[5] = 1 - (quaternion[0] * quaternion[0] +
                         quaternion[2] * quaternion[2]) * 2.0f;
        result[6] = (quaternion[1] * quaternion[2] +
                     quaternion[3] * quaternion[0]) * 2.0f;
        result[7] = 0.0f;
        result[8] = (quaternion[0] * quaternion[2] +
                     quaternion[3] * quaternion[1]) * 2.0f;
        result[9] = (quaternion[1] * quaternion[2] -
                     quaternion[3] * quaternion[0]) * 2.0f;
        result[10] = 1 - (quaternion[0] * quaternion[0] +
                          quaternion[1] * quaternion[1]) * 2.0f;
        result[11] =  result[12] =  result[13] =  result[14] = 0.0f;
        result[15] = 1.0f;
    }
    /* """
    vector3_0(0, 0, 0)
    vector3_1(1, 1, 1)
    matrix4_from_compose(vector3_0, quaternion, vector3_1, result)


@ctypes_wrap(None, VOIDP, VOIDP, VOIDP, VOIDP)
def matrix4_from_look_at(eye, target, up, result):
    """ */

    void matrix4_from_look_at(const float *eye, const float *target,
                              const float *up, float *result) {
        vector3_sub_vector3(target, eye, vector3_2);
        vector3_normalize(vector3_2, vector3_2);
        vector3_cross_vector3(vector3_2, up, vector3_0);
        vector3_normalize(vector3_0, vector3_0);
        vector3_cross_vector3(vector3_0, vector3_2, vector3_1);
        vector3_normalize(vector3_1, vector3_1);
        result[0] = vector3_0[0];
        result[1] = vector3_1[0];
        result[2] = -vector3_2[0];
        result[3] = 0.0f;
        result[4] = vector3_0[1];
        result[5] = vector3_1[1];
        result[6] = -vector3_2[1];
        result[7] = 0.0f;
        result[8] = vector3_0[2];
        result[9] = vector3_1[2];
        result[10] = -vector3_2[2];
        result[11] = 0.0f;
        result[12] = -vector3_dot_vector3(vector3_0, eye);
        result[13] = -vector3_dot_vector3(vector3_1, eye);
        result[14] = vector3_dot_vector3(vector3_2, eye);
        result[15] = 1.0f;
    }
    /* """
    vector3_sub_vector3(target, eye, vector3_2)
    vector3_normalize(vector3_2, vector3_2)
    vector3_cross_vector3(vector3_2, up, vector3_0)
    vector3_normalize(vector3_0, vector3_0)
    vector3_cross_vector3(vector3_0, vector3_2, vector3_1)
    vector3_normalize(vector3_1, vector3_1)
    return result(vector3_0[0], vector3_1[0], -vector3_2[0], 0,
                  vector3_0[1], vector3_1[1], -vector3_2[1], 0,
                  vector3_0[2], vector3_1[2], -vector3_2[2], 0,
                  -vector3_dot_vector3(vector3_0, eye),
                  -vector3_dot_vector3(vector3_1, eye),
                  vector3_dot_vector3(vector3_2, eye), 1)


@ctypes_wrap(None, VOIDP, VOIDP, VOIDP)
def matrix4_mul_matrix4(self, other, result):
    """ */

    void matrix4_mul_matrix4(const float *self, const float *other,
                             float *result) {
        float cache[16] = {
            self[0] * other[0] + self[4] * other[1] +
            self[8] * other[2] + self[12] * other[3],
            self[1] * other[0] + self[5] * other[1] +
            self[9] * other[2] + self[13] * other[3],
            self[2] * other[0] + self[6] * other[1] +
            self[10] * other[2] + self[14] * other[3],
            self[3] * other[0] + self[7] * other[1] +
            self[11] * other[2] + self[15] * other[3],
            self[0] * other[4] + self[4] * other[5] +
            self[8] * other[6] + self[12] * other[7],
            self[1] * other[4] + self[5] * other[5] +
            self[9] * other[6] + self[13] * other[7],
            self[2] * other[4] + self[6] * other[5] +
            self[10] * other[6] + self[14] * other[7],
            self[3] * other[4] + self[7] * other[5] +
            self[11] * other[6] + self[15] * other[7],
            self[0] * other[8] + self[4] * other[9] +
            self[8] * other[10] + self[12] * other[11],
            self[1] * other[8] + self[5] * other[9] +
            self[9] * other[10] + self[13] * other[11],
            self[2] * other[8] + self[6] * other[9] +
            self[10] * other[10] + self[14] * other[11],
            self[3] * other[8] + self[7] * other[9] +
            self[11] * other[10] + self[15] * other[11],
            self[0] * other[12] + self[4] * other[13] +
            self[8] * other[14] + self[12] * other[15],
            self[1] * other[12] + self[5] * other[13] +
            self[9] * other[14] + self[13] * other[15],
            self[2] * other[12] + self[6] * other[13] +
            self[10] * other[14] + self[14] * other[15],
            self[3] * other[12] + self[7] * other[13] +
            self[11] * other[14] + self[15] * other[15]
        };
        memcpy(result, cache, 16 * sizeof(float));
    }
    /* """
    (_m11, _m21, _m31, _m41, _m12, _m22, _m32, _m42,
     _m13, _m23, _m33, _m43, _m14, _m24, _m34, _m44) = self
    (_n11, _n21, _n31, _n41, _n12, _n22, _n32, _n42,
     _n13, _n23, _n33, _n43, _n14, _n24, _n34, _n44) = other

    result(
        _m11 * _n11 + _m12 * _n21 + _m13 * _n31 + _m14 * _n41,
        _m21 * _n11 + _m22 * _n21 + _m23 * _n31 + _m24 * _n41,
        _m31 * _n11 + _m32 * _n21 + _m33 * _n31 + _m34 * _n41,
        _m41 * _n11 + _m42 * _n21 + _m43 * _n31 + _m44 * _n41,
        _m11 * _n12 + _m12 * _n22 + _m13 * _n32 + _m14 * _n42,
        _m21 * _n12 + _m22 * _n22 + _m23 * _n32 + _m24 * _n42,
        _m31 * _n12 + _m32 * _n22 + _m33 * _n32 + _m34 * _n42,
        _m41 * _n12 + _m42 * _n22 + _m43 * _n32 + _m44 * _n42,
        _m11 * _n13 + _m12 * _n23 + _m13 * _n33 + _m14 * _n43,
        _m21 * _n13 + _m22 * _n23 + _m23 * _n33 + _m24 * _n43,
        _m31 * _n13 + _m32 * _n23 + _m33 * _n33 + _m34 * _n43,
        _m41 * _n13 + _m42 * _n23 + _m43 * _n33 + _m44 * _n43,
        _m11 * _n14 + _m12 * _n24 + _m13 * _n34 + _m14 * _n44,
        _m21 * _n14 + _m22 * _n24 + _m23 * _n34 + _m24 * _n44,
        _m31 * _n14 + _m32 * _n24 + _m33 * _n34 + _m34 * _n44,
        _m41 * _n14 + _m42 * _n24 + _m43 * _n34 + _m44 * _n44
    )


@ctypes_wrap(None, VOIDP, FLT, VOIDP)
def matrix4_mul_scalar(self, other, result):
    """ */

    void matrix4_mul_scalar(const float *self, float other, float *result) {
        for (int i = 0; i < 16; i++) result[i] = self[i] * other;
    }
    /* """
    result(*(_x * other for _x in self))


@ctypes_wrap(FLT, VOIDP)
def matrix4_determinant(self):
    """ */

    float matrix4_determinant(const float *self) {
        return self[3] * (
            + self[12] * self[9] * self[6] - self[8] * self[13] * self[6]
            - self[12] * self[5] * self[10] + self[4] * self[13] * self[10]
            + self[8] * self[5] * self[14] - self[4] * self[9] * self[14])
            + self[7] * (
            + self[0] * self[9] * self[14] - self[0] * self[13] * self[10]
            + self[12] * self[1] * self[10] - self[8] * self[1] * self[14]
            + self[8] * self[13] * self[2] - self[12] * self[9] * self[2])
            + self[11] * (
            + self[0] * self[13] * self[6] - self[0] * self[5] * self[14]
            - self[12] * self[1] * self[6] + self[4] * self[1] * self[14]
            + self[12] * self[5] * self[2] - self[4] * self[13] * self[2])
            + self[15] * (
            - self[8] * self[5] * self[2] - self[0] * self[9] * self[6]
            + self[0] * self[5] * self[10] + self[8] * self[1] * self[6]
            - self[4] * self[1] * self[10] + self[4] * self[9] * self[2]);
    }
    /* """
    (_n11, _n21, _n31, _n41, _n12, _n22, _n32, _n42,
     _n13, _n23, _n33, _n43, _n14, _n24, _n34, _n44) = self

    return _n41 * (+ _n14 * _n23 * _n32 - _n13 * _n24 * _n32
                   - _n14 * _n22 * _n33 + _n12 * _n24 * _n33
                   + _n13 * _n22 * _n34 - _n12 * _n23 * _n34) + _n42 * (
                   + _n11 * _n23 * _n34 - _n11 * _n24 * _n33
                   + _n14 * _n21 * _n33 - _n13 * _n21 * _n34
                   + _n13 * _n24 * _n31 - _n14 * _n23 * _n31) + _n43 * (
                   + _n11 * _n24 * _n32 - _n11 * _n22 * _n34
                   - _n14 * _n21 * _n32 + _n12 * _n21 * _n34
                   + _n14 * _n22 * _n31 - _n12 * _n24 * _n31) + _n44 * (
                   - _n13 * _n22 * _n31 - _n11 * _n23 * _n32
                   + _n11 * _n22 * _n33 + _n13 * _n21 * _n32
                   - _n12 * _n21 * _n33 + _n12 * _n23 * _n31)


@ctypes_wrap(None, VOIDP, VOIDP)
def matrix4_transpose(self, result):
    """ */

    void matrix4_transpose(const float *self, float *result) {
        float tmp;
        tmp = self[4]; result[4] = self[1]; result[1] = tmp;
        tmp = self[8]; result[8] = self[2]; result[2] = tmp;
        tmp = self[12]; result[12] = self[3]; result[3] = tmp;
        tmp = self[9]; result[9] = self[6]; result[6] = tmp;
        tmp = self[13]; result[13] = self[7]; result[7] = tmp;
        tmp = self[14]; result[14] = self[11]; result[11] = tmp;
        result[0] = self[0];
        result[5] = self[5];
        result[10] = self[10];
        result[15] = self[15];
    }
    /* """
    (_n11, _n21, _n31, _n41, _n12, _n22, _n32, _n42,
     _n13, _n23, _n33, _n43, _n14, _n24, _n34, _n44) = self

    result(
        _n11, _n12, _n13, _n14, _n21, _n22, _n23, _n24,
        _n31, _n32, _n33, _n34, _n41, _n42, _n43, _n44
    )


@ctypes_wrap(None, VOIDP, VOIDP)
def matrix4_inverse(self, result):
    """ */

    void matrix4_inverse(const float *self, float *result) {
        float cache[16] = {
            self[9] * self[14] * self[7] - self[13] * self[10] * self[7] +
            self[13] * self[6] * self[11] - self[5] * self[14] * self[11] -
            self[9] * self[6] * self[15] + self[5] * self[10] * self[15],
            self[13] * self[10] * self[3] - self[9] * self[14] * self[3] -
            self[13] * self[2] * self[11] + self[1] * self[14] * self[11] +
            self[9] * self[2] * self[15] - self[1] * self[10] * self[15],
            self[5] * self[14] * self[3] - self[13] * self[6] * self[3] +
            self[13] * self[2] * self[7] - self[1] * self[14] * self[7] -
            self[5] * self[2] * self[15] + self[1] * self[6] * self[15],
            self[9] * self[6] * self[3] - self[5] * self[10] * self[3] -
            self[9] * self[2] * self[7] + self[1] * self[10] * self[7] +
            self[5] * self[2] * self[11] - self[1] * self[6] * self[11],
            self[12] * self[10] * self[7] - self[8] * self[14] * self[7] -
            self[12] * self[6] * self[11] + self[4] * self[14] * self[11] +
            self[8] * self[6] * self[15] - self[4] * self[10] * self[15],
            self[8] * self[14] * self[3] - self[12] * self[10] * self[3] +
            self[12] * self[2] * self[11] - self[0] * self[14] * self[11] -
            self[8] * self[2] * self[15] + self[0] * self[10] * self[15],
            self[12] * self[6] * self[3] - self[4] * self[14] * self[3] -
            self[12] * self[2] * self[7] + self[0] * self[14] * self[7] +
            self[4] * self[2] * self[15] - self[0] * self[6] * self[15],
            self[4] * self[10] * self[3] - self[8] * self[6] * self[3] +
            self[8] * self[2] * self[7] - self[0] * self[10] * self[7] -
            self[4] * self[2] * self[11] + self[0] * self[6] * self[11],
            self[8] * self[13] * self[7] - self[12] * self[9] * self[7] +
            self[12] * self[5] * self[11] - self[4] * self[13] * self[11] -
            self[8] * self[5] * self[15] + self[4] * self[9] * self[15],
            self[12] * self[9] * self[3] - self[8] * self[13] * self[3] -
            self[12] * self[1] * self[11] + self[0] * self[13] * self[11] +
            self[8] * self[1] * self[15] - self[0] * self[9] * self[15],
            self[4] * self[13] * self[3] - self[12] * self[5] * self[3] +
            self[12] * self[1] * self[7] - self[0] * self[13] * self[7] -
            self[4] * self[1] * self[15] + self[0] * self[5] * self[15],
            self[8] * self[5] * self[3] - self[4] * self[9] * self[3] -
            self[8] * self[1] * self[7] + self[0] * self[9] * self[7] +
            self[4] * self[1] * self[11] - self[0] * self[5] * self[11],
            self[12] * self[9] * self[6] - self[8] * self[13] * self[6] -
            self[12] * self[5] * self[10] + self[4] * self[13] * self[10] +
            self[8] * self[5] * self[14] - self[4] * self[9] * self[14],
            self[8] * self[13] * self[2] - self[12] * self[9] * self[2] +
            self[12] * self[1] * self[10] - self[0] * self[13] * self[10] -
            self[8] * self[1] * self[14] + self[0] * self[9] * self[14],
            self[12] * self[5] * self[2] - self[4] * self[13] * self[2] -
            self[12] * self[1] * self[6] + self[0] * self[13] * self[6] +
            self[4] * self[1] * self[14] - self[0] * self[5] * self[14],
            self[4] * self[9] * self[2] - self[8] * self[5] * self[2] +
            self[8] * self[1] * self[6] - self[0] * self[9] * self[6] -
            self[4] * self[1] * self[10] + self[0] * self[5] * self[10]
        };
        float det = self[0] * cache[0] + self[1] * cache[4] +
            self[2] * cache[8] + self[3] * cache[12];
        if (det == 0.0f) memcpy(result, matrix4_identity, 16 * sizeof(float));
        else for (int i = 0; i < 16; i ++) result[i] = cache[i] / det;
    }
    /* """
    (_n11, _n21, _n31, _n41, _n12, _n22, _n32, _n42,
     _n13, _n23, _n33, _n43, _n14, _n24, _n34, _n44) = self

    _t11 = (_n23 * _n34 * _n42 - _n24 * _n33 * _n42 + _n24 * _n32 * _n43 -
            _n22 * _n34 * _n43 - _n23 * _n32 * _n44 + _n22 * _n33 * _n44)
    _t12 = (_n14 * _n33 * _n42 - _n13 * _n34 * _n42 - _n14 * _n32 * _n43 +
            _n12 * _n34 * _n43 + _n13 * _n32 * _n44 - _n12 * _n33 * _n44)
    _t13 = (_n13 * _n24 * _n42 - _n14 * _n23 * _n42 + _n14 * _n22 * _n43 -
            _n12 * _n24 * _n43 - _n13 * _n22 * _n44 + _n12 * _n23 * _n44)
    _t14 = (_n14 * _n23 * _n32 - _n13 * _n24 * _n32 - _n14 * _n22 * _n33 +
            _n12 * _n24 * _n33 + _n13 * _n22 * _n34 - _n12 * _n23 * _n34)

    _det = _n11 * _t11 + _n21 * _t12 + _n31 * _t13 + _n41 * _t14

    if _det:
        _det = 1 / _det
        result(
            _t11 * _det,
            (_n24 * _n33 * _n41 - _n23 * _n34 * _n41 -
             _n24 * _n31 * _n43 + _n21 * _n34 * _n43 +
             _n23 * _n31 * _n44 - _n21 * _n33 * _n44) * _det,
            (_n22 * _n34 * _n41 - _n24 * _n32 * _n41 +
             _n24 * _n31 * _n42 - _n21 * _n34 * _n42 -
             _n22 * _n31 * _n44 + _n21 * _n32 * _n44) * _det,
            (_n23 * _n32 * _n41 - _n22 * _n33 * _n41 -
             _n23 * _n31 * _n42 + _n21 * _n33 * _n42 +
             _n22 * _n31 * _n43 - _n21 * _n32 * _n43) * _det,

            _t12 * _det,
            (_n13 * _n34 * _n41 - _n14 * _n33 * _n41 +
             _n14 * _n31 * _n43 - _n11 * _n34 * _n43 -
             _n13 * _n31 * _n44 + _n11 * _n33 * _n44) * _det,
            (_n14 * _n32 * _n41 - _n12 * _n34 * _n41 -
             _n14 * _n31 * _n42 + _n11 * _n34 * _n42 +
             _n12 * _n31 * _n44 - _n11 * _n32 * _n44) * _det,
            (_n12 * _n33 * _n41 - _n13 * _n32 * _n41 +
             _n13 * _n31 * _n42 - _n11 * _n33 * _n42 -
             _n12 * _n31 * _n43 + _n11 * _n32 * _n43) * _det,

            _t13 * _det,
            (_n14 * _n23 * _n41 - _n13 * _n24 * _n41 -
             _n14 * _n21 * _n43 + _n11 * _n24 * _n43 +
             _n13 * _n21 * _n44 - _n11 * _n23 * _n44) * _det,
            (_n12 * _n24 * _n41 - _n14 * _n22 * _n41 +
             _n14 * _n21 * _n42 - _n11 * _n24 * _n42 -
             _n12 * _n21 * _n44 + _n11 * _n22 * _n44) * _det,
            (_n13 * _n22 * _n41 - _n12 * _n23 * _n41 -
             _n13 * _n21 * _n42 + _n11 * _n23 * _n42 +
             _n12 * _n21 * _n43 - _n11 * _n22 * _n43) * _det,

            _t14 * _det,
            (_n13 * _n24 * _n31 - _n14 * _n23 * _n31 +
             _n14 * _n21 * _n33 - _n11 * _n24 * _n33 -
             _n13 * _n21 * _n34 + _n11 * _n23 * _n34) * _det,
            (_n14 * _n22 * _n31 - _n12 * _n24 * _n31 -
             _n14 * _n21 * _n32 + _n11 * _n24 * _n32 +
             _n12 * _n21 * _n34 - _n11 * _n22 * _n34) * _det,
            (_n12 * _n23 * _n31 - _n13 * _n22 * _n31 +
             _n13 * _n21 * _n32 - _n11 * _n23 * _n32 -
             _n12 * _n21 * _n33 + _n11 * _n22 * _n33) * _det)

    else:
        matrix4_from_identity(result)


@ctypes_wrap(None, VOIDP, VOIDP, VOIDP)
def matrix4_scale_vector3(self, vector3, result):
    """ */

    void matrix4_scale_vector3(const float *self, const float *vector3,
                               float *result) {
        vector4_mul_scalar(self, vector3[0], result);
        vector4_mul_scalar(self + 4, vector3[1], result + 4);
        vector4_mul_scalar(self + 8, vector3[2], result + 8);
        memcpy(result + 12, self + 12, 4 * sizeof(float));
    }
    /* """
    (_n11, _n21, _n31, _n41, _n12, _n22, _n32, _n42,
     _n13, _n23, _n33, _n43, _n14, _n24, _n34, _n44) = self
    _x, _y, _z = vector3
    result(
        _n11 * _x, _n21 * _x, _n31 * _x, _n41 * _x,
        _n12 * _y, _n22 * _y, _n32 * _y, _n42 * _y,
        _n13 * _z, _n23 * _z, _n33 * _z, _n43 * _z,
        _n14, _n24, _n34, _n44
    )


@ctypes_wrap(FLT, VOIDP)
def matrix4_max_scale(self):
    """ */

    float matrix4_max_scale(const float *self) {
        float result = vector3_length_squared(self);
        result = max(result, vector3_length_squared(self + 4));
        result = max(result, vector3_length_squared(self + 8));
        return sqrtf(result);
    }
    /* """
    (_n11, _n21, _n31, _, _n12, _n22, _n32, _,
     _n13, _n23, _n33, _, _, _, _, _) = self

    return max(_n11 * _n11 + _n21 * _n21 + _n31 * _n31,
               _n12 * _n12 + _n22 * _n22 + _n32 * _n32,
               _n13 * _n13 + _n23 * _n23 + _n33 * _n33) ** 0.5


@ctypes_wrap(None, FLT, FLT, FLT, VOIDP)
def matrix4_from_translation(x, y, z, result):
    """ */

    void matrix4_from_translation(float x, float y, float z, float *result) {
        result[0] = result[5] = result[10] = result[15] = 1.0f;
        result[1] = result[2] = result[4] = result[6] = result[8] =
        result[9] = result[12] = result[13] = result[14] = 0.0f;
        result[3] = x; result[7] = y; result[11] = z;
    }
    /* """
    result(1, 0, 0, x, 0, 1, 0, y, 0, 0, 1, z, 0, 0, 0, 1)


@ctypes_wrap(None, FLT, VOIDP)
def matrix4_from_rotation_x(theta, result):
    """ */

    void matrix4_from_rotation_x(float theta, float *result) {
        float _c = cosf(theta), _s = sinf(theta);
        result[0] = result[15] = 1.0f;
        result[1] = result[2] = result[3] = result[4] = result[7] =
        result[8] = result[11] = result[12] = result[13] = result[14] = 0.0f;
        result[5] = _c; result[6] = -_s; result[9] = _s; result[10] = _c;
    }
    /* """
    _c = math.cos(theta)
    _s = math.sin(theta)
    result(1, 0, 0, 0, 0, _c, - _s, 0, 0, _s, _c, 0, 0, 0, 0, 1)


@ctypes_wrap(None, FLT, VOIDP)
def matrix4_from_rotation_y(theta, result):
    """ */

    void matrix4_from_rotation_y(float theta, float *result) {
        float _c = cosf(theta), _s = sinf(theta);
        result[5] = result[15] = 1.0f;
        result[1] = result[3] = result[4] = result[6] = result[7] =
        result[9] = result[11] = result[12] = result[13] = result[14] = 0.0f;
        result[0] = _c; result[2] = _s; result[8] = -_s; result[10] = _c;
    }
    /* """
    _c = math.cos(theta)
    _s = math.sin(theta)
    result(_c, 0, _s, 0, 0, 1, 0, 0, - _s, 0, _c, 0, 0, 0, 0, 1)


@ctypes_wrap(None, FLT, VOIDP)
def matrix4_from_rotation_z(theta, result):
    """ */

    void matrix4_from_rotation_z(float theta, float *result) {
        float _c = cosf(theta), _s = sinf(theta);
        result[10] = result[15] = 1.0f;
        result[2] = result[3] = result[6] = result[7] = result[8] =
        result[9] = result[11] = result[12] = result[13] = result[14] = 0.0f;
        result[0] = _c; result[1] = -_s; result[4] = _s; result[5] = _c;
    }
    /* """
    _c = math.cos(theta)
    _s = math.sin(theta)
    result(_c, - _s, 0, 0, _s, _c, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1)


@ctypes_wrap(None, VOIDP, FLT, VOIDP)
def matrix4_from_rotation(axis, angle, result):
    """ */

    void matrix4_from_rotation(const float *axis, float angle,
                               float *result) {
        float _c = cosf(angle), _s = sinf(angle);
        float _tc = 1.0f - _c;

        result[0] = _tc * axis[0] * axis[0] + _c;
        result[1] = _tc * axis[0] * axis[1] - _s * axis[2];
        result[2] = _tc * axis[0] * axis[2] + _s * axis[1];
        result[4] = _tc * axis[0] * axis[1] + _s * axis[2];
        result[5] = _tc * axis[1] * axis[1] + _c;
        result[6] = _tc * axis[1] * axis[2] - _s * axis[0];
        result[8] = _tc * axis[0] * axis[2] - _s * axis[1];
        result[9] = -_tc * axis[1] * axis[2] + _s * axis[0];
        result[10] = _tc * axis[2] * axis[2] + _c;

        result[3] = result[7] = result[11] = result[12] = result[13] =
        result[14] = 0.0f; result[15] = 1.0f;
    }
    /* """
    _c = math.cos(angle)
    _s = math.sin(angle)
    _tc = 1 - _c
    _x, _y, _z = axis
    _tx = _tc * _x
    _ty = _tc * _y

    result(_tx * _x + _c, _tx * _y - _s * _z, _tx * _z + _s * _y, 0,
           _tx * _y + _s * _z, _ty * _y + _c, _ty * _z - _s * _x, 0,
           _tx * _z - _s * _y, _ty * _z + _s * _x, _tc * _z * _z + _c, 0,
           0, 0, 0, 1)


@ctypes_wrap(None, FLT, FLT, FLT, VOIDP)
def matrix4_from_scale(x, y, z, result):
    """ */

    void matrix4_from_scale(float x, float y, float z, float *result) {
        result[1] = result[2] = result[3] = result[4] = result[6] =
        result[7] = result[8] = result[9] = result[11] = result[12] =
        result[13] = result[14] = 0.0f;
        result[0] = x; result[5] = y; result[10] = z; result[15] = 1.0f;
    }
    /* """
    result(x, 0, 0, 0, 0, y, 0, 0, 0, 0, z, 0, 0, 0, 0, 1)


@ctypes_wrap(None, FLT, FLT, FLT, VOIDP)
def matrix4_from_shear(x, y, z, result):
    """ */

    void matrix4_from_shear(float x, float y, float z, float *result) {
        result[1] = result[9] = y; result[2] = result[6] = z;
        result[4] = result[8] = x; result[3] = result[7] = result[11] =
        result[12] = result[13] = result[14] = 0.0f;
        result[0] = result[5] = result[10] = result[15] = 1.0f;
    }
    /* """
    result(1, y, z, 0, x, 1, z, 0, x, y, 1, 0, 0, 0, 0, 1)


@ctypes_wrap(None, VOIDP, VOIDP, VOIDP, VOIDP)
def matrix4_from_compose(position, rotation, scale, result):
    """ */

    void matrix4_from_compose(const float *position, const float *rotation,
                              const float *scale, float *result) {
        result[0] = (1.0f - (rotation[1] * rotation[1] +
                             rotation[2] * rotation[2]) * 2) * scale[0];
        result[1] = (rotation[0] * rotation[1] +
                     rotation[3] * rotation[2]) * 2 * scale[0];
        result[2] = (rotation[0] * rotation[2] -
                     rotation[3] * rotation[1]) * 2 * scale[0];
        result[3] = 0.0f;
        result[4] = (rotation[0] * rotation[1] -
                     rotation[3] * rotation[2]) * 2 * scale[1];
        result[5] = (1 - (rotation[0] * rotation[0] +
                          rotation[2] * rotation[2]) * 2) * scale[1];
        result[6] = (rotation[1] * rotation[2] +
                     rotation[3] * rotation[0]) * 2 * scale[1];
        result[7] = 0.0f;
        result[8] = (rotation[0] * rotation[2] +
                     rotation[3] * rotation[1]) * 2 * scale[2];
        result[9] = (rotation[1] * rotation[2] -
                     rotation[3] * rotation[0]) * 2 * scale[2];
        result[10] = (1 - (rotation[0] * rotation[0] +
                           rotation[1] * rotation[1]) * 2) * scale[2];
        result[11] = 0.0f;
        result[12] = position[0];
        result[13] = position[1];
        result[14] = position[2];
        result[15] = 1.0f;
    }
    /* """
    x, y, z, w = rotation
    x2 = x + x
    y2 = y + y
    z2 = z + z
    xx2 = x * x2
    xy2 = x * y2
    xz2 = x * z2
    yy2 = y * y2
    yz2 = y * z2
    zz2 = z * z2
    wx2 = w * x2
    wy2 = w * y2
    wz2 = w * z2

    sx, sy, sz = scale

    result(
        (1 - (yy2 + zz2)) * sx, (xy2 + wz2) * sx, (xz2 - wy2) * sx, 0,
        (xy2 - wz2) * sy, (1 - (xx2 + zz2)) * sy, (yz2 + wx2) * sy, 0,
        (xz2 + wy2) * sz, (yz2 - wx2) * sz, (1 - (xx2 + yy2)) * sz, 0,
        position[0], position[1], position[2], 1
    )


@ctypes_wrap(None, VOIDP, VOIDP, VOIDP, VOIDP)
def matrix4_to_decompose(self, position, rotation, scale):
    """ */

    void matrix4_to_decompose(const float *self, float *position,
                              float *rotation, float *scale) {
        memcpy(position, self + 12, 3 * sizeof(float));
        scale[0] = vector3_length(self);
        scale[1] = vector3_length(self + 4);
        scale[2] = vector3_length(self + 8);
        float det = matrix4_determinant(self);
        if (det < 0.0f) scale[0] = -scale[0];
        vector3_div_scalar(self, scale[0], matrix4_0);
        vector3_div_scalar(self + 4, scale[1], matrix4_0 + 4);
        vector3_div_scalar(self + 8, scale[2], matrix4_0 + 8); // 仅 matrix3
        quaternion_from_matrix4_rotation(matrix4_0, rotation);
    }
    /* """
    vector3_from_matrix4_scale(self, scale)
    det = matrix4_determinant(self)
    if det < 0:
        scale[0] = - scale[0]

    position(self[12], self[13], self[14])
    vector3_0(1 / scale[0], 1 / scale[1], 1 / scale[2])
    matrix4_scale_vector3(self, vector3_0, matrix4_0)
    quaternion_from_matrix4_rotation(matrix4_0, rotation)


@ctypes_wrap(None, FLT, FLT, FLT, FLT, FLT, FLT, VOIDP)
def matrix4_from_perspective_bounds(
        left, right, bottom, top, near, far, result):
    """ */

    void matrix4_from_perspective_bounds(
            float left, float right, float bottom, float top, float near,
            float far, float *result) {
        result[0] = 2.0f * near / (right - left);
        result[5] = 2.0f * near / (top - bottom);
        result[8] = (right + left) / (right - left);
        result[9] = (top + bottom) / (top - bottom);
        result[10] = -(far + near) / (far - near);
        result[14] = -2.0f * far * near / (far - near);
        result[11] = -1.0f;

        result[1] = result[2] = result[3] = result[4] = result[6] =
        result[7] = result[12] = result[13] = result[15] = 0.0f;
    }
    /* """
    # 注意输入顺序，左右上下近远
    _x = 2 * near / (right - left)
    _y = 2 * near / (top - bottom)
    _a = (right + left) / (right - left)
    _b = (top + bottom) / (top - bottom)
    _c = - (far + near) / (far - near)
    _d = - 2 * far * near / (far - near)
    result(_x, 0, 0, 0, 0, _y, 0, 0, _a, _b, _c, -1, 0, 0, _d, 0)


@ctypes_wrap(None, FLT, FLT, FLT, FLT, FLT, FLT, VOIDP)
def matrix4_from_orthogonal(left, right, bottom, top, near, far, result):
    """ */

    void matrix4_from_orthogonal(
            float left, float right, float bottom, float top, float near,
            float far, float *result) {
        result[0] = 2.0f / (right - left);
        result[5] = 2.0f / (top - bottom);
        result[10] = -2.0f / (far - near);
        result[12] = -(right + left) / (right - left);
        result[13] = -(top + bottom) / (top - bottom);
        result[14] = -(far + near) / (far - near);
        result[15] = 1.0f;

        result[1] = result[2] = result[3] = result[4] = result[6] =
        result[7] = result[8] = result[9] = result[11] = 0.0f;
    }
    /* """
    # 矩阵算法，产生 Orthogonal 矩阵
    _h = 2 / (top - bottom)
    _p = -2 / (far - near)
    _w = 2 / (right - left)
    _x = -(right + left) / (right - left)
    _y = -(top + bottom) / (top - bottom)
    _z = -(far + near) / (far - near)

    result(_w, 0, 0, 0, 0, _h, 0, 0, 0, 0, _p, 0, _x, _y, _z, 1)

# */
